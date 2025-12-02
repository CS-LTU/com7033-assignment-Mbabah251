from flask import session
import sqlite3



def get_current_user():
    """
    Retrieve the currently logged-in user's information from the database
    based on the user_id stored in the session.
    Returns user data as a dictionary or None if not logged in.
    """
   
    user_id = session.get("user_id")
    if not user_id:
        return None

    conn = sqlite3.connect('hospital.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    return dict(user) if user else None