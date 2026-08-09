import sqlite3


def get_user(username: str):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = '" + username + "'")
    return cursor.fetchall()
