from config import Config
from bson.objectid import ObjectId
from models.mongo.patient_model import mongo_connection
from datetime import datetime


def get_assessment_collection():
    """Get assessments collection from MongoDB"""
    client, mdb, _ = mongo_connection()
    if client is None:
        return None, None
    assessment_coll = mdb[Config.MONGO_ASSESSMENT_COL]
    return client, assessment_coll


def get_assessments_by_patient_id(patient_id):
    """Get all assessments for a patient"""
    client, coll = get_assessment_collection()
    if coll is None:
        return []
    
    assessments = list(coll.find({"patient_id": int(patient_id)}).sort("created_at", -1))
    client.close()
    return assessments


def create_assessment(patient_id, hypertension, ever_married, work_type, residence_type, 
                     avg_glucose_level, bmi, smoking_status, stroke):
    """Create a new assessment record"""
    client, coll = get_assessment_collection()
    if coll is None:
        return None
    
    new_assessment = {
        "patient_id": int(patient_id),
        "hypertension": int(hypertension),
        "ever_married": ever_married,
        "work_type": work_type,
        "residence_type": residence_type,
        "avg_glucose_level": float(avg_glucose_level),
        "bmi": float(bmi),
        "smoking_status": smoking_status,
        "stroke": int(stroke),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    result = coll.insert_one(new_assessment)
    client.close()
    return str(result.inserted_id)