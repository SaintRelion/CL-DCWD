import random
from datetime import datetime, timedelta
from database.db_base import db_cursor, conn

# Import the training function from your ai folder
from ai.predictive_model_train import recalibrate_nn_model

# Dapitan Bounds
BOUNDS = {
    "north": 8.7383383,
    "south": 8.5496192,
    "east": 123.5536909,
    "west": 123.3028289,
}


def simulate_weekly_pattern(weeks=52, loc_id=None):
    """Inserts an incident every specific day for N weeks and retrains the AI."""
    today = datetime.now()
    day_name = today.strftime("%A")

    print(f"[SIM] Injecting {weeks} {day_name} incidents into history...")

    for i in range(weeks):
        # Calculate timestamp for 'i' weeks ago
        ts = today - timedelta(weeks=i)
        # Randomize the time slightly (between 8 AM and 8 PM)
        ts = ts.replace(hour=random.randint(8, 20), minute=random.randint(0, 59))

        target_loc = loc_id if loc_id else random.randint(1, 72)
        keyword_id = random.randint(1, 9)  # Randomly assign No Water, Leak, or Dirty
        lat = round(random.uniform(BOUNDS["south"], BOUNDS["north"]), 6)
        lon = round(random.uniform(BOUNDS["west"], BOUNDS["east"]), 6)

        # Using your standard database column names
        query = """
            INSERT INTO incident_reports 
            (post_id, keyword_category_id, location_id, latitude, longitude, timestamp, condition, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        db_cursor.execute(
            query,
            (-1, keyword_id, target_loc, lat, lon, ts, "High Priority", "Pending"),
        )

    conn.commit()
    print(f"[SUCCESS] {day_name} signature created. Retraining AI...")

    # --- AUTO RETRAIN ---
    recalibrate_nn_model()


def delete_weekly_pattern(months=12):
    """Wipes the day's pattern for the past N months and retrains the AI."""
    today = datetime.now()
    target_day_index = today.weekday()
    # Adjust for Postgres DOW (0=Sun, 1=Mon... 6=Sat)
    psql_dow = (target_day_index + 1) % 7

    cutoff_date = today - timedelta(days=months * 30)
    day_name = today.strftime("%A")

    query = """
        DELETE FROM incident_reports 
        WHERE EXTRACT(DOW FROM timestamp) = %s 
        AND timestamp >= %s
        AND post_id = -1
    """
    db_cursor.execute(query, (psql_dow, cutoff_date))
    conn.commit()
    print(f"[CLEANUP] Wiped {day_name} simulated data. Retraining AI...")

    # --- AUTO RETRAIN ---
    recalibrate_nn_model()


def simulate_random_history(count=500):
    """
    Spreads random incidents across the last 2 years.
    This creates 'Background Noise' for the AI to learn from.
    """
    print(f"[SIM] Injecting {count} random incidents across the last 2 years...")
    today = datetime.now()

    for i in range(count):
        # Random date within the last 730 days
        days_back = random.randint(0, 730)
        ts = today - timedelta(days=days_back)
        # Random time of day
        ts = ts.replace(hour=random.randint(0, 23), minute=random.randint(0, 59))

        target_loc = random.randint(1, 72)
        keyword_id = random.randint(1, 9)
        lat = round(random.uniform(BOUNDS["south"], BOUNDS["north"]), 6)
        lon = round(random.uniform(BOUNDS["west"], BOUNDS["east"]), 6)

        query = """
            INSERT INTO incident_reports 
            (post_id, keyword_category_id, location_id, latitude, longitude, timestamp, condition, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        db_cursor.execute(
            query, (-1, keyword_id, target_loc, lat, lon, ts, "Moderate", "Handled")
        )

    conn.commit()
    print("[SUCCESS] Background history populated. Retraining AI...")

    # Auto-train so the AI immediately incorporates the new 'Noise'
    # recalibrate_nn_model()


# simulate_random_history()
