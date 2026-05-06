from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from database.db_base import db_cursor, conn


def get_posts(status_filter="All", limit=None):
    query: str = """
        SELECT p.id, p.raw_post_text, p.username, p.profile_link, p.date_scraped, 
               p.status, p.location_id, p.latitude, p.longitude, p.nlp_intent, 
               p.scraper_init, ir.id as incident_id
        FROM posts p
        LEFT JOIN incident_reports ir ON p.id = ir.post_id
        WHERE 1=1
    """
    params: List[Any] = []

    if status_filter != "All":
        query += " AND status = %s"
        params.append(status_filter)

    query += " ORDER BY scraper_init DESC, date_scraped DESC"
    if limit:
        query += " LIMIT %s"
        params.append(limit)

    db_cursor.execute(query, tuple(params))
    return db_cursor.fetchall()


def insert_post(
    post: str,
    username: str,
    profile_link: str,
    intent: str,
    status: str,
    location_row: Optional[Dict[str, Any]] = None,
    scraper_init: Optional[datetime] = None,
):

    db_cursor.execute("SELECT id FROM posts WHERE raw_post_text=%s;", (post,))
    row: Optional[Tuple] = db_cursor.fetchone()
    if row:
        return row[0]

    location_id: Optional[int] = location_row.get("id") if location_row else None
    latitude: Optional[float] = location_row.get("latitude") if location_row else None
    longitude: Optional[float] = location_row.get("longitude") if location_row else None

    db_cursor.execute(
        """
        INSERT INTO posts
        (raw_post_text, username, profile_link, date_scraped, status, location_id, latitude, longitude, nlp_intent, scraper_init)
        VALUES (%s, %s, %s, NOW(), %s, %s, %s, %s, %s, %s)
        RETURNING id
        """,
        (
            post,
            username,
            profile_link,
            status,
            location_id,
            latitude,
            longitude,
            intent,
            scraper_init,
        ),
    )

    post_id: int = db_cursor.fetchone()[0]
    conn.commit()
    print(f"[DB] Inserted new post (id={post_id})")
    return post_id


def update_post_operator(
    post_id: int,
    status: Optional[str] = None,
    location_row: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Updates the post details (like location corrections or marking a post as reviewed).
    NOTE: This no longer automatically creates or updates an incident.
    """
    updates: List[str] = []
    params: List[Any] = []

    if status is not None:
        updates.append("status=%s")
        params.append(status)

    if location_row is not None:
        updates.append("location_id=%s")
        params.append(location_row["id"])
        updates.append("latitude=%s")
        params.append(location_row["latitude"])
        updates.append("longitude=%s")
        params.append(location_row["longitude"])

    if updates:
        sql: str = f"UPDATE posts SET {', '.join(updates)} WHERE id=%s"
        params.append(post_id)
        try:
            db_cursor.execute(sql, tuple(params))
            conn.commit()
            print(f"[DB] Successfully updated post {post_id}")
        except Exception as e:
            conn.rollback()
            print(f"[Error] Failed to update post: {e}")
