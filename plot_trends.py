import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D
from datetime import datetime
from typing import List, Optional, Literal
from fpdf import FPDF  # NEW: PDF Library

from database.db_locations import get_location_by_id
from database.db_incident_reports import get_incident_reports

# ── Category mapping ────────────────────────────────────────────────────────
CAT_GROUPS = {
    **{k: 0 for k in [1, 4, 7]},  # No Water
    **{k: 1 for k in [2, 5, 8]},  # Leak
    **{k: 2 for k in [3, 6, 9]},  # Dirty Water
}
CAT_NAMES = {0: "No Water", 1: "Leak", 2: "Dirty Water"}
CAT_COLORS = {0: "#378ADD", 1: "#D85A30", 2: "#1D9E75"}


# ── Helpers ──────────────────────────────────────────────────────────────────
def load_dataframe() -> Optional[pd.DataFrame]:
    records = get_incident_reports(limit=None)
    if not records:
        return None
    cols = ["id", "pid", "cat_id", "loc_id", "lat", "lon", "ts", "t1", "t2", "cat_name"]
    df = pd.DataFrame(records, columns=cols)
    df["ts"] = pd.to_datetime(df["ts"])
    df["cat_grp"] = df["cat_id"].map(CAT_GROUPS)
    df = df[df["cat_grp"].notna()].copy()
    df["cat_grp"] = df["cat_grp"].astype(int)
    df["loc_id"] = df["loc_id"].astype(str)
    return df


def get_location_label(loc_id: str) -> str:
    info = get_location_by_id(int(loc_id))
    if info:
        return info["barangay"]  # or f"{info['street']}, {info['barangay']}"
    return f"Loc {loc_id}"


