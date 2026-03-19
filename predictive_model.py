import os
import pandas as pd
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")
model_path = os.path.join(MODEL_DIR, "rf_incident_model.pkl")
features_path = os.path.join(MODEL_DIR, "feature_columns.pkl")


class PredictiveModel:
    def initModel(self):
        self.rf = joblib.load(model_path)
        self.feature_columns = joblib.load(features_path)

    def predictIncidentProbability(
        self, category, location_id, timestamp, past_7d=0, past_30d=0
    ):
        # category_id = None
        # for c_id, categories in category_dict.items():
        #     if category.lower() in categories:
        #         category_id = c_id
        #         break
        # if category_id is None:
        #     raise ValueError(f"Category '{category}' not found in category_dict")

        # ts = pd.to_datetime(timestamp)
        # day_of_week = ts.dayofweek
        # week = ts.isocalendar().week
        # month = ts.month
        # year = ts.year

        # feature_row = {
        #     "keyword_id": category_id,
        #     "location_id": location_id,
        #     "day_of_week": day_of_week,
        #     "week": week,
        #     "month": month,
        #     "year": year,
        #     "past_7d": past_7d,
        #     "past_30d": past_30d,
        # }

        # X = pd.DataFrame([feature_row])[self.feature_columns]

        # # Predict probability
        # proba = self.rf.predict_proba(X)[0]
        # if 1 in self.rf.classes_:
        #     idx = list(self.rf.classes_).index(1)
        #     return proba[idx]
        return 0.0
