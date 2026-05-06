from database.db_base import db_cursor

db_cursor.execute("SELECT id, barangay, latitude, longitude FROM locations;")
locations = db_cursor.fetchall()

location_dict = {
    row[0]: {
        "barangay": row[1],
        "latitude": row[2],
        "longitude": row[3],
    }
    for row in locations
}


def get_location_by_id(location_id):
    query: str = """
        SELECT id, barangay, latitude, longitude
        FROM locations
        WHERE id = %s
        LIMIT 1;
    """

    db_cursor.execute(query, (location_id,))
    row = db_cursor.fetchone()

    if row:
        return {
            "id": row[0],
            "barangay": row[1],
            "latitude": row[2],
            "longitude": row[3],
        }
    return None
