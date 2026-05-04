import os
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from database.db_incident_reports import get_incident_reports

# ---------------------------------------------------------------------------
# ARCHITECTURE: One Ridge regression model per location (72 models).
# Each model is trained ONLY on data from its own location_id plus its own
# silence baseline.  No location can ever bleed into another.
# ---------------------------------------------------------------------------

NUM_LOCATIONS = 72


def get_time_bin(dt):
    hour = dt.hour
    if 5 <= hour < 12:
        return 1
    if 12 <= hour < 17:
        return 2
    if 17 <= hour < 21:
        return 3
    return 4


def get_group(cid):
    if cid in [1, 4, 7]:
        return 0  # No Water
    if cid in [2, 5, 8]:
        return 1  # Leak
    if cid in [3, 6, 9]:
        return 2  # Dirty Water
    return -1


def _build_silence_for_location():
    """Returns X (28 rows × 2 features) and Y (28 × 3) of all-zero targets."""
    rows = []
    for day in range(7):
        for t_bin in [1, 2, 3, 4]:
            rows.append({"day_of_week": day, "time_bin": t_bin})
    X = pd.DataFrame(rows)
    Y = np.zeros((len(X), 3))
    return X, Y


def recalibrate_nn_model():
    records = get_incident_reports(limit=None)
    columns = [
        "id",
        "pid",
        "cat_id",
        "loc_id",
        "lat",
        "lon",
        "ts",
        "t1",
        "t2",
        "cat_name",
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

    # Pre-process incident rows
    df_all["target_idx"] = df_all["cat_id"].apply(get_group)
    df_incidents_all = df_all[df_all["target_idx"] != -1].copy()
    df_incidents_all["day_of_week"] = df_incidents_all["ts"].dt.dayofweek
    df_incidents_all["time_bin"] = df_incidents_all["ts"].apply(get_time_bin)
    df_incidents_all["loc_id"] = df_incidents_all["loc_id"].astype(str)

    model_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    os.makedirs(model_dir, exist_ok=True)

    per_location_models = {}  # { loc_id_str: {"model": ..., "scaler": ...} }

    for loc in range(1, NUM_LOCATIONS + 1):
        loc_str = str(loc)

        # --- Incident rows for THIS location only ---
        df_loc = df_incidents_all[df_incidents_all["loc_id"] == loc_str]

        X_inc = df_loc[["day_of_week", "time_bin"]].copy()
        Y_inc = np.zeros((len(df_loc), 3))
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

    # --- Trend data (unchanged) ---
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
