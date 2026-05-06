import random
from datetime import datetime, timedelta
from database.db_base import db_cursor, conn
from database.db_locations import location_dict
from database.db_users import get_all_tubero_names

# Import the training function from your ai folder
from ai.predictive_model_train import recalibrate_nn_model


def get_valid_ids(table_name):
    """Fetches all existing IDs from a specified table to ensure FK integrity."""
    db_cursor.execute(f"SELECT id FROM {table_name}")
    return [row[0] for row in db_cursor.fetchall()]


def simulate_historical_data(count=100):
    """
    Injects random incidents into history using original post_id offset logic.
    """
    print(f"[SIM] Initializing simulation constraints...")

    # 1. Fetch valid IDs to avoid ForeignKeyViolation
    valid_keywords = get_valid_ids("keywords")
    valid_locations = list(location_dict.keys())
    tuberos = get_all_tubero_names()

    if not valid_keywords:
        print("[ERROR] No keywords found in database. Simulation aborted.")
        return

    today = datetime.now()
    common_post_pool = [10, 20, 30, 40, 50]

    print(f"[SIM] Injecting {count} incidents with original offset logic...")

    for i in range(count):
        # --- ORIGINAL POST_ID LOGIC ---
        if random.random() < 0.15:
            post_id = random.choice(common_post_pool)
        else:
            base_offset = 4
            avg_gap = 3
            post_id = base_offset + (i * avg_gap) + random.randint(1, 10)

        # --- TIMESTAMP LOGIC ---
        days_back = random.randint(0, 90)
        ts = today - timedelta(days=days_back)
        ts = ts.replace(hour=random.randint(0, 23), minute=random.randint(0, 59))

        # --- DYNAMIC FK SELECTION ---
        # Pick from actual IDs found in your DB
        keyword_id = random.choice(valid_keywords)
        loc_id = random.choice(valid_locations)

        # --- WORKFLOW DATA ---
        plumber = random.choice(tuberos) if tuberos else "System Simulated"
        status = "Closed" if random.random() > 0.4 else "Active"
        remarks = "" if status == "Closed" else ""

        query = """
            INSERT INTO incident_reports 
            (post_id, keyword_category_id, location_id, street_name, 
             plumber_name, timestamp, status, remarks)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        try:
            db_cursor.execute(
                query, (post_id, keyword_id, loc_id, "", plumber, ts, status, remarks)
            )
        except Exception as e:
            print(f"[ERR] Iteration {i} failed: {e}")
            conn.rollback()
            continue

    conn.commit()
    print("[SIM] Commit successful. Retraining AI predictive models...")
    recalibrate_nn_model()
    print("[SIM] Completed.")


if __name__ == "__main__":
    simulate_historical_data()
