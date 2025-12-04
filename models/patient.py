import sqlite3
import re
from datetime import date, datetime
from werkzeug.security import generate_password_hash

DB_PATH = "hospital.db"


class Patient:
    """
    Patient Model representing a patient record.
    Handles CRUD operations (Create, Read, Update).
    """

    def __init__(self, id, first_name, last_name, date_of_birth, gender, email, password_hash, created_at):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at
  
    @staticmethod
    def get_by_id(patient_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return Patient(*row)

    @staticmethod
    def insert(first_name, last_name, date_of_birth, gender, email, password):
        """
        Insert a new patient.
        """
        password_hash = generate_password_hash(password)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO patients (first_name, last_name, date_of_birth, gender, email, password_hash)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (first_name, last_name, date_of_birth, gender, email, password_hash),
        )

        conn.commit()
        conn.close()


    @staticmethod
    def update_patient(id, first_name, last_name, date_of_birth, gender):
        """
        Update an existing patient's information.
        """

        # Validate required fields
        if not first_name or not last_name or not date_of_birth or not gender:
            raise ValueError("All fields are required. Please fill out all fields.")

        try:
            conn = sqlite3.connect("hospital.db")
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE patients
                SET first_name = ?, last_name = ?, date_of_birth = ?, gender = ?
                WHERE id = ?
            """, (first_name, last_name, date_of_birth, gender, id))

            # No rows updated then raise patient does not exist
            if cursor.rowcount == 0:
                conn.close()
                raise ValueError(f"No patient found with ID {id}.")

            conn.commit()
            conn.close()
            return True

        except sqlite3.IntegrityError:
            raise ValueError("Error while updating patient information.")

        except sqlite3.Error as e:
            raise ValueError(f"Database error occurred: {str(e)}")
        
    @staticmethod
    def validate_patient_data(email=None, date_of_birth=None, gender=None):
        """
        This function validates patient data if any of the fields are passed.
        It raises ValueError with appropriate message if validation fails.
        """
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            if email:
                cursor.execute('''
                SELECT 1
                FROM patients
                WHERE email = ?
                ''', (email,))
                if cursor.fetchone(): 
                    raise ValueError('Email already registered. Please use a different email')
                
                # Email pattern validation
                email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                if not re.match(email_pattern, email):
                    raise ValueError('Please enter a valid email address') 
        

            if date_of_birth:
                # Calculate age from date_of_birth
                dob = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
                today = date.today()
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                if age < 0 or age > 120:
                    raise ValueError('Age must be between 0 and 120.')
            
            if gender:
                if gender not in ['Male', 'Female', 'Other']:
                    raise ValueError('Gender must be Male, Female, or Other.')
        finally:
            conn.close()

    @staticmethod
    def delete(patient_id):
        """
        Delete a patient by ID.
        """
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))

        conn.commit()
        conn.close()