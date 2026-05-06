import os
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from database.db_incident_reports import get_incident_reports
from database.db_keywords import keyword_dict
from database.db_locations import location_dict

id_to_category = {v: k for k, v in keyword_dict.items()}
sorted_categories = sorted(id_to_category.values())  # stable alphabetical order
cat_to_index = {cat: i for i, cat in enumerate(sorted_categories)}
index_to_cat = {i: cat for cat, i in cat_to_index.items()}
NUM_CATEGORIES = len(cat_to_index)

NUM_LOCATIONS = len(location_dict)


def get_time_bin(dt):
    hour = dt.hour
    if 5 <= hour < 12:
        return 1
    if 12 <= hour < 17:
        return 2
    if 17 <= hour < 21:
        return 3
    return 4


def _build_silence_for_location():
    """Returns X (28 rows x 2 features) and Y (28 x NUM_CATEGORIES) of all-zero targets."""
    rows = []
    for day in range(7):
        for t_bin in [1, 2, 3, 4]:
            rows.append({"day_of_week": day, "time_bin": t_bin})
    X = pd.DataFrame(rows)
    Y = np.zeros((len(X), NUM_CATEGORIES))
    return X, Y


def recalibrate_nn_model():
    records = get_incident_reports(limit=None)
    columns = [
        "id",
        "ts",
        "cat_name_db",  # This is the category name from the JOIN
        "loc_id",
        "street_name",
        "plumber_name",
        "status",
    ]

    if not records:
        print(
            "[TRAIN] Database empty – training silence-only models for all locations."
        )
        df_all = pd.DataFrame(columns=columns)
        df_all["ts"] = pd.to_datetime(df_all["ts"])
        total_weeks = 52
    else:
        df_all = pd.DataFrame(records, columns=columns)
        df_all["ts"] = pd.to_datetime(df_all["ts"])
        oldest_date = df_all["ts"].min()
        total_weeks = max(1, (datetime.now() - oldest_date).days // 7)

    df_all["cat_name_mapped"] = df_all["cat_name_db"].str.lower().str.replace(" ", "_")
    df_all["target_idx"] = df_all["cat_name_mapped"].map(cat_to_index)
    df_incidents_all = df_all[df_all["target_idx"].notna()].copy()
    df_incidents_all["target_idx"] = df_incidents_all["target_idx"].astype(int)
    df_incidents_all["day_of_week"] = df_incidents_all["ts"].dt.dayofweek
    df_incidents_all["time_bin"] = df_incidents_all["ts"].apply(get_time_bin)
    df_incidents_all["loc_id"] = df_incidents_all["loc_id"].astype(str)

    model_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    os.makedirs(model_dir, exist_ok=True)

    per_location_models = {}

    for loc in location_dict.keys():
        loc_str = str(loc)

        # --- Incident rows for THIS location only ---
        df_loc = df_incidents_all[df_incidents_all["loc_id"] == loc_str]

        X_inc = df_loc[["day_of_week", "time_bin"]].copy()
        Y_inc = np.zeros((len(df_loc), NUM_CATEGORIES))
        for i, idx in enumerate(df_loc["target_idx"]):
            Y_inc[i, int(idx)] = 1.0

        # --- Silence baseline for THIS location ---
        X_sil, Y_sil = _build_silence_for_location()

        # --- Combine ---
        X_combined = pd.concat([X_inc, X_sil], ignore_index=True)
        Y_combined = np.vstack([Y_inc, Y_sil])

        # Sample weights: silence rows count as 'total_weeks' incidents
        weights = np.ones(len(X_combined))
        weights[len(X_inc) :] = total_weeks

        # --- Fit a fresh scaler per location (avoids cross-contamination) ---
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_combined)

        # Ridge with alpha=1 – linear, stable, no hidden layers
        model = Ridge(alpha=1.0, fit_intercept=True)
        model.fit(X_scaled, Y_combined, sample_weight=weights)

        per_location_models[loc_str] = {"model": model, "scaler": scaler}

    # --- Persist ---
    joblib.dump(per_location_models, os.path.join(model_dir, "per_location_models.pkl"))
    joblib.dump(index_to_cat, os.path.join(model_dir, "index_to_cat.pkl"))

    # --- Trend data ---
    if not df_incidents_all.empty:
        trend_summary = (
            df_incidents_all.groupby(
                ["loc_id", pd.Grouper(key="ts", freq="W-MON"), "target_idx"]
            )
            .size()
            .reset_index(name="count")
        )
    else:
        trend_summary = pd.DataFrame()
    joblib.dump(trend_summary, os.path.join(model_dir, "trend_data.pkl"))

    print(
        f"[SUCCESS] {NUM_LOCATIONS} isolated Ridge models trained "
        f"({total_weeks}-week baseline). Zero cross-location bleed."
    )


if __name__ == "__main__":
    recalibrate_nn_model()
