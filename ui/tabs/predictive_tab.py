import tkinter as tk
from tkinter import ttk
from datetime import datetime

from predictive_model_train import recalibrateRFC
from database.db_locations import locations
from database.db_incident_reports import get_rolling_counts
from database.db_keywords import category_dict


class PredictiveTab:

    def __init__(self, parent, pm):

        self.pm = pm

        self.frame = tk.Frame(parent)

        tk.Label(self.frame, text="Predictive Model", font=("Arial", 18)).pack(
            anchor="w"
        )

        categories = sorted({cat for cats in category_dict.values() for cat in cats})

        self.category_var = tk.StringVar(value=categories[0])

        ttk.Combobox(
            self.frame, textvariable=self.category_var, values=categories
        ).pack(anchor="w")

        tk.Button(
            self.frame, text="Run Predictions", command=self.run_predictions
        ).pack(pady=10)

        self.results_box = tk.Text(self.frame, height=20)
        self.results_box.pack(fill="both", expand=True)

    def run_predictions(self):

        recalibrateRFC()
        self.pm.initModel()

        category = self.category_var.get()

        self.results_box.delete("1.0", tk.END)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for id, barangay, street, _, _ in locations:

            past_7d = get_rolling_counts(id, now, 7)
            past_30d = get_rolling_counts(id, now, 30)

            prob = self.pm.predictIncidentProbability(
                category=category,
                location_id=id,
                timestamp=now,
                past_7d=past_7d,
                past_30d=past_30d,
            )

            percent = prob * 100

            self.results_box.insert(
                tk.END, f"{barangay} - {street} => {percent:.2f}%\n"
            )
