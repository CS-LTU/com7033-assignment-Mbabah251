"""
User model - Simple data class for user information
"""

class User:
    """
    User class to represent a user in the system
    Data is retrieved directly from the database using raw SQL
    """

    def __init__(self, id=None, full_name=None, email=None, password_hash=None, 
                 role="Patient", created_at=None, reset_token=None, token_expiry=None):
        self.id = id
        self.full_name = full_name
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.created_at = created_at
        self.reset_token = reset_token
        self.token_expiry = token_expiry
