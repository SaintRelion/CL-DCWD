import os
import joblib
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
from database.db_locations import locations
from database.db_incident_reports import get_incident_reports

# Path for Trend Data
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")


class PredictiveTab:
    def __init__(self, parent: tk.Widget, pm: any) -> None:
        self.pm = pm
        self.frame = tk.Frame(parent, bg="#f4f7f6")

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
        self.cat_options = ["All Types", "No Water", "Leak", "Dirty Water"]
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

        tk.Button(
            ctrl_frame,
            text="⚡ RUN ANALYSIS",
            command=self.run_analysis,
            bg="#2ecc71",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
        ).pack(side="right", padx=10)

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
            self.right_panel,
            columns=("ID", "Brgy", "Street", "Risk"),
            show="headings",
            height=8,
        )
        for col in ["ID", "Brgy", "Street", "Risk"]:
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

        # Dev Tools
        dev_frame = tk.LabelFrame(
            self.right_panel,
            text=" 🛠️ DEV TOOLS ",
            bg="#ffffff",
            font=("Arial", 8, "bold"),
        )
        dev_frame.pack(fill="x", side="bottom", pady=(5, 10))
        tk.Button(
            dev_frame,
            text="🚀 SIM 1YR",
            command=self.trigger_sim,
            bg="#3498db",
            fg="white",
            font=("Arial", 8, "bold"),
        ).pack(side="left", padx=5, pady=5, expand=True, fill="x")
        tk.Button(
            dev_frame,
            text="🧹 WIPE",
            command=self.trigger_wipe,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 8, "bold"),
        ).pack(side="left", padx=5, pady=5, expand=True, fill="x")
        # --- NEW REPORT BUTTON ---
        tk.Button(
            dev_frame,
            text="📄 GENERATE REPORT",
            command=self.open_report_dialog,
            bg="#f39c12",
            fg="white",
            font=("Arial", 8, "bold"),
        ).pack(side="left", padx=5, pady=5, expand=True, fill="x")

        self.refresh_view()

    def open_report_dialog(self) -> None:
        """Opens a modal dialog to specify report parameters using date pickers and directory selection."""
        dialog: tk.Toplevel = tk.Toplevel(self.frame)
        dialog.title("Generate Trend Report")
        dialog.geometry(
            "340x360"
        )  # Increased height and slightly wider for the file path
        dialog.resizable(False, False)
        dialog.config(bg="#f4f7f6", padx=20, pady=15)

        dialog.transient(self.frame.winfo_toplevel())
        dialog.grab_set()

        # Resolution (D, W, M, Q)
        tk.Label(
            dialog, text="Resolution:", bg="#f4f7f6", font=("Arial", 9, "bold")
        ).pack(anchor="w", pady=(0, 2))
        res_var: tk.StringVar = tk.StringVar(value="Monthly (M)")
        res_dropdown: ttk.Combobox = ttk.Combobox(
            dialog,
            textvariable=res_var,
            values=["Daily (D)", "Weekly (W)", "Monthly (M)", "Quarterly (Q)"],
            state="readonly",
        )
        res_dropdown.pack(fill="x", pady=(0, 10))

        # Top N Locations
        tk.Label(
            dialog, text="Top N Locations:", bg="#f4f7f6", font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(0, 2))
        top_n_var: tk.IntVar = tk.IntVar(value=10)
        top_n_spin: ttk.Spinbox = ttk.Spinbox(
            dialog, from_=1, to=50, textvariable=top_n_var, width=10
        )
        top_n_spin.pack(fill="x", pady=(0, 10))

        # Start Date Picker
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

        # End Date Picker
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

        # Save Directory Selection
        tk.Label(
            dialog, text="Save Location:", bg="#f4f7f6", font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(0, 2))

        path_frame: tk.Frame = tk.Frame(dialog, bg="#f4f7f6")
        path_frame.pack(fill="x", pady=(0, 15))

        # Default to the user's desktop or home directory
        default_dir: str = os.path.expanduser("~/Desktop")
        if not os.path.exists(default_dir):
            default_dir = os.path.expanduser("~")

        save_dir_var: tk.StringVar = tk.StringVar(value=default_dir)
        path_entry: ttk.Entry = ttk.Entry(
            path_frame, textvariable=save_dir_var, state="readonly"
        )
        path_entry.pack(side="left", fill="x", expand=True)

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
            # Extract the raw values
            raw_res: str = res_var.get()
            top_n: int = top_n_var.get()
            s_date: str = start_picker.get()
            e_date: str = end_picker.get()
            save_dir: str = save_dir_var.get()

            # Parse the resolution character (e.g., 'M' from 'Monthly (M)')
            res_code: str = raw_res.split("(")[1][0]

            if not s_date or not e_date:
                messagebox.showwarning(
                    "Input Error",
                    "Please provide both start and end dates.",
                    parent=dialog,
                )
                return

            if not os.path.isdir(save_dir):
                messagebox.showwarning(
                    "Directory Error",
                    "Please select a valid folder to save the reports.",
                    parent=dialog,
                )
                return

            dialog.destroy()
            self.generate_report(top_n, s_date, e_date, res_code, save_dir)

        # Buttons
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
        """Executes the plot_monthly_trend function with user-defined parameters."""

        # Build absolute paths for the image and PDF
        out_img: str = os.path.join(save_dir, "incident_trend_analysis.png")
        out_pdf: str = os.path.join(save_dir, "incident_trend_report.pdf")

        print(
            f"Generating trend report: Top {top_n}, {start_date} -> {end_date}, Res: {resolution}\nSaving to: {save_dir}"
        )

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
                "Success",
                f"Report successfully generated!\n\nSaved in:\n{save_dir}\n\nParameters:\n- Top: {top_n}\n- Range: {start_date} to {end_date}\n- Resolution: {resolution}",
            )

        except Exception as e:
            messagebox.showerror("Generation Failed", str(e))

    # ---------------------------

    def show_trend_chart(self, loc_id: int) -> None:
        """Displays a linear incident count chart in the UI."""
        for widget in self.chart_container.winfo_children():
            widget.destroy()

        try:
            trend_df = joblib.load(os.path.join(MODEL_DIR, "trend_data.pkl"))
            if trend_df.empty:
                raise ValueError
        except:
            tk.Label(
                self.chart_container, text="No simulation/trend data found.", bg="white"
            ).pack(pady=20)
            return

        loc_trend = trend_df[trend_df["loc_id"] == str(loc_id)]
        fig, ax = plt.subplots(figsize=(5, 2.5), dpi=80)
        fig.patch.set_facecolor("white")

        if not loc_trend.empty:
            colors = {0: "#e74c3c", 1: "#f1c40f", 2: "#8e44ad"}
            labels = {0: "No Water", 1: "Leak", 2: "Dirty"}
            for cat_id in [0, 1, 2]:
                data = loc_trend[loc_trend["target_idx"] == cat_id].sort_values("ts")
                if not data.empty:
                    ax.plot(
                        data["ts"],
                        data["count"],
                        marker="o",
                        label=labels[cat_id],
                        color=colors[cat_id],
                        linewidth=1.5,
                    )
            ax.set_title("Historical Frequency Basis", fontsize=11)
            ax.legend(fontsize=9)
            ax.tick_params(axis="both", which="major", labelsize=7)
            plt.xticks(rotation=20)
        else:
            ax.text(
                0.5,
                0.5,
                "Location is Stable\n(0 incidents in history)",
                ha="center",
                va="center",
            )

        canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def refresh_view(self) -> None:
        """Unified Filter Logic (Barangay, Day, Type, Limit)."""
        for widget in self.history_container.winfo_children():
            widget.destroy()
        selected_brgy = self.brgy_var.get()
        selected_cat = self.cat_var.get()
        allowed_days = [d for d, v in self.day_vars.items() if v.get()]
        limit = self.limit_var.get()

        # Use ID mapping for the Category filter
        cat_groups = {
            "No Water": [1, 4, 7],
            "Leak": [2, 5, 8],
            "Dirty Water": [3, 6, 9],
        }

        all_reports = get_incident_reports(limit=3000)
        loc_map = {l[0]: (l[1], l[2]) for l in locations}

        count = 0
        for r in all_reports:
            if count >= limit:
                break
            brgy_name, street_name = loc_map.get(r[3], ("Unknown", "Unknown"))
            ts, cat_id = r[6], r[2]

            if selected_brgy != "All Barangays" and brgy_name != selected_brgy:
                continue
            if ts.weekday() not in allowed_days:
                continue
            if selected_cat != "All Types" and cat_id not in cat_groups.get(
                selected_cat, []
            ):
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
                text=f"{r[9].upper()}",
                font=("Arial", 11, "bold"),
                bg="white",
                fg="#2c3e50",
            ).pack(anchor="w")
            tk.Label(
                card,
                text=f"📍 {brgy_name}, {street_name}",
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
        """Isolated Linear Analysis."""
        self.pred_tree.delete(*self.pred_tree.get_children())
        selected_brgy = self.brgy_var.get()
        risk_map = {1: "NO WATER", 2: "LEAK", 3: "DIRTY WATER"}
        for loc_id, brgy, street, _, _ in locations:
            if selected_brgy != "All Barangays" and brgy != selected_brgy:
                continue
            report = self.pm.get_daily_risk_report(loc_id)
            top_id = max(report, key=report.get)
            top_val = report[top_id]
            status = (
                f"⚠️ {risk_map[top_id]} ({top_val}%)" if top_val >= 10 else "✅ STABLE"
            )
            self.pred_tree.insert("", "end", values=(loc_id, brgy, street, status))

    def on_result_select(self, event: any) -> None:
        """Displays breakdown and triggers the trend chart."""
        selected = self.pred_tree.selection()
        if not selected:
            return
        values = self.pred_tree.item(selected[0], "values")
        loc_id = int(values[0])
        report = self.pm.get_daily_risk_report(loc_id)

        self.summary_text.config(state=tk.NORMAL)
        self.summary_text.delete("1.0", tk.END)
        summary = f"LOCATION: {values[1]}, {values[2]}\n" + "-" * 45 + "\n"
        for r_id, pct in report.items():
            label = {1: "NO WATER", 2: "LEAK    ", 3: "DIRTY   "}[r_id]
            summary += f"{label} | {pct:>6.2f}% " + ("■" * int(pct / 5)) + "\n"

        self.summary_text.insert(tk.END, summary)
        self.summary_text.config(state=tk.DISABLED)

        # Update the Chart
        self.show_trend_chart(loc_id)

    def trigger_sim(self) -> None:
        from simulate_incident import simulate_weekly_pattern

        selected = self.pred_tree.selection()
        loc_id = (
            int(self.pred_tree.item(selected[0], "values")[0]) if selected else None
        )
        simulate_weekly_pattern(weeks=52, loc_id=loc_id)
        self.pm.reloadModel()
        self.run_analysis()
        self.refresh_view()

    def trigger_wipe(self) -> None:
        from simulate_incident import delete_weekly_pattern

        delete_weekly_pattern(months=12)
        self.pm.reloadModel()
        self.run_analysis()
        self.refresh_view()
