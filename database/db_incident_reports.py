from datetime import datetime, timedelta
from database.db_base import db_cursor, conn


def get_rolling_counts(location_id, reference_time, days=7):
    """
    Count number of incidents for a location in the past `days` days up to `reference_time`.
    """
    reference_dt = datetime.strptime(reference_time, "%Y-%m-%d %H:%M:%S")
    start_dt = reference_dt - timedelta(days=days)

    db_cursor.execute(
        """
        SELECT COUNT(*) FROM incident_reports
        WHERE location_id = %s AND timestamp >= %s AND timestamp <= %s
        """,
        (location_id, start_dt, reference_dt),
    )
    count = db_cursor.fetchone()[0]
    return count


def get_incident_reports(
    limit=15,
    status="All",
    category="All",
    condition="All",
    offset=0,
    show_test_data: bool = True,
):
    # Base query with a JOIN to handle filtering by category name
    sql = """
    SELECT ir.id, ir.post_id, ir.keyword_category_id, ir.location_id, 
           ir.latitude, ir.longitude, ir.timestamp, ir.condition, ir.status,
           kc.word as category_name
    FROM incident_reports ir
    LEFT JOIN keywords kc ON ir.keyword_category_id = kc.id
    WHERE 1=1
    """
    params = []

    if not show_test_data:
        sql += " AND ir.post_id != -1"

    if status != "All":
        sql += " AND ir.status = %s"
        params.append(status)

    if category != "All":
        sql += " AND kc.category = %s"  # Filter by the category group name
        params.append(category)

    if condition != "All":
        sql += " AND ir.condition = %s"
        params.append(condition)

    sql += " ORDER BY ir.timestamp DESC"

    if limit:
        sql += " LIMIT %s OFFSET %s"
        params.extend([limit, offset])

    db_cursor.execute(sql, tuple(params))
    return db_cursor.fetchall()


def update_incident_report(
    post_id, post_text, operator_status, condition, location_row, intent_word
):
    # Check if post already has an incident report
    db_cursor.execute("SELECT id FROM incident_reports WHERE post_id=%s;", (post_id,))
    incident_row = db_cursor.fetchone()

    if operator_status == "Actual Incident":
        # --- THE FIX: Get the ID from the category name we already have ---
        db_cursor.execute(
            "SELECT id FROM keywords WHERE category = %s LIMIT 1", (intent_word,)
        )
        res = db_cursor.fetchone()

        if not res:
            print(f"[Error] Category '{intent_word}' not found in DB.")
            return

        keyword_id = res[0]  # This is the numerical ID

        if location_row is None:
            print(f"[Incident] Skipping: No location selected for post {post_id}")
            return

        if incident_row:
            # Update existing incident
            db_cursor.execute(
                """UPDATE incident_reports 
                       SET condition=%s, location_id=%s, latitude=%s, longitude=%s 
                       WHERE post_id=%s""",
                (
                    condition,
                    location_row["id"],
                    location_row["latitude"],
                    location_row["longitude"],
                    post_id,
                ),
            )
            print(f"[Incident] Updated incident for post {post_id}")
        else:
            # Insert new incident
            db_cursor.execute(
                """
                    INSERT INTO incident_reports
                    (post_id, keyword_category_id, location_id, latitude, longitude, timestamp, condition, status)
                    VALUES (%s, %s, %s, %s, %s, NOW(), %s, %s)
                    """,
                (
                    post_id,
                    keyword_id,
                    location_row["id"],
                    location_row["latitude"],
                    location_row["longitude"],
                    condition,
                    "Pending",
                ),
            )
            print(f"[Incident] Inserted incident for post {post_id}")

        conn.commit()


def update_incident_tubero(post_id, status):
    # Make sure an incident exists
    db_cursor.execute("SELECT id FROM incident_reports WHERE post_id=%s;", (post_id,))
    incident = db_cursor.fetchone()
    if incident:
        db_cursor.execute(
            "UPDATE incident_reports SET status=%s WHERE post_id=%s",
            (status, post_id),
        )
        conn.commit()

        if db_cursor.rowcount > 0:
            print(f"[Incident] Updated status for post {post_id}")
            return True
        else:
            print(f"[Incident] No record found for post {post_id}")
            return False
    else:
        print(f"[Incident] Cannot update status: no incident for post {post_id}")
