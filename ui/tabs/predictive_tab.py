import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

# Internal Imports
from database.db_locations import locations
from database.db_incident_reports import get_incident_reports, get_rolling_counts


class PredictiveTab:
    def __init__(self, parent, pm):
        self.pm = pm
        self.frame = tk.Frame(parent, bg="#f4f7f6")

        # --- HEADER ---
        header_frame = tk.Frame(self.frame, bg="#f4f7f6")
        header_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(
            header_frame,
            text="DA-WATS PREDICTIVE RISK ENGINE",
            font=("Verdana", 14, "bold"),
            fg="#2c3e50",
            bg="#f4f7f6",
        ).pack(side="left")

        # --- CONTROLS ---
        ctrl_frame = tk.Frame(self.frame, bg="#f4f7f6")
        ctrl_frame.pack(fill="x", padx=20)

        tk.Button(
            ctrl_frame,
            text="🔄 RECALIBRATE MODEL",
            command=self.run_recalibration,
            bg="#3498db",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=10,
        ).pack(side="left", pady=10)

        tk.Button(
            ctrl_frame,
            text="🎯 RUN DAILY FORECAST",
            command=self.run_predictions,
            bg="#2ecc71",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=10,
        ).pack(side="left", padx=10, pady=10)

        # --- INSTRUCTION LABEL ---
        tk.Label(
            self.frame,
            text="💡 Double-click any row to view historical evidence and cluster data.",
            font=("Arial", 8, "italic"),
            fg="#7f8c8d",
            bg="#f4f7f6",
        ).pack(anchor="w", padx=25)

        # --- RESULTS TABLE (TREEVIEW) ---
        # Columns: ID is hidden, used for database lookups on click
        cols = ("ID", "Barangay", "Street", "Primary Risk", "Confidence", "Status")
        self.tree = ttk.Treeview(self.frame, columns=cols, show="headings")

        for col in cols:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=120, anchor="center")

        # Hide the ID column
        self.tree.column("ID", width=0, stretch=tk.NO)
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        # BIND DOUBLE-CLICK EVENT
        self.tree.bind("<Double-1>", self.on_row_click)

    def on_row_click(self, event):
        """Displays the historical incidents that justify the prediction."""
        selected = self.tree.selection()
        if not selected:
            return

        row_values = self.tree.item(selected[0], "values")
        loc_id = row_values[0]
        barangay = row_values[1]

        # Fetch recent history (Limit 50 to see the most recent clusters)
        # In a real scenario, you'd filter this query by location_id directly in SQL
        all_history = get_incident_reports(limit=100)
        loc_history = [r for r in all_history if str(r[3]) == str(loc_id)]

        # --- CREATE POPUP ---
        popup = tk.Toplevel(self.frame)
        popup.title(f"Evidence Report: {barangay}")
        popup.geometry("550x400")

        header = tk.Label(
            popup,
            text=f"HISTORICAL CLUSTERS IN {barangay.upper()}",
            font=("Arial", 10, "bold"),
            pady=10,
        )
        header.pack()

        scroll = tk.Scrollbar(popup)
        scroll.pack(side="right", fill="y")

        txt = tk.Text(
            popup, padx=15, pady=15, font=("Consolas", 9), yscrollcommand=scroll.set
        )
        txt.pack(fill="both", expand=True)
        scroll.config(command=txt.yview)

        if not loc_history:
            txt.insert(
                tk.END,
                "No recent physical reports found.\nPrediction is based on Global Seasonal Patterns (Rain/Date).",
            )
        else:
            txt.insert(tk.END, f"{'DATE':<20} | {'CATEGORY':<15} | {'CONDITION'}\n")
            txt.insert(tk.END, "-" * 55 + "\n")
            for r in loc_history:
                # r[6]=ts, r[9]=cat_name, r[7]=cond
                date_str = r[6].strftime("%Y-%m-%d %H:%M")
                txt.insert(tk.END, f"{date_str:<20} | {r[9].upper():<15} | {r[7]}\n")

        txt.config(state=tk.DISABLED)

    def run_recalibration(self):
        """Triggers the Neural Network training script."""
        from predictive_model_train import recalibrate_nn_model

        recalibrate_nn_model()
        self.pm.initModel()
        messagebox.showinfo(
            "Model Updated",
            "The Neural Network has been retrained on the latest incident clusters.",
        )

    def run_predictions(self):
        """Calculates Softmax risk distribution for every Barangay."""
        self.tree.delete(*self.tree.get_children())

        # 1. Sync Time for Rolling Counts
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 2. Category Word-to-Label Map
        id_to_label = {
            1: "NO WATER",
            4: "NO WATER",
            7: "NO WATER",
            2: "LEAK",
            5: "LEAK",
            8: "LEAK",
            3: "DIRTY WATER",
            6: "DIRTY WATER",
            9: "DIRTY WATER",
        }

        # 3. Iterate through Dapitan Locations
        for loc_id, barangay, street, _, _ in locations:
            # Get real-time history from DB
            past_7d = get_rolling_counts(loc_id, now_str, days=7)

            # Get the Softmax Report from the PM {cat_id: probability}
            # Passing 0.0 as mock rainfall (connect to weather API for live rain)
            report = self.pm.get_daily_risk_report(loc_id, 0.0, past_7d)

            # 4. Determine Primary Risk (Skip ID 0: No Incident)
            top_id, top_prob = 0, 0.0
            for c_id, prob in report.items():
                if c_id != 0:
                    top_id, top_prob = c_id, prob
                    break

            # 5. Calibration of Managerial Alerts
            status = "STABLE"
            if top_prob > 65:
                status = "🚨 CRITICAL"
            elif top_prob > 35:
                status = "⚠️ HIGH RISK"
            elif top_prob > 12:
                status = "MODERATE"

            risk_name = id_to_label.get(top_id, "CLEAR")

            # 6. Insert into View
            self.tree.insert(
                "",
                "end",
                values=(
                    loc_id,
                    barangay,
                    street,
                    risk_name,
                    f"{top_prob:.2f}%",
                    status,
                ),
            )
