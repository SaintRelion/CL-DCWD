import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="dcwd_incidents",
    user="postgres",
    password="postgres",
    port=5433,
)

db_cursor = conn.cursor()
