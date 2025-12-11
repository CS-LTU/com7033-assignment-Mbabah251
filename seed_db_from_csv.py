import os
import random
import sqlite3
from datetime import date

import pandas as pd
from faker import Faker
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

# Seed database on app startup: loads healthcare dataset and creates test patients with assessments
load_dotenv()

INPUT_CSV = "healthcare-dataset-stroke-data.csv"
OUTPUT_CSV = "healthcare_stroke_with_fake_names.csv"
MAX_ROWS = 1500
SQLITE_DB_PATH = "hospital.db"





MONGO_URI = os.environ.get("MONGO_URI")
MONGO_DB_NAME = os.environ.get("MONGO_DB")
MONGO_COLLECTION_NAME = os.environ.get("MONGO_ASSESSMENT_COL", "assessments")

fake = Faker()
Faker.seed(42)
random.seed(42)

def generate_fake_identity(gender_value: str):
    """
    Generate fake first name, last name, and email based on gender.
    """
    g = str(gender_value).strip().lower()

    if g == "male":
        first_name = fake.first_name_male()
    elif g == "female":
        first_name = fake.first_name_female()
    else:
        first_name = fake.first_name()

    last_name = fake.last_name()

    # Generate email with random number suffix
    number = random.randint(10, 9999)
    email = f"{first_name.lower()}.{last_name.lower()}{number}@gmail.com"

    return first_name, last_name, email


def approximate_dob_from_age(age_value):
    """
    Convert age value to date_of_birth string (YYYY-01-01 format).
    """
    try:
        age_int = int(float(age_value))
    except (TypeError, ValueError):
        age_int = 40  # Default age if missing or invalid

    today = date.today()
    year = today.year - age_int
    return date(year, 1, 1).isoformat()  # 'YYYY-MM-DD'


def normalise_gender_for_db(gender_value: str):
    """
    Normalize gender: 'Male', 'Female', 'Other'.
    """
    g = str(gender_value).strip().lower()
    if g == "male":
        return "Male"
    if g == "female":
        return "Female"
    return "Other"

def load_and_augment_csv():
    """
    Load stroke dataset and add fake identities (name, email, DOB).
    Saves augmented data to OUTPUT_CSV.
    """
    print("Loading CSV...")
    df = pd.read_csv(INPUT_CSV)

    # Load first MAX_ROWS records
    df = df.head(MAX_ROWS).copy()

    first_names = []
    last_names = []
    emails = []
    dobs = []

    for row in df.itertuples(index=False):
        gender_value = getattr(row, "gender")
        age_value = getattr(row, "age")

        first_name, last_name, email = generate_fake_identity(gender_value)
        dob = approximate_dob_from_age(age_value)

        first_names.append(first_name)
        last_names.append(last_name)
        emails.append(email)
        dobs.append(dob)

    df["first_name"] = first_names
    df["last_name"] = last_names
    df["email"] = emails
    df["date_of_birth"] = dobs

    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Created new CSV with fake identities: {OUTPUT_CSV}")

    return df

def seed_databases(df: pd.DataFrame):
    """
    Insert patient records into SQLite and assessments into MongoDB.
    Password hash is generated as @Password{patient_id}.
    """
    print("Connecting to SQLite and MongoDB...")

    # SQLite connection
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()

    # Mongo connection
    client = MongoClient(MONGO_URI)
    mdb = client[MONGO_DB_NAME]
    assess_coll = mdb[MONGO_COLLECTION_NAME]

    created_patients = 0
    created_assessments = 0

    print("Seeding data...")
    for row in df.itertuples(index=False):
        # Extract patient demographic fields
        first_name = row.first_name
        last_name = row.last_name
        gender_original = row.gender
        gender_for_db = normalise_gender_for_db(gender_original)
        email = row.email
        dob = row.date_of_birth

        # Check if patient already exists by email
        cursor.execute("SELECT id FROM patients WHERE email = ?", (email,))
        existing = cursor.fetchone()

        if existing:
            # Use existing patient ID
            patient_id = existing[0]
        else:
            # Insert new patient with temporary password placeholder
            cursor.execute(
                """
                INSERT INTO patients (first_name, last_name, date_of_birth, gender, email, password_hash)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (first_name, last_name, dob, gender_for_db, email, "TEMP"),
            )
            patient_id = cursor.lastrowid

            # Generate password hash based on patient ID
            password_plain = f"@Password{patient_id}"
            password_hash = generate_password_hash(password_plain)

            # Update patient record with actual password hash
            cursor.execute(
                "UPDATE patients SET password_hash = ? WHERE id = ?",
                (password_hash, patient_id),
            )

            created_patients += 1

        # Insert clinical assessment data into MongoDB
        assessment_doc = {
            "patient_id": patient_id,
            "age": float(row.age),
            "hypertension": int(row.hypertension),
            "heart_disease": int(row.heart_disease),
            "ever_married": row.ever_married,
            "work_type": row.work_type,
            "residence_type": row.Residence_type,
            "avg_glucose_level": float(row.avg_glucose_level),
            "bmi": float(row.bmi) if str(row.bmi) != "nan" else None,
            "smoking_status": row.smoking_status,
            "stroke": int(row.stroke),
        }

        assess_coll.insert_one(assessment_doc)
        created_assessments += 1

    conn.commit()
    conn.close()
    client.close()

    print(f" Seeded {created_patients} new patients into SQLite.")
    print(f" Seeded {created_assessments} assessment documents into MongoDB.")


def run_seed():
    """
    Run seeding once on startup using a marker file to prevent duplicates.
    """
    seed_marker = ".seed_complete"
    
    if os.path.exists(seed_marker):
        print(" Database already seeded.")
        return
    
    print("Seeding database...")
    df = load_and_augment_csv()
    seed_databases(df)
    
    with open(seed_marker, "w") as f:
        f.write("Database seeded successfully")
    
    print("Seeding complete.")


if __name__ == "__main__":
    run_seed()
    print("Seeding complete.")