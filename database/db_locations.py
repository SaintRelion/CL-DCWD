from database.db_base import db_cursor

db_cursor.execute("SELECT id, barangay, street, latitude, longitude FROM locations;")
locations = db_cursor.fetchall()
location_dict = {
    row[0]: {
        "barangay": row[1],
        "street": row[2],
        "latitude": row[3],
        "longitude": row[4],
    }
    for row in locations
}


def get_location_by_id(location_id):
    query = """
        SELECT id, barangay, street, latitude, longitude
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
            "street": row[2],
            "latitude": row[3],
            "longitude": row[4],
        }
    return None
