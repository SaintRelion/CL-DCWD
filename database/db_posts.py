from database.db_incident_reports import update_incident_report
from database.db_base import db_cursor, conn


def get_posts(status_filter="All", limit=None):
    query = "SELECT id, raw_post_text, status, location_id, latitude, longitude, nlp_intent, nlp_score FROM posts WHERE 1=1"
    params = []

    if status_filter != "All":
        query += " AND status = %s"
        params.append(status_filter)

    query += " ORDER BY scraper_init DESC, date_scraped DESC"
    if limit:
        query += " LIMIT %s"
        params.append(limit)

    db_cursor.execute(query, tuple(params))
    return db_cursor.fetchall()


def insert_post(post, intent, score, status, location_row=None, scraper_init=None):
    db_cursor.execute("SELECT id FROM posts WHERE raw_post_text=%s;", (post,))
    row = db_cursor.fetchone()
    if row:
        return row[0]

    location_id = location_row.get("id") if location_row else None
    latitude = location_row.get("latitude") if location_row else None
    longitude = location_row.get("longitude") if location_row else None

    db_cursor.execute(
        """
        INSERT INTO posts
        (raw_post_text, nlp_intent, nlp_score, date_scraped, status, location_id, latitude, longitude, scraper_init)
        VALUES (%s, %s, %s, NOW(), %s, %s, %s, %s, %s)
        RETURNING id
        """,
        (post, intent, score, status, location_id, latitude, longitude, scraper_init),
    )

    post_id = db_cursor.fetchone()[0]
    conn.commit()
    print(f"[DB] Inserted new post (id={post_id})")
    return post_id


def update_post_operator(
    post_id, post_text, status=None, condition=None, location_row=None, intent_word=None
):
    updates = []
    params = []

    if status is not None:
        updates.append("status=%s")
        params.append(status)

    if updates:
        updates.append("location_id=%s")
        params.append(location_row["id"])
        updates.append("latitude=%s")
        params.append(location_row["latitude"])
        updates.append("longitude=%s")
        params.append(location_row["longitude"])

    if updates:
        sql = f"UPDATE posts SET {', '.join(updates)} WHERE id=%s"
        params.append(post_id)
        try:
            db_cursor.execute(sql, tuple(params))
            conn.commit()  # Save Post update
        except Exception as e:
            conn.rollback()
            print(f"[Error] Failed to update post: {e}")

    # Now update incident_reports accordingly
    if status is not None or condition is not None:
        update_incident_report(
            post_id, post_text, status, condition, location_row, intent_word
        )
