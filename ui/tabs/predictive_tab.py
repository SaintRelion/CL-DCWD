import os
import joblib
import matplotlib.dates as mdates
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry

# Plotting Imports
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Internal Imports
from plot_trends import plot_monthly_trend
from database.db_locations import locations, location_dict
from database.db_incident_reports import get_incident_reports
from database.db_keywords import keyword_dict  # <-- Cleaned up import

# Path for Trend Data
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")


class PredictiveTab:
    def __init__(self, parent: tk.Widget, pm: any) -> None:
        self.pm = pm
        self.frame = tk.Frame(parent, bg="#f4f7f6")

        # Create a dynamic risk mapping dictionary: ID -> "CATEGORY NAME"
        self.risk_map = {kw_id: cat.upper() for cat, kw_id in keyword_dict.items()}

        # --- 1. TOP SECTION: FILTERS ---
        ctrl_frame = tk.Frame(self.frame, bg="#ffffff", pady=10, relief="groove", bd=1)
        ctrl_frame.pack(fill="x", side="top", padx=10, pady=5)

        # Area Filter
        tk.Label(
            ctrl_frame, text="📍 Area:", font=("Arial", 10, "bold"), bg="#ffffff"
        ).pack(side="left", padx=(10, 2))
        self.brgy_list = ["All Barangays"] + sorted(
            list(set([l[1] for l in locations]))
        )
        self.brgy_var = tk.StringVar(value="All Barangays")
        self.brgy_dropdown = ttk.Combobox(
            ctrl_frame,
            textvariable=self.brgy_var,
            values=self.brgy_list,
            state="readonly",
            width=15,
        )
        self.brgy_dropdown.pack(side="left", padx=5)
        self.brgy_dropdown.bind("<<ComboboxSelected>>", lambda e: self.refresh_view())

        # Type Filter
        tk.Label(
            ctrl_frame, text="📂 Type:", font=("Arial", 10, "bold"), bg="#ffffff"
        ).pack(side="left", padx=(10, 2))
        self.cat_options = ["All Types"] + sorted(
            [cat.title() for cat in keyword_dict.keys()]
        )
        self.cat_var = tk.StringVar(value="All Types")
        self.cat_dropdown = ttk.Combobox(
            ctrl_frame,
            textvariable=self.cat_var,
            values=self.cat_options,
            state="readonly",
            width=12,
        )
        self.cat_dropdown.pack(side="left", padx=5)
        self.cat_dropdown.bind("<<ComboboxSelected>>", lambda e: self.refresh_view())

        # --- ACTION BUTTONS (Grouped on the Right) ---
        # 1. Generate Report Button
        tk.Button(
            ctrl_frame,
            text="📄 GENERATE REPORT",
            command=self.open_report_dialog,
            bg="#f39c12",  # Orange
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
        ).pack(side="right", padx=10)

        # 2. Run Analysis Button
        tk.Button(
            ctrl_frame,
            text="⚡ RUN ANALYSIS",
            command=self.run_analysis,
            bg="#2ecc71",  # Green
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
        ).pack(side="right", padx=5)

        # Day Checkboxes
        day_frame = tk.Frame(ctrl_frame, bg="#ffffff")
        day_frame.pack(side="left", padx=10)
        self.day_vars = {}
        for text, val in [
            ("M", 0),
            ("T", 1),
            ("W", 2),
            ("Th", 3),
            ("F", 4),
            ("S", 5),
            ("Su", 6),
        ]:
            var = tk.BooleanVar(value=True)
            self.day_vars[val] = var
            tk.Checkbutton(
                day_frame,
                text=text,
                variable=var,
                bg="#ffffff",
                command=self.refresh_view,
                font=("Arial", 8),
            ).pack(side="left")

        # Limit Filter
        tk.Label(
            ctrl_frame, text="🔢 Limit:", font=("Arial", 10, "bold"), bg="#ffffff"
        ).pack(side="left", padx=(5, 2))
        self.limit_var = tk.IntVar(value=50)
        self.limit_dropdown = ttk.Combobox(
            ctrl_frame,
            textvariable=self.limit_var,
            values=[20, 50, 100, 200, 500],
            state="readonly",
            width=5,
        )
        self.limit_dropdown.pack(side="left", padx=5)
        self.limit_dropdown.bind("<<ComboboxSelected>>", lambda e: self.refresh_view())

        # --- 2. MAIN CONTAINER ---
        main_container = tk.Frame(self.frame, bg="#f4f7f6")
        main_container.pack(fill="both", expand=True)

        # Left: History Feed
        self.left_panel = tk.Frame(main_container, bg="#f4f7f6")
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(10, 5))
        tk.Label(
            self.left_panel,
            text="📜 HISTORICAL EVIDENCE",
            font=("Arial", 11, "bold"),
            bg="#f4f7f6",
        ).pack(pady=5)

        self.history_canvas = tk.Canvas(
            self.left_panel, bg="#f4f7f6", highlightthickness=0
        )
        self.history_scroll = tk.Scrollbar(
            self.left_panel, orient="vertical", command=self.history_canvas.yview
        )
        self.history_container = tk.Frame(self.history_canvas, bg="#f4f7f6")
        self.canvas_window = self.history_canvas.create_window(
            (0, 0), window=self.history_container, anchor="nw"
        )

        self.history_canvas.configure(yscrollcommand=self.history_scroll.set)
        self.history_canvas.pack(side="left", fill="both", expand=True)
        self.history_scroll.pack(side="right", fill="y")
        self.history_canvas.bind(
            "<Configure>",
            lambda e: self.history_canvas.itemconfig(self.canvas_window, width=e.width),
        )

        # Right Panel: Results & Chart
        self.right_panel = tk.Frame(main_container, bg="#f4f7f6")
        self.right_panel.pack(side="right", fill="both", expand=True, padx=(5, 10))

        # Risk Tree
        self.pred_tree = ttk.Treeview(
            self.right_panel, columns=("ID", "Brgy", "Risk"), show="headings", height=8
        )
        for col in ["ID", "Brgy", "Risk"]:
            self.pred_tree.heading(col, text=col.upper())
        self.pred_tree.column("ID", width=0, stretch=tk.NO)
        self.pred_tree.pack(fill="x", expand=False)
        self.pred_tree.bind("<<TreeviewSelect>>", self.on_result_select)

        # AI Summary & Chart Area
        self.summary_panel = tk.LabelFrame(
            self.right_panel,
            text=" 📊 LINEAR RISK TREND ",
            font=("Arial", 10, "bold"),
            bg="#ffffff",
            padx=10,
            pady=10,
        )
        self.summary_panel.pack(fill="both", expand=True, pady=5)

        self.summary_text = tk.Text(
            self.summary_panel,
            font=("Consolas", 10),
            bg="#ffffff",
            relief="flat",
            height=6,
        )
        self.summary_text.pack(fill="x", expand=False)

        self.chart_container = tk.Frame(self.summary_panel, bg="white")
        self.chart_container.pack(fill="both", expand=True)

        self.refresh_view()

    def open_report_dialog(self) -> None:
        dialog: tk.Toplevel = tk.Toplevel(self.frame)
        dialog.title("Generate Trend Report")
        dialog.geometry("340x360")
        dialog.resizable(False, False)
        dialog.config(bg="#f4f7f6", padx=20, pady=15)
        dialog.transient(self.frame.winfo_toplevel())
        dialog.grab_set()

        tk.Label(
            dialog, text="Resolution:", bg="#f4f7f6", font=("Arial", 9, "bold")
        ).pack(anchor="w", pady=(0, 2))
        res_var: tk.StringVar = tk.StringVar(value="Monthly (M)")
        ttk.Combobox(
            dialog,
            textvariable=res_var,
            values=["Daily (D)", "Weekly (W)", "Monthly (M)", "Quarterly (Q)"],
            state="readonly",
        ).pack(fill="x", pady=(0, 10))

        tk.Label(
            dialog, text="Top N Locations:", bg="#f4f7f6", font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(0, 2))
        top_n_var: tk.IntVar = tk.IntVar(value=5)
        ttk.Spinbox(dialog, from_=1, to=50, textvariable=top_n_var, width=10).pack(
            fill="x", pady=(0, 10)
        )

        tk.Label(
            dialog, text="Start Date:", bg="#f4f7f6", font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(0, 2))
        start_picker: DateEntry = DateEntry(
            dialog,
            width=12,
            background="#3498db",
            foreground="white",
            borderwidth=0,
            date_pattern="yyyy-mm-dd",
        )
        start_picker.set_date(datetime.now().replace(day=1))
        start_picker.pack(fill="x", pady=(0, 10))

        tk.Label(
            dialog, text="End Date:", bg="#f4f7f6", font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(0, 2))
        end_picker: DateEntry = DateEntry(
            dialog,
            width=12,
            background="#3498db",
            foreground="white",
            borderwidth=0,
            date_pattern="yyyy-mm-dd",
        )
        end_picker.set_date(datetime.now())
        end_picker.pack(fill="x", pady=(0, 10))

        tk.Label(
            dialog, text="Save Location:", bg="#f4f7f6", font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(0, 2))
        path_frame: tk.Frame = tk.Frame(dialog, bg="#f4f7f6")
        path_frame.pack(fill="x", pady=(0, 15))

        default_dir: str = os.path.expanduser("~/Desktop")
        if not os.path.exists(default_dir):
            default_dir = os.path.expanduser("~")

        save_dir_var: tk.StringVar = tk.StringVar(value=default_dir)
        ttk.Entry(path_frame, textvariable=save_dir_var, state="readonly").pack(
            side="left", fill="x", expand=True
        )

        def browse_folder() -> None:
            folder: str = filedialog.askdirectory(
                parent=dialog,
                title="Select Output Folder",
                initialdir=save_dir_var.get(),
            )
            if folder:
                save_dir_var.set(folder)

        tk.Button(
            path_frame,
            text="Browse",
            command=browse_folder,
            bg="#ecf0f1",
            font=("Arial", 9),
        ).pack(side="right", padx=(5, 0))

        def on_confirm() -> None:
            res_code: str = res_var.get().split("(")[1][0]

            start_val = start_picker.get_date().strftime("%Y-%m-%d")
            end_val = end_picker.get_date().strftime("%Y-%m-%d")
            save_path = save_dir_var.get()

            if not start_val or not end_val:
                messagebox.showwarning(
                    "Input Error", "Please provide dates.", parent=dialog
                )
                return

            dialog.destroy()

            self.generate_report(
                top_n_var.get(), start_val, end_val, res_code, save_path
            )

        btn_frame: tk.Frame = tk.Frame(dialog, bg="#f4f7f6")
        btn_frame.pack(fill="x")
        tk.Button(btn_frame, text="Cancel", command=dialog.destroy, width=10).pack(
            side="right", padx=(5, 0)
        )
        tk.Button(
            btn_frame,
            text="Generate",
            command=on_confirm,
            bg="#2ecc71",
            fg="white",
            font=("Arial", 10, "bold"),
            width=10,
        ).pack(side="right")

    def generate_report(
        self, top_n: int, start_date: str, end_date: str, resolution: str, save_dir: str
    ) -> None:
        out_img: str = os.path.join(save_dir, "incident_trend_analysis.png")
        out_pdf: str = os.path.join(save_dir, "incident_trend_report.pdf")

        try:
            plot_monthly_trend(
                top_n_locations=top_n,
                date_from=start_date,
                date_to=end_date,
                resolution=resolution,
                output_image=out_img,
                output_pdf=out_pdf,
            )
            messagebox.showinfo(
                "Success", f"Report successfully generated!\n\nSaved in:\n{save_dir}"
            )
        except Exception as e:
            messagebox.showerror("Generation Failed", str(e))

    def show_trend_chart(self, loc_id: int) -> None:
        """Plots the historical frequency from trend_data.pkl."""
        for widget in self.chart_container.winfo_children():
            widget.destroy()

        try:
            trend_df = joblib.load(os.path.join(MODEL_DIR, "trend_data.pkl"))
            if trend_df.empty:
                raise ValueError
        except:
            tk.Label(
                self.chart_container, text="No historical trend data found.", bg="white"
            ).pack(pady=20)
            return

        loc_trend = trend_df[trend_df["loc_id"] == str(loc_id)]
        fig, ax = plt.subplots(figsize=(5, 2.8), dpi=80)
        fig.patch.set_facecolor("white")

        if not loc_trend.empty:
            color_palette = ["#e74c3c", "#f1c40f", "#3498db", "#9b59b6", "#2ecc71"]

            # FIX: Use the model's index mapping (0..N) instead of Database IDs
            for cat_idx, cat_name in self.pm.index_to_cat.items():
                # Filter by the index stored during training
                data = loc_trend[loc_trend["target_idx"] == cat_idx].sort_values("ts")

                if not data.empty:
                    label = cat_name.replace("_", " ").title()
                    ax.plot(
                        data["ts"],
                        data["count"],
                        marker="o",
                        markersize=4,
                        label=label,
                        color=color_palette[cat_idx % len(color_palette)],
                        linewidth=1.5,
                    )

                    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
                    ax.xaxis.set_major_locator(mdates.AutoDateLocator())

                    ax.set_title(f"Historical Incident Frequency", fontsize=10)
                    ax.legend(fontsize=8, loc="upper left")
                    ax.tick_params(axis="both", labelsize=7)

                    # Increase rotation for better readability
                    plt.xticks(rotation=45)
                    fig.tight_layout()

            ax.set_title(
                f"Historical Incident Frequency (Brgy. {location_dict[loc_id]['barangay']})",
                fontsize=10,
            )
            ax.legend(fontsize=8, loc="upper left")
            ax.tick_params(axis="both", which="major", labelsize=7)
            plt.xticks(rotation=25)
            fig.tight_layout()
        else:
            ax.text(
                0.5,
                0.5,
                "Location is Stable\n(No historical incidents)",
                ha="center",
                va="center",
            )

        canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def refresh_view(self) -> None:
        for widget in self.history_container.winfo_children():
            widget.destroy()

        selected_brgy = self.brgy_var.get()
        selected_cat = self.cat_var.get()
        allowed_days = [d for d, v in self.day_vars.items() if v.get()]
        limit = self.limit_var.get()

        # Dynamic Direct ID Matcher using our new dictionary
        selected_cat = self.cat_var.get()

        db_category_match = selected_cat.lower().replace(" ", "_")
        all_reports = get_incident_reports(limit=3000)

        count = 0
        for r in all_reports:
            if count >= limit:
                break

            inc_id, ts, cat_name_db, loc_id, street_name, plumber, status, remarks = r

            clean_cat_db = cat_name_db.lower().replace(" ", "_")

            loc_data = location_dict.get(loc_id, {"barangay": "Unknown"})
            brgy_name: str = loc_data["barangay"]

            if selected_brgy != "All Barangays" and brgy_name != selected_brgy:
                continue

            if ts.weekday() not in allowed_days:
                continue

            if selected_cat != "All Types" and clean_cat_db != db_category_match:
                continue

            card = tk.Frame(
                self.history_container,
                bg="white",
                relief="ridge",
                bd=1,
                padx=10,
                pady=8,
            )
            card.pack(fill="x", pady=3, padx=10)

            tk.Label(
                card,
                text=f"{clean_cat_db.upper()}",
                font=("Arial", 11, "bold"),
                bg="white",
                fg="#2c3e50",
            ).pack(anchor="w")

            display_street = f"{street_name}, " if street_name else ""
            tk.Label(
                card,
                text=f"📍 {display_street}Brgy. {brgy_name}",
                font=("Arial", 10),
                bg="white",
                fg="#7f8c8d",
            ).pack(anchor="w")
            tk.Label(
                card,
                text=f"🗓️ {ts.strftime('%a, %b %d, %Y - %I:%M %p')}",
                font=("Arial", 10),
                bg="white",
                fg="#3498db",
            ).pack(anchor="w")

            count += 1

        self.history_container.update_idletasks()
        self.history_canvas.config(scrollregion=self.history_canvas.bbox("all"))

    def run_analysis(self) -> None:
        """Runs the prediction for each location and updates the results tree."""
        self.pred_tree.delete(*self.pred_tree.get_children())
        selected_brgy = self.brgy_var.get()

        for loc_id, brgy, lat, lon in locations:
            if selected_brgy != "All Barangays" and brgy != selected_brgy:
                continue

            report = self.pm.get_daily_risk_report(loc_id)
            if not report:
                continue

            # The model returns a dict: { "category_name": probability }
            top_name = max(report, key=report.get)
            top_val = report[top_name]

            # Format the name (e.g., dirty_water -> DIRTY WATER)
            risk_label = top_name.replace("_", " ").upper()
            status = f"⚠️ {risk_label} ({top_val}%)" if top_val >= 10 else "✅ STABLE"

            self.pred_tree.insert("", "end", values=(loc_id, brgy, status))

    def on_result_select(self, event: any) -> None:
        """Handles selection of a result to show detailed breakdown and trend chart."""
        selected = self.pred_tree.selection()
        if not selected:
            return

        values = self.pred_tree.item(selected[0], "values")
        loc_id = int(values[0])
        report = self.pm.get_daily_risk_report(loc_id)

        self.summary_text.config(state=tk.NORMAL)
        self.summary_text.delete("1.0", tk.END)
        summary = f"LOCATION: Brgy. {values[1]}\n" + "-" * 45 + "\n"

        # Show all probabilities in the textbox
        for cat_name, pct in report.items():
            label = cat_name.replace("_", " ").title().ljust(15)
            bar = "■" * int(pct / 5)
            summary += f"{label} | {pct:>6.2f}% {bar}\n"

        self.summary_text.insert(tk.END, summary)
        self.summary_text.config(state=tk.DISABLED)

        # Refresh the chart
        self.show_trend_chart(loc_id)
