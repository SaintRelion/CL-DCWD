import random
import requests
from datetime import datetime, timedelta
from database.db_base import db_cursor, conn

# --- Configuration ---
N_ROWS = 1000
# Dapitan Bounds
BOUNDS = {
    "north": 8.7383383,
    "south": 8.5496192,
    "east": 123.5536909,
    "west": 123.3028289,
}


def simulate_data():
    print(f"[SIM] Starting simulation for {N_ROWS} records in Dapitan...")

    for i in range(N_ROWS):
        post_id = -1  # Indicates simulated data
        keyword_id = random.randint(1, 9)
        location_id = random.randint(1, 72)

        lat = round(random.uniform(BOUNDS["south"], BOUNDS["north"]), 6)
        lon = round(random.uniform(BOUNDS["west"], BOUNDS["east"]), 6)

        # Random Timestamp (Last 2 Years)
        days_back = random.randint(0, 730)
        hour = random.randint(0, 23)
        ts = datetime.now() - timedelta(days=days_back, hours=hour)

        # --- PATTERN INJECTION (Making the AI Smarter) ---

        # "Weather Bias": Simulating heavy rain effect
        # Simulate that 30% of incidents are "Rain-Triggered"
        is_rainy = random.random() < 0.3

        # B. Cluster Bias: 50% of incidents result in a follow-up (Leaky pipes)
        is_cluster = random.random() < 0.50

        # Insert Primary Incident
        insert_incident(post_id, keyword_id, location_id, lat, lon, ts)

        # If it's a storm or a cluster, we add more related data
        if is_cluster:
            # Same location, 2-24 hours later
            follow_up_ts = ts + timedelta(hours=random.randint(2, 23))
            insert_incident(-1, keyword_id, location_id, lat, lon, follow_up_ts)

        if is_rainy:
            # Random location, same day (Simulating city-wide pressure/rain stress)
            storm_ts = ts + timedelta(hours=random.randint(1, 5))
            insert_incident(
                -1, random.randint(1, 9), random.randint(1, 72), lat, lon, storm_ts
            )

        if i % 250 == 0:
            conn.commit()
            print(f"[DB] Progress: {i}/{N_ROWS} rows inserted.")

    conn.commit()
    print("[DB] Simulation Complete.")


def insert_incident(pid, kid, lid, lat, lon, ts):
    db_cursor.execute(
        """
        INSERT INTO incident_reports 
        (post_id, keyword_category_id, location_id, latitude, longitude, timestamp, condition, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            pid,
            kid,
            lid,
            lat,
            lon,
            ts,
            "High Priority" if random.random() > 0.8 else "Low",
            "Handled",
        ),
    )


if __name__ == "__main__":
    simulate_data()
