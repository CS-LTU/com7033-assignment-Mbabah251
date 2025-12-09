class User:
    """
    User class to represent a user in the system
    Data is retrieved directly from the database using raw SQL
    """

    def __init__(self, id=None, first_name=None, last_name=None, email=None, 
                 password_hash=None, role=None, created_at=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.created_at = created_at
    
    def is_doctor(self):
        """
        Check if user is a doctor
        """
        return self.role == 'Doctor'
    
    def is_nurse(self):
        """
        Check if user is a nurse
        """
        return self.role == 'Nurse'
    
    def is_patient(self):
        """
        Check if user is a patient
        """
        return self.role == 'Patient'