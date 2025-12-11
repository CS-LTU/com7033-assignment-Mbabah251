from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Config:
    BASE_DIR = os.getcwd()
    SECRET_KEY = os.environ.get("SECRET_KEY", "change_me_dev_key")
    DB_PATH = os.path.join(BASE_DIR, "hospital.db")

    # Mongo
    MONGO_URI = os.environ.get("MONGO_URI")
    MONGO_DB = os.environ.get("MONGO_DB", "SecureApp12")
    MONGO_PATIENT_COL = os.environ.get("MONGO_PATIENT_COL", "patients")
    MONGO_EMERGENCY_CONTACT_COL = os.environ.get("MONGO_EMERGENCY_CONTACT_COL", "emergency_contacts")
    MONGO_ASSESSMENT_COL = os.environ.get("MONGO_ASSESSMENT_COL", "assessments")