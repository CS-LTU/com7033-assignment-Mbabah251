
from pathlib import Path


import os

class Config:
    BASE_DIR = os.getcwd()
    SECRET_KEY = os.environ.get("SECRET_KEY", "change_me_dev_key")
    DB_PATH = os.path.join(BASE_DIR, "hospital.db")

    # Mongo
    MONGO_URI = os.environ.get(
        "MONGO_URI",
        "mongodb+srv://ekemini_db_user:Mvik1Ux3FNj082FO@cluster0.kuiueyq.mongodb.net/?appName=Cluster0"
    )
    MONGO_DB = "SecureApp12"
    MONGO_PATIENT_COL = "patients"


