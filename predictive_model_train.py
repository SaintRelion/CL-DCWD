import os
import joblib
import pandas as pd
import numpy as np
import requests
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from tqdm import tqdm
from database.db_incident_reports import get_incident_reports


def fetch_weather_bulk(df):
    """Fetches daily rainfall for all unique dates in the dataset."""
    unique_dates = df["ts"].dt.date.unique()
    start_date = min(unique_dates)
    end_date = max(unique_dates)

    # Using Open-Meteo Archive API (No API Key needed)
    # Using Dapitan center coordinates
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude=8.6440&longitude=123.4283&"
        f"start_date={start_date}&end_date={end_date}&"
        f"daily=rain_sum&timezone=Asia%2FSingapore"
    )

    try:
        print(f"[API] Fetching weather from {start_date} to {end_date}...")
        res = requests.get(url).json()
        daily_data = res.get("daily", {})
        weather_map = dict(
            zip(daily_data.get("time", []), daily_data.get("rain_sum", []))
        )

        # Map back to the dataframe (convert date to string to match JSON keys)
        df["rainfall"] = df["ts"].dt.strftime("%Y-%m-%d").map(weather_map).fillna(0)
    except Exception as e:
        print(f"Weather API failed: {e}. Defaulting to 0mm rain.")
        df["rainfall"] = 0
    return df


def recalibrate_model():
    records = get_incident_reports()
    if not records:
        return

    columns = ["id", "post_id", "cat_id", "loc_id", "lat", "lon", "ts", "cond", "stat"]
    df = pd.DataFrame(records, columns=columns)
    df["ts"] = pd.to_datetime(df["ts"])
    df = df.sort_values("ts")

    # 1. Weather Integration
    df = fetch_weather_bulk(df)
    df["hour"] = df["ts"].dt.hour
    df["day_of_week"] = df["ts"].dt.dayofweek

    df["ts"] = df["ts"] + pd.to_timedelta(df.groupby("ts").cumcount(), unit="us")
    df = df.set_index("ts").sort_index()

    df["past_7d"] = (
        df.groupby("loc_id")["id"].rolling("7D").count().reset_index(level=0, drop=True)
    )
    df = df.reset_index()

    # MULTI-CLASS LABEL CREATION
    df["y"] = 0  # Default: No Incident
    for i in range(len(df) - 1):
        if df.loc[i, "loc_id"] == df.loc[i + 1, "loc_id"]:
            diff = (df.loc[i + 1, "ts"] - df.loc[i, "ts"]).total_seconds()
            if diff <= 86400:
                # Instead of 1, we store the ACTUAL category ID of the next incident
                df.loc[i, "y"] = df.loc[i + 1, "cat_id"]

    ## TRAINING
    features = ["loc_id", "hour", "day_of_week", "rainfall", "past_7d"]
    X = df[features]
    y = df["y"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # The Random Forest
    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        n_jobs=-1,
        random_state=42,
        class_weight="balanced",  # Tells AI that '1' is more important than '0'
    )

    print(
        f"[TRAIN] Training Multi-class model on {len(df['y'].unique())} categories..."
    )
    rf.fit(X_train, y_train)

    # Diagnostics
    preds = rf.predict(X_test)
    print(f"Overall Accuracy: {accuracy_score(y_test, preds):.2%}")
    # This will now show a breakdown for every Category ID
    print(classification_report(y_test, preds, zero_division=0))

    # Saving
    model_dir = os.path.join(os.path.dirname(__file__), "models")
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(rf, os.path.join(model_dir, "rf_multi_model.pkl"))
    joblib.dump(features, os.path.join(model_dir, "feature_columns.pkl"))
    print("Model and Features saved successfully.")


if __name__ == "__main__":
    recalibrate_model()
