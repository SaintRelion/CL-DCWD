import os
import joblib
import pandas as pd
import numpy as np
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")


def get_time_bin(dt):
    hour = dt.hour
    if 5 <= hour < 12:
        return 1
    if 12 <= hour < 17:
        return 2
    if 17 <= hour < 21:
        return 3
    return 4


class PredictiveModel:
    def __init__(self):
        self.per_location_models = (
            {}
        )  # { "1": {"model": Ridge, "scaler": StandardScaler}, ... }
        self.initModel()

    def initModel(self):
        """Loads the per-location isolated Ridge models from disk."""
        path = os.path.join(MODEL_DIR, "per_location_models.pkl")
        try:
            self.per_location_models = joblib.load(path)
            print(
                f"[PREDICTIVE] Loaded {len(self.per_location_models)} isolated location models."
            )
        except Exception as e:
            print(f"[ERROR] Failed to load per-location models: {e}")
            self.per_location_models = {}

    def reloadModel(self):
        """Refreshes models from disk after a retrain."""
        self.initModel()

    def get_daily_risk_report(self, location_id):
        """
        Returns peak risk percentages for the given location across all time bins.

        Returns: { 1: <no_water_%>, 2: <leak_%>, 3: <dirty_water_%> }

        Because each location has its own model trained on its own data only,
        simulating incidents at location X has ZERO effect on location Y.
        """
        loc_str = str(location_id)

        if loc_str not in self.per_location_models:
            # Location has no model (shouldn't happen after full train)
            return {1: 0.0, 2: 0.0, 3: 0.0}

        bundle = self.per_location_models[loc_str]
        model = bundle["model"]
        scaler = bundle["scaler"]

        now = datetime.now()
        current_day = now.weekday()

        peak_risks = {1: 0.0, 2: 0.0, 3: 0.0}

        for t_bin in [1, 2, 3, 4]:
            X_raw = pd.DataFrame([{"day_of_week": current_day, "time_bin": t_bin}])
            X_scaled = scaler.transform(X_raw)

            # raw_probs shape: (1, 3)  → [no_water, leak, dirty]
            raw_probs = model.predict(X_scaled)[0]

            for i, p in enumerate(raw_probs):
                pct = round(max(0.0, float(p)) * 100, 2)
                category_id = i + 1
                if pct > peak_risks[category_id]:
                    peak_risks[category_id] = pct

        return peak_risks
