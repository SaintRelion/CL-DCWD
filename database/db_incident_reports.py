from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Tuple
from database.db_base import db_cursor, conn


def get_rolling_counts(location_id, reference_time, days=7, group_ids=None):
    """
    Count incidents for a location in the past X days, optionally filtered by category groups.
    """
    reference_dt = datetime.strptime(reference_time, "%Y-%m-%d %H:%M:%S")
    start_dt = reference_dt - timedelta(days=days)

    sql = """
        SELECT COUNT(*) FROM incident_reports
        WHERE location_id = %s AND timestamp >= %s AND timestamp <= %s
    """
    params = [location_id, start_dt, reference_dt]

    # Add category filtering if groups are provided
    if group_ids:
        sql += f" AND keyword_category_id IN ({','.join(['%s'] * len(group_ids))})"
        params.extend(group_ids)

    db_cursor.execute(sql, tuple(params))
    count = db_cursor.fetchone()[0]
    return count


def get_incident_reports(
    limit: int = 15,
    status: str = "All",
    category: str = "All",
    offset: int = 0,
    show_test_data: bool = True,
) -> list:
    # SQL optimized to return exactly what the UI loop expects to unpack
    sql = """
    SELECT 
        ir.id, 
        ir.timestamp, 
        kc.category as category_name, 
        ir.location_id, 
        ir.street_name, 
        ir.plumber_name,
        ir.status,
        ir.remarks
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
        sql += " AND kc.category = %s"
        params.append(category)

    sql += " ORDER BY ir.timestamp DESC"

    if limit:
        sql += " LIMIT %s OFFSET %s"
        params.extend([limit, offset])

    db_cursor.execute(sql, tuple(params))
    return db_cursor.fetchall()


def open_incident_case(
    post_id: int,
    location_row: Dict[str, Any],
    intent_word: str,
    street_name: Optional[str] = None,
    plumber_name: Optional[str] = None,
) -> Optional[int]:
    """
    Opens a new case or REACTIVATES an invalidated one.
    Updates the post status to 'actual incident', syncs the location, and updates NLP intent.
    """
    # 1. Get the keyword ID for the category
    db_cursor.execute(
        "SELECT id FROM keywords WHERE category = %s LIMIT 1", (intent_word,)
    )
    res: Optional[Tuple] = db_cursor.fetchone()

    if not res:
        print(f"[Error] Category '{intent_word}' not found in DB. Cannot open case.")
        return None

    keyword_id: int = res[0]

    try:
        # 2. Update the original POST with confirmed location, 'actual incident' status, and NLP intent
        db_cursor.execute(
            """
            UPDATE posts 
            SET location_id=%s, latitude=%s, longitude=%s, status=%s, nlp_intent=%s
            WHERE id=%s
            """,
            (
                location_row["id"],
                location_row["latitude"],
                location_row["longitude"],
                "actual incident",
                intent_word,  # Saving the operator-verified problem
                post_id,
            ),
        )

        # 3. Check if an incident already exists for this post
        db_cursor.execute(
            "SELECT id FROM incident_reports WHERE post_id=%s;", (post_id,)
        )
        existing_incident: Optional[Tuple] = db_cursor.fetchone()

        if existing_incident:
            # Reactivate the existing incident and update new fields
            incident_id: int = existing_incident[0]
            db_cursor.execute(
                """
                UPDATE incident_reports 
                SET status=%s, keyword_category_id=%s, location_id=%s, street_name=%s, plumber_name=%s
                WHERE id=%s
                """,
                (
                    "Active",
                    keyword_id,
                    location_row["id"],
                    street_name,
                    plumber_name,
                    incident_id,
                ),
            )
            print(
                f"[Incident] Reactivated existing case (Incident ID: {incident_id}) for post {post_id}"
            )
        else:
            # Insert a brand new incident with new fields
            db_cursor.execute(
                """
                INSERT INTO incident_reports
                (post_id, keyword_category_id, location_id, timestamp, status, street_name, plumber_name)
                VALUES (%s, %s, %s, NOW(), %s, %s, %s)
                RETURNING id
                """,
                (
                    post_id,
                    keyword_id,
                    location_row["id"],
                    "Active",
                    street_name,
                    plumber_name,
                ),
            )
            incident_id = db_cursor.fetchone()[0]
            print(
                f"[Incident] Opened new case (Incident ID: {incident_id}) for post {post_id}"
            )

        conn.commit()
        return incident_id

    except Exception as e:
        conn.rollback()
        print(f"[Error] Failed to open/reactivate incident case: {e}")
        return None


def update_incident_status(incident_id: int, status: str, remarks: str) -> bool:
    """
    Updates an incident's status and remarks.
    If 'Invalidate', it wipes location data and reverts post status to 'non-incident'.
    """
    valid_statuses = ["Active", "Closed", "Invalidate"]
    if status not in valid_statuses:
        print(f"[Error] '{status}' is not a valid incident status.")
        return False

    # Get the associated post_id so we can update the post as well
    db_cursor.execute(
        "SELECT post_id FROM incident_reports WHERE id=%s;", (incident_id,)
    )
    incident_row: Optional[Tuple] = db_cursor.fetchone()

    if not incident_row:
        print(f"[Incident] Cannot update: no incident found with ID {incident_id}")
        return False

    post_id: int = incident_row[0]

    # Map the incident status to the corresponding post status
    # We change 'Invalidate' to map to 'non-incident' as requested
    post_status_map = {
        "Closed": "completed",
        "Invalidate": "non-incident",
        "Active": "actual incident",
    }
    post_status: str = post_status_map[status]

    try:
        # 1. Update the incident record
        db_cursor.execute(
            """
            UPDATE incident_reports 
            SET status=%s, remarks=%s 
            WHERE id=%s
            """,
            (status, remarks, incident_id),
        )

        # 2. Update the parent post
        if status == "Invalidate":
            # WIPE location data if invalidated
            db_cursor.execute(
                """
                UPDATE posts 
                SET status=%s, location_id=NULL, latitude=NULL, longitude=NULL
                WHERE id=%s
                """,
                (post_status, post_id),
            )
        else:
            # Normal status update (Closed or Active)
            db_cursor.execute(
                """
                UPDATE posts 
                SET status=%s 
                WHERE id=%s
                """,
                (post_status, post_id),
            )

        conn.commit()
        print(
            f"[Incident] Updated incident {incident_id} to '{status}'. Synced post {post_id} to '{post_status}'."
        )
        return True

    except Exception as e:
        conn.rollback()
        print(f"[Error] Failed to update incident status and sync post: {e}")
        return False
