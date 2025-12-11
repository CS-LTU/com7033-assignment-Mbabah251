import sqlite3
import re
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
    patient=cursor.lastrowid
   

    conn.commit()
    conn.close()
    return patient


def validate_emergency_contact_data(first_name, last_name, phone_number, relationship):
    """
    Validate emergency contact data.
    Raises ValueError with appropriate message if validation fails.
    """
    # Validate required fields
    if not all([first_name, last_name, phone_number, relationship]):
        raise ValueError('All fields are required.')
    
    # Validate phone number format starting with 0 or international format +
    phone_pattern = r'^(\+?[1-9]\d{0,3})?[0-9]{10,14}$'
    if not re.match(phone_pattern, phone_number.strip()):
        raise ValueError('Phone number must start with 0 or international format (e.g., +234).')
    
    # Validate relationship
    valid_relationships = ['Spouse', 'Parent', 'Sibling', 'Family', 'Friend']
    if relationship not in valid_relationships:
        raise ValueError(f'Relationship must be one of the options.')