def build_location_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Per-location counts per category, plus dominant category."""
    grp = (
        df.groupby(["loc_id", "cat_grp"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=[0, 1, 2], fill_value=0)
    )
    grp["total"] = grp.sum(axis=1)
    grp["dominant"] = grp[[0, 1, 2]].idxmax(axis=1)
    return grp.reset_index().sort_values("total", ascending=False)


ResolutionT = Literal["D", "W", "M", "Q"]  # daily / weekly / monthly / quarterly

_RESOLUTION_LABELS = {"D": "Daily", "W": "Weekly", "M": "Monthly", "Q": "Quarterly"}


# ── PDF Generation ───────────────────────────────────────────────────────────
def export_trend_pdf(
    image_path: str,
    loc_summary: pd.DataFrame,
    selected_locs: List[str],
    loc_labels: dict,
    date_from_dt: datetime,
    date_to_dt: datetime,
    output_path: str = "incident_trend_report.pdf",
) -> None:
    """Generates a structured PDF with the chart and a color-coded discussion."""
    pdf = FPDF()
    pdf.add_page()

    # 1. Place the generated chart at the top
    # A4 width is 210mm. Margins are 10mm. Usable width = 190mm.
    pdf.image(image_path, x=10, y=10, w=190)

    # 2. Push text down below the image (Aspect ratio puts bottom around 145mm)
    pdf.set_y(150)

    # 3. Report Header
    pdf.set_font("helvetica", "B", 16)
    pdf.set_text_color(44, 44, 42)  # Dark Gray
    pdf.cell(0, 10, "Executive Summary & Location Breakdown", ln=True)

    pdf.set_font("helvetica", "", 10)
    pdf.set_text_color(95, 94, 90)  # Light Gray
    date_str = (
        f"{date_from_dt.strftime('%b %d, %Y')} to {date_to_dt.strftime('%b %d, %Y')}"
    )
    pdf.cell(0, 6, f"Analysis Period: {date_str}", ln=True)
    pdf.ln(5)

    # RGB mapping based on your hex CAT_COLORS
    color_map = {
        0: (55, 138, 221),  # No Water (Blue)
        1: (216, 90, 48),  # Leak (Orange)
        2: (29, 158, 117),  # Dirty Water (Green)
    }

    # 4. Grouped Colorful Discussion
    for loc_id in selected_locs:
        row = loc_summary[loc_summary["loc_id"] == loc_id].iloc[0]
        loc_name = loc_labels[loc_id]
        total = row["total"]
        dominant_cat = row["dominant"]
        dom_name = CAT_NAMES[dominant_cat]

        # Location Title
        pdf.set_font("helvetica", "B", 12)
        pdf.set_text_color(44, 44, 42)
        pdf.cell(0, 8, f"> {loc_name} (Total Incidents: {total})", ln=True)

        # Dominant Issue with dynamic color mapping
        pdf.set_font("helvetica", "", 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(10, 6, "", border=0)  # Indent
        pdf.write(6, "Dominant Issue: ")

        # Inject the specific color for the category
        r, g, b = color_map[dominant_cat]
        pdf.set_font("helvetica", "B", 10)
        pdf.set_text_color(r, g, b)
        pdf.write(6, f"{dom_name.upper()}\n")

        # Raw Breakdown
        pdf.set_font("helvetica", "", 9)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(10, 5, "", border=0)  # Indent
        breakdown_text = (
            f"Breakdown: {row[0]} No Water  |  {row[1]} Leaks  |  {row[2]} Dirty Water"
        )
        pdf.cell(0, 5, breakdown_text, ln=True)
        pdf.ln(4)  # Space between locations

    pdf.output(output_path)
    print(f"[SUCCESS] PDF Report saved → {output_path}")


# ── Main plot ────────────────────────────────────────────────────────────────
def plot_monthly_trend(
    top_n_locations: int = 10,
    locations: Optional[List[int]] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    resolution: ResolutionT = "M",
    output_image: str = "incident_trend_analysis.png",
    output_pdf: str = "incident_trend_report.pdf",
) -> None:
    """
    Two-panel figure:
      Top    — Bubble congregation chart for the resolved location set.
      Bottom — Stacked-area trend at the requested resolution.
    """

    df = load_dataframe()
    if df is None:
        print("[PLOT] No data available.")
        return

    # ── 1. Date filtering ────────────────────────────────────────────────────
    date_from_dt = pd.to_datetime(date_from) if date_from else df["ts"].min()
    date_to_dt = pd.to_datetime(date_to) if date_to else datetime.now()

    df = df[(df["ts"] >= date_from_dt) & (df["ts"] <= date_to_dt)].copy()
    if df.empty:
        print(
            f"[PLOT] No incidents in range {date_from_dt.date()} → {date_to_dt.date()}."
        )
        return

    # ── 2. Location filtering ────────────────────────────────────────────────
    loc_summary = build_location_summary(df)

    if locations:
        selected_locs = [str(l) for l in locations]
        missing = [l for l in selected_locs if l not in loc_summary["loc_id"].values]
        if missing:
            print(
                f"[PLOT] Warning: location(s) {missing} have no data in the selected range."
            )
        selected_locs = [l for l in selected_locs if l in loc_summary["loc_id"].values]
    else:
        selected_locs = loc_summary.head(top_n_locations)["loc_id"].tolist()

    if not selected_locs:
        print("[PLOT] No valid locations to plot.")
        return

    loc_labels = {loc: get_location_label(loc) for loc in selected_locs}

    # ── 3. Build subtitle from active filters ─────────────────────────────────
    range_label = (
        f"{date_from_dt.strftime('%b %d %Y')} → {date_to_dt.strftime('%b %d %Y')}"
    )
    loc_label = (
        f"Loc {', '.join(selected_locs)}"
        if locations
        else f"Top {top_n_locations} by volume"
    )
    subtitle = (
        f"{loc_label}  ·  {range_label}  ·  {_RESOLUTION_LABELS[resolution]} buckets"
    )

    # ── 4. Figure layout ──────────────────────────────────────────────────────
    fig = plt.figure(figsize=(16, 11), facecolor="#FAFAFA")
    gs = gridspec.GridSpec(
        2,
        1,
        figure=fig,
        hspace=0.42,
        top=0.91,
        bottom=0.08,
        left=0.07,
        right=0.97,
        height_ratios=[1.1, 1],
    )
    ax_bubble = fig.add_subplot(gs[0])
    ax_trend = fig.add_subplot(gs[1])

    fig.suptitle(
        "Water Incident Analysis — Per-Location Congregation & Trend",
        fontsize=14,
        fontweight="medium",
        color="#2C2C2A",
        y=0.97,
    )
    fig.text(0.5, 0.935, subtitle, ha="center", fontsize=9, color="#5F5E5A")

    # ── 5. Bubble congregation panel ─────────────────────────────────────────
    max_total = loc_summary["total"].max()

    for xi, row in enumerate(loc_summary.itertuples()):
        is_selected = row.loc_id in selected_locs
        area = 80 + (row.total / max_total) * 520
        color = CAT_COLORS[row.dominant]
        alpha = 0.78 if is_selected else 0.18
        ax_bubble.scatter(
            xi,
            row.total,
            s=area,
            c=color,
            alpha=alpha,
            linewidths=0.6 if is_selected else 0.2,
            edgecolors=color,
        )
        if is_selected:
            ax_bubble.annotate(
                f"{loc_labels[row.loc_id]}",
                xy=(xi, row.total),
                xytext=(0, 6),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=7.5,
                color="#444441",
            )

    ax_bubble.set_xlim(-1, len(loc_summary))
    ax_bubble.set_ylim(0, max_total * 1.25)
    ax_bubble.set_xticks([])
    ax_bubble.set_ylabel("Total Incidents", fontsize=11, color="#444441")
    ax_bubble.set_title(
        "Incident Congregation per Location  ·  highlighted = selected  ·  colour = dominant category",
        fontsize=10,
        color="#5F5E5A",
        pad=8,
    )
    ax_bubble.spines[["top", "right", "bottom"]].set_visible(False)
    ax_bubble.spines["left"].set_color("#D3D1C7")
    ax_bubble.yaxis.grid(
        True, linestyle="--", linewidth=0.5, color="#D3D1C7", alpha=0.8
    )
    ax_bubble.set_axisbelow(True)
    ax_bubble.set_facecolor("#FAFAFA")

    legend_handles = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="none",
            markerfacecolor=CAT_COLORS[c],
            markeredgecolor=CAT_COLORS[c],
            markersize=9,
            label=CAT_NAMES[c],
        )
        for c in [0, 1, 2]
    ]
    ax_bubble.legend(
        handles=legend_handles, loc="upper right", fontsize=9, frameon=False
    )

    # ── 6. Trend panel (resolution-aware) ────────────────────────────────────
    df_sel = df[df["loc_id"].isin(selected_locs)].copy()
    df_sel["bucket"] = df_sel["ts"].dt.to_period(resolution)

    bucketed = df_sel.groupby(["bucket", "loc_id"]).size().unstack(fill_value=0)
    full_range = pd.period_range(
        start=pd.Timestamp(date_from_dt).to_period(resolution),
        end=pd.Timestamp(date_to_dt).to_period(resolution),
        freq=resolution,
    )

    bucketed = bucketed.reindex(full_range, fill_value=0)
    x_dates = [p.to_timestamp() for p in bucketed.index]

    cmap = plt.cm.get_cmap("tab10", len(selected_locs))
    colors = [cmap(i) for i in range(len(selected_locs))]

    bottom = np.zeros(len(bucketed))
    for i, loc in enumerate(selected_locs):
        vals = (
            bucketed[loc].values if loc in bucketed.columns else np.zeros(len(bucketed))
        )
        ax_trend.fill_between(
            x_dates, bottom, bottom + vals, color=colors[i], alpha=0.65, linewidth=0
        )
        ax_trend.plot(x_dates, bottom + vals, color=colors[i], linewidth=0.7, alpha=0.9)
        bottom += vals

    ax_trend.set_xlim(x_dates[0], x_dates[-1])
    ax_trend.set_ylim(0)
    ax_trend.set_ylabel(
        f"{_RESOLUTION_LABELS[resolution]} Incidents (stacked)",
        fontsize=11,
        color="#444441",
    )
    ax_trend.set_title(
        f"{_RESOLUTION_LABELS[resolution]} Volume — {loc_label}  (stacked, each band = one location)",
        fontsize=10,
        color="#5F5E5A",
        pad=8,
    )
    ax_trend.spines[["top", "right"]].set_visible(False)
    ax_trend.spines[["left", "bottom"]].set_color("#D3D1C7")
    ax_trend.xaxis.set_tick_params(rotation=35, labelsize=9)
    ax_trend.yaxis.grid(True, linestyle="--", linewidth=0.5, color="#D3D1C7", alpha=0.8)
    ax_trend.set_axisbelow(True)
    ax_trend.set_facecolor("#FAFAFA")

    trend_handles = [
        Line2D(
            [0],
            [0],
            color=colors[i],
            linewidth=5,
            alpha=0.65,
            label=loc_labels[selected_locs[i]],
        )
        for i in range(len(selected_locs))
    ]
    ax_trend.legend(
        handles=trend_handles, loc="upper left", ncol=2, fontsize=8, frameon=False
    )

    # ── 7. Save Image & Trigger PDF Build ────────────────────────────────────
    plt.savefig(output_image, dpi=150, bbox_inches="tight", facecolor="#FAFAFA")
    plt.close()
    print(f"[SUCCESS] Chart saved → {output_image}")

    # Generate the PDF with the image and summary text
    export_trend_pdf(
        image_path=output_image,
        loc_summary=loc_summary,
        selected_locs=selected_locs,
        loc_labels=loc_labels,
        date_from_dt=date_from_dt,
        date_to_dt=date_to_dt,
        output_path=output_pdf,
    )


if __name__ == "__main__":
    plot_monthly_trend()
