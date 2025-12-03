"""
Patient model - Simple data class for patient information
"""

class Patient:
    """
    Patient class to represent a patient in the system
    Data is retrieved directly from the database using raw SQL
    """

    def __init__(self, id=None, name=None, age=None, gender=None, email=None, 
                 phone=None, blood_type=None, condition=None, last_visit=None, status="Active"):
        self.id = id
        self.name = name
        self.age = age
        self.gender = gender
        self.email = email
        self.phone = phone
        self.blood_type = blood_type
        self.condition = condition
        self.last_visit = last_visit
        self.status = status
