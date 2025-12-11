import unittest
from app import app
import sqlite3
import os


def create_database():
    """Create test database with users table"""
    db_name = 'test_database.db'
    
    if os.path.exists(db_name):
        os.remove(db_name)
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL
    )
    ''')
    
    cursor.execute(''' 
        INSERT INTO users (first_name, last_name, email, password_hash, role)
        VALUES (?, ?, ?, ?, ?)
    ''', ('John', 'Doe', 'john@example.com', 'hashed_password_123', 'doctor'))
    
    conn.commit() 
    conn.close()


def user_in_db(email):
    """Check if user exists in database"""
    db_name = 'test_database.db'
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return user is not None


class HospitalAppTest(unittest.TestCase):
    """Test cases for Hospital Management System"""
    
    def setUp(self):
        """Set up test client"""
        self.email = "john@example.com"
        app.config['TESTING'] = True
        self.app = app.test_client()
    
    def test_home_page(self):
        """Test that home page loads"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_signup_page(self):
        """Test that signup page loads"""
        response = self.app.get('/signup')
        self.assertIn(response.status_code, [200, 302])
        
    def test_login_page(self):
        """Test that login page loads"""
        response = self.app.get('/login')
        self.assertIn(response.status_code, [200, 302])
    
    def test_user_creation(self):
        """Test user exists in database"""
        self.assertTrue(
            user_in_db(self.email),
            f"User with email {self.email} should exist in the database."
        )
    
    def test_404_error(self):
        """Test 404 error page"""
        response = self.app.get('/nonexistent-page')
        self.assertEqual(response.status_code, 404)


create_database()

if __name__ == "__main__":
    unittest.main(verbosity=2)
