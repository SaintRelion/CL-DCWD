import os
import joblib
import pandas as pd
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
        self.index_to_cat = {}  # { 0: "dirty water", 1: "leak", 2: "no water" }

    def initModel(self):
        """Loads the per-location isolated Ridge models and category mapping from disk."""
        try:
            self.per_location_models = joblib.load(
                os.path.join(MODEL_DIR, "per_location_models.pkl")
            )
            self.index_to_cat = joblib.load(os.path.join(MODEL_DIR, "index_to_cat.pkl"))
            print(
                f"[PREDICTIVE] Loaded {len(self.per_location_models)} isolated location models "
                f"with categories: {list(self.index_to_cat.values())}"
            )
        except Exception as e:
            print(f"[ERROR] Failed to load model files: {e}")
            self.per_location_models = {}
            self.index_to_cat = {}

    def reloadModel(self):
        self.initModel()

    def get_daily_risk_report(self, location_id):
        loc_str = str(location_id)

        if loc_str not in self.per_location_models or not self.index_to_cat:
            return (
                {cat: 0.0 for cat in self.index_to_cat.values()}
                if self.index_to_cat
                else {}
            )

        bundle = self.per_location_models[loc_str]
        model = bundle["model"]
        scaler = bundle["scaler"]

        now = datetime.now()
        current_day = now.weekday()

        peak_risks = {cat: 0.0 for cat in self.index_to_cat.values()}

        for t_bin in [1, 2, 3, 4]:
            X_raw = pd.DataFrame([{"day_of_week": current_day, "time_bin": t_bin}])
            X_scaled = scaler.transform(X_raw)

            raw_probs = model.predict(X_scaled)[0]

            for i, p in enumerate(raw_probs):
                pct = round(max(0.0, float(p)) * 100, 2)
                cat_name = self.index_to_cat[i]
                if pct > peak_risks[cat_name]:
                    peak_risks[cat_name] = pct

        return peak_risks
