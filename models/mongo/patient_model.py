from config import Config
from pymongo import MongoClient
from bson.objectid import ObjectId
client = MongoClient(Config.MONGO_URI)
mdb = client[Config.MONGO_DB]
patients_collection = mdb[Config.MONGO_PATIENT_COL]


def create_patient(patient_id):
    patient = {
        "_id": ObjectId(),
        "first_name": "lilian",
        "last_name": "chima",
        "patient_id": patient_id,

    }
    patients_collection.insert_one(patient)
    return str(patient["_id"])

def get_patient_by_id(patient_id):
    patient = patients_collection.find_one({"_id": ObjectId(patient_id)})
    print(patient)
    return patient