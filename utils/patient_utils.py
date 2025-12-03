
import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = "hospital.db"


def insert_patient(
    first_name,
    last_name,
    date_of_birth,
    gender,
    email,
    password,
):
    """
    Insert a new patient into the patients table.
    Password is hashed here before saving.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    password_hash = generate_password_hash(password)

    cursor.execute(
        """
        INSERT INTO patients (first_name, last_name, date_of_birth, gender, email, password_hash)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (first_name, last_name, date_of_birth, gender, email, password_hash),
    )

    conn.commit()
    conn.close()
