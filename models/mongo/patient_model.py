from config import Config
from pymongo import MongoClient
from bson.objectid import ObjectId

def mongo_connection():
    """
    Get MongoDB connection
    Returns client, db and collection if successful, else None.
    """
    try:
        client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)
        mdb = client[Config.MONGO_DB]
        patients_collection = mdb[Config.MONGO_PATIENT_COL]
        
        # Test connection
        client.server_info()
        print("Connected to MongoDB")
        return client, mdb, patients_collection
    
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        return None, None, None


def create_patient(patient_id):
    client, mdb, patients_collection = mongo_connection()
    
    if patients_collection is None:
        return None
    
    try:
        patient = {
            "_id": ObjectId(),
            "first_name": "lilian",
            "last_name": "chima",
            "patient_id": patient_id,
        }
        patients_collection.insert_one(patient)
        return str(patient["_id"])
    finally:
        if client is not None:
            client.close()



def get_patient_by_id(patient_id):
    client, mdb, patients_collection = mongo_connection()
    
    if patients_collection is None:
        return None
    
    try:
        patient = patients_collection.find_one({"_id": ObjectId(patient_id)})
        print(patient)
        return patient
    finally:
        if client is not None:
            client.close()