
import os
import sqlite3

def patients_schema():
    '''Define the patients table schema'''
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
      
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            email TEXT,
            phone TEXT,
            blood_type TEXT,
            condition TEXT,
            last_visit TEXT,
            status TEXT DEFAULT 'Active'
        )
    """)
    
    conn.commit()
    conn.close()