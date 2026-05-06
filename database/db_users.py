from database.db_base import conn, db_cursor


def get_user(username, password):

    db_cursor.execute(
        """
        SELECT id, username, email, role
        FROM users
        WHERE username = %s AND password = %s
        """,
        (username, password),
    )

    return db_cursor.fetchone()


def register_user(username, email, password, role):

    db_cursor.execute(
        """
        INSERT INTO users (username, email, password, role)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """,
        (username, email, password, role),
    )

    user_id = db_cursor.fetchone()[0]
    conn.commit()

    return user_id


def username_exists(username):

    db_cursor.execute(
        "SELECT id FROM users WHERE username=%s",
        (username,),
    )

    return db_cursor.fetchone() is not None


def get_all_users():
    db_cursor.execute("SELECT id, username, role FROM users ORDER BY id DESC")
    return db_cursor.fetchall()


# Non Auth
def get_all_tubero_names():
    db_cursor.execute("SELECT username FROM users WHERE role = 'tubero'")
    return [row[0] for row in db_cursor.fetchall() if row[0]]
