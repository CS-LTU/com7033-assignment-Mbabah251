from flask import session
import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = "hospital.db"


def insert_user(first_name, last_name, email, password, role):
    """
    Insert a new user (Doctor / Nurse / Patient etc.) into the users table.
    Password is hashed here before saving.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    password_hash = generate_password_hash(password)

    cursor.execute(
        """
        INSERT INTO users (first_name, last_name, email, password_hash, role)
        VALUES (?, ?, ?, ?, ?)
        """,
        (first_name, last_name, email, password_hash, role),
    )

    conn.commit()
    conn.close()


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


def validate_if_email_exist(email):
    """
    Validate if email exists in either the users or patients table.
    Raises ValueError if email already registered.
    """
    try:
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()

        # Check users table
        cursor.execute("""
            SELECT 1 FROM users WHERE email = ?
        """, (email,))
        if cursor.fetchone():
            raise ValueError("Email already registered in users table. Please use a different email.")

        # Check patients table
        cursor.execute("""
            SELECT 1 FROM patients WHERE email = ?
        """, (email,))
        if cursor.fetchone():
            raise ValueError("Email already registered as a patient. Please use a different email.")

    finally:
        conn.close()
