from config import Config
from pymongo import MongoClient
from bson.objectid import ObjectId
from models.mongo.patient_model import mongo_connection


def get_emergency_collection():
    """Get emergency contacts collection from MongoDB"""
    client, mdb, _ = mongo_connection()
    if client is None:
        return None, None
    emergency_coll = mdb[Config.MONGO_EMERGENCY_CONTACT_COL]
    return client, emergency_coll


def get_emergency_contacts_by_patient_id(patient_id):
    """Get all emergency contacts for a patient"""
    client, coll = get_emergency_collection()
    if coll is None:
        return []
    
    contacts = list(coll.find({"patient_id": int(patient_id)}))
    client.close()
    return contacts


def count_emergency_contacts(patient_id):
    """Count emergency contacts for a patient"""
    client, coll = get_emergency_collection()
    if coll is None:
        return 0
    
    count = coll.count_documents({"patient_id": int(patient_id)})
    client.close()
    return count


def create_emergency_contact(patient_id, first_name, last_name, phone_number, relationship):
    """Create a new emergency contact"""
    client, coll = get_emergency_collection()
    if coll is None:
        return None
    
    new_contact = {
        "patient_id": int(patient_id),
        "first_name": first_name,
        "last_name": last_name,
        "phone_number": phone_number,
        "relationship": relationship
    }
    result = coll.insert_one(new_contact)
    client.close()
    return str(result.inserted_id)


def get_emergency_contact_by_id(contact_id):
    """Get a single emergency contact by ID"""
    client, coll = get_emergency_collection()
    if coll is None:
        return None
    
    contact = coll.find_one({"_id": ObjectId(contact_id)})
    client.close()
    return contact


def update_emergency_contact(contact_id, patient_id, first_name, last_name, phone_number, relationship):
    """Update an emergency contact"""
    client, coll = get_emergency_collection()
    if coll is None:
        return False
    
    updated_contact = {
        "first_name": first_name,
        "last_name": last_name,
        "phone_number": phone_number,
        "relationship": relationship
    }
    result = coll.update_one(
        {"_id": ObjectId(contact_id), "patient_id": int(patient_id)},
        {"$set": updated_contact}
    )
    client.close()
    return result.modified_count > 0


def delete_emergency_contact(contact_id):
    """Delete an emergency contact"""
    client, coll = get_emergency_collection()
    if coll is None:
        return False
    
    result = coll.delete_one({"_id": ObjectId(contact_id)})
    client.close()
    return result.deleted_count > 0