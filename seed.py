
import sqlite3
import os
from schema.users import users_schema
from schema.patients import patients_schema
from werkzeug.security import generate_password_hash
from utils.data import SAMPLE_PATIENTS

DB_NAME = 'hospital.db'


def delete_and_create_database():
    """
    Drop and recreate the database tables
    """
    os.makedirs('instance', exist_ok=True)
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Drop tables if they exist
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS patients")
    
    conn.commit()
    conn.close()
    
    # Recreate tables from schema
    users_schema()
    patients_schema()


def seed_database():
    """
    Initialize database with tables and sample data
    """
    print("Deleting and recreating database...")
    delete_and_create_database()
    print("Tables created.")
    
    print("Seeding database with initial data...")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Insert sample users
    print("Creating sample users...")
    sample_users = [
        ("Admin User", "admin@hospital.com", "Admin", "admin123"),
        ("Nurse Sarah", "nurse@hospital.com", "Nurse", "nurse123"),
        ("Doctor John", "doctor@hospital.com", "Nurse", "doctor123"),
    ]
    
    for full_name, email, role, password in sample_users:
        password_hash = generate_password_hash(password)
        cursor.execute("""
            INSERT OR IGNORE INTO users (full_name, email, password_hash, role)
            VALUES (?, ?, ?, ?)
        """, (full_name, email, password_hash, role))
    
    print(f"{len(sample_users)} users inserted.")
    
    # Insert sample patients
    print("Creating sample patients...")
    for patient in SAMPLE_PATIENTS:
        cursor.execute("""
            INSERT OR IGNORE INTO patients (name, age, gender, email, phone, blood_type, condition, last_visit, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, patient)
    
    print(f"{len(SAMPLE_PATIENTS)} patients inserted.")
    
    conn.commit()
    conn.close()
    print("Database seeding completed successfully!")


if __name__ == "__main__":
    seed_database()

