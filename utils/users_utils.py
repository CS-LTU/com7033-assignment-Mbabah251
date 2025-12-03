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


def validate_if_user_exist(email):
    """
    Validate if email exist in the database
    """
    try:        
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        # Check if user already exists in User table by email
        cursor.execute('''
        SELECT 1
        FROM users
        WHERE email = ?
        ''', (email,))
        if cursor.fetchone():
            raise ValueError('Email already registered. Please use a different email')
            
    finally:
        conn.close()