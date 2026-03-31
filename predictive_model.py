import os
import pandas as pd
import joblib
from datetime import datetime

# Path Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")


class PredictiveModel:
    def initModel(self):
        """Loads the Neural Network, Scaler, and Feature list."""
        try:
            self.model = joblib.load(os.path.join(MODEL_DIR, "nn_incident_model.pkl"))
            self.scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
            self.feature_columns = joblib.load(
                os.path.join(MODEL_DIR, "feature_columns.pkl")
            )
            print("[PREDICTIVE] Neural Network and Scaler loaded successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to load model files: {e}")

    def get_daily_risk_report(self, location_id, rainfall, past_7d):
        """
        Calculates the probability spread for a specific location.
        Returns: A sorted dictionary of {category_id: probability_percentage}
        """
        now = datetime.now()

        # Prepare the input matching our 'KOS' features:
        # ["loc_id", "day_of_week", "month", "rainfall", "past_7d"]
        feature_row = pd.DataFrame(
            [
                {
                    "loc_id": location_id,
                    "day_of_week": now.weekday(),
                    "month": now.month,
                    "rainfall": rainfall,
                    "past_7d": past_7d,
                }
            ]
        )[self.feature_columns]

        # 1. Scale the data (Mandatory for Neural Networks)
        X_scaled = self.scaler.transform(feature_row)

        # 2. Get Softmax probabilities
        probs = self.model.predict_proba(X_scaled)[0]
        classes = self.model.classes_

        # 3. Build a report of all risks > 0.1%
        risk_report = {}
        for idx, class_id in enumerate(classes):
            percentage = probs[idx] * 100
            if percentage > 0.1:
                risk_report[int(class_id)] = round(percentage, 2)

        # Sort by highest risk first
        return dict(sorted(risk_report.items(), key=lambda item: item[1], reverse=True))
