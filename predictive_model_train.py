import os
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
import requests
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from database.db_incident_reports import get_incident_reports


def fetch_weather_bulk(df):
    """Fetches daily rainfall for all unique dates in the dataset."""
    unique_dates = df["ts"].dt.date.unique()
    start_date, end_date = min(unique_dates), max(unique_dates)
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
        df["rainfall"] = df["ts"].dt.strftime("%Y-%m-%d").map(weather_map).fillna(0)
    except:
        df["rainfall"] = 0
    return df


def recalibrate_nn_model():
    records = get_incident_reports(limit=None)
    if not records:
        print("[ERROR] No data found.")
        return

    columns = [
        "id",
        "pid",
        "cat_id",
        "loc_id",
        "lat",
        "lon",
        "ts",
        "cond",
        "stat",
        "cat_name",
    ]
    df = pd.DataFrame(records, columns=columns)
    df["ts"] = pd.to_datetime(df["ts"])
    df = df.sort_values("ts")

    # 1. Fix Duplicate Timestamps (The KOS Jitter Fix)
    # Adds 1 microsecond to each duplicate so the index is unique
    df["ts"] = df["ts"] + pd.to_timedelta(df.groupby("ts").cumcount(), unit="us")

    # 2. Weather & Feature Engineering
    df = fetch_weather_bulk(df)
    df["day_of_week"] = df["ts"].dt.dayofweek
    df["month"] = df["ts"].dt.month

    # Calculate 7-day rolling history
    df = df.set_index("ts")
    df["past_7d"] = (
        df.groupby("loc_id")["id"].rolling("7D").count().reset_index(level=0, drop=True)
    )
    df = df.reset_index()

    # 3. Label Creation (The 'Softmax' Fuel)
    # We look for ANY incident in the SAME Barangay within the NEXT 7 days
    print("[DATA] Generating labels. This might take a moment...")
    df["y"] = 0
    for i in range(len(df)):
        loc = df.loc[i, "loc_id"]
        t_start = df.loc[i, "ts"]
        t_end = t_start + pd.Timedelta(days=7)

        # Look ahead for incidents in the same location
        future = df[(df["loc_id"] == loc) & (df["ts"] > t_start) & (df["ts"] <= t_end)]

        if not future.empty:
            df.loc[i, "y"] = future.iloc[0]["cat_id"]

    print(f"[DATA] Incident distribution found:\n{df['y'].value_counts()}")

    # 4. Feature Selection & Scaling
    features = ["loc_id", "day_of_week", "month", "rainfall", "past_7d"]
    X = df[features]
    y = df["y"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 5. Neural Network (Softmax Layers)
    # MLPClassifier naturally uses Softmax for multi-class probability
    mlp = MLPClassifier(
        hidden_layer_sizes=(128, 64, 32),  # Deep brain for complex patterns
        max_iter=1000,
        activation="relu",
        solver="adam",
        alpha=0.001,  # Regularization to keep percentages fluid
        random_state=42,
    )

    print(f"[TRAIN] Feeding {len(X_scaled)} rows into Neural Network...")
    mlp.fit(X_scaled, y)

    # --- REAL-WORLD VALIDATION TESTS ---
    print("\n" + "=" * 60)
    print("   HISTORICAL DATA VALIDATION (SOFTMAX)   ")
    print("=" * 60)

    # Grab 5 random rows where an incident actually happened (y > 0)
    # and 5 where nothing happened (y = 0)
    test_rows = pd.concat(
        [
            df[df["y"] > 0].sample(min(5, len(df[df["y"] > 0]))),
            df[df["y"] == 0].sample(5),
        ]
    ).sample(
        frac=1
    )  # Shuffle them

    for _, row in test_rows.iterrows():
        actual_y = int(row["y"])

        # Prepare input exactly like training
        input_data = pd.DataFrame([row[features]], columns=features)
        scaled_input = scaler.transform(input_data)

        # Get Softmax Probabilities
        probs = mlp.predict_proba(scaled_input)[0]
        results = sorted(zip(mlp.classes_, probs), key=lambda x: x[1], reverse=True)

        print(
            f"\n>>> Historical Snapshot (Loc: {int(row['loc_id'])}, Rain: {row['rainfall']:.1f}mm)"
        )
        print(
            f"    ACTUAL OUTCOME: {'No Incident' if actual_y == 0 else f'Category {actual_y}'}"
        )

        for cat_id, prob in results:
            p = prob * 100
            if p < 0.5:
                continue  # KOS: focus on the real signal

            label = "No Incident" if cat_id == 0 else f"Category {cat_id}"
            color = "🟢" if cat_id == actual_y else "⚪"
            bar = "■" * int(p / 5)
            print(f"    {color} {label:15} | {p:6.2f}% {bar}")

    # 7. Save Models
    model_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(mlp, os.path.join(model_dir, "nn_incident_model.pkl"))
    joblib.dump(scaler, os.path.join(model_dir, "scaler.pkl"))
    joblib.dump(features, os.path.join(model_dir, "feature_columns.pkl"))


if __name__ == "__main__":
    recalibrate_nn_model()
