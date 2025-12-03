
import sqlite3

def patients_schema():
    '''Define the patients table schema'''
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
      
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            date_of_birth DATE NOT NULL,
            gender TEXT,
            email TEXT,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
        )
    """)
    
    conn.commit()
    conn.close()