import sqlite3
import os  

def users_schema():
    '''Define the users table schema'''
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
      
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'Patient',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            reset_token TEXT,
            token_expiry TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()