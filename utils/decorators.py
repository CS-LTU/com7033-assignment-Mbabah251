from flask import session, redirect, url_for, flash
from functools import wraps

from utils.users_utils import get_current_user

def login_required(view_func):
    """
    Decorator to require login for a route
    Redirects to login page if user is not authenticated
    """
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        # Check if user_id is stored in session (indicates logged in user)
        if "user_id" not in session:
            session.clear() 
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)
    return wrapper

def patient_login_required(f):
    """Ensures only logged-in patients can access the route."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "patient_id" not in session:
            session.clear()
            flash("Please login to continue.", "danger")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


def doctor_required(func):
    """
    Decorator to require 'Doctor' role for accessing a route
    Redirects to dashboard if user is not a doctor
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get current logged-in user
        user = get_current_user()
        
        # Check if user exists and has 'Doctor' role
        if not user or user['role'] != 'Doctor':
            session.clear() 
            flash("You do not have permission to access this page.", "danger")
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper


def nurse_required(func):
    """
    Decorator to require 'Nurse' role for accessing a route
    Redirects to dashboard if user is not a nurse
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get current logged-in user
        user = get_current_user()
        
        # Check if user exists and has 'Nurse' role
        if not user or user['role'] != 'Nurse':
            session.clear()
            flash("You do not have permission to access this page.", "danger")
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper


def doctor_or_nurse_required(func):
    """
    Decorator to require 'Doctor' or 'Nurse' role for accessing a route
    Redirects to dashboard if user is neither
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get current logged-in user
        user = get_current_user()
        
        # Check if user exists and has 'Doctor' or 'Nurse' role
        if not user or user['role'] not in ['Doctor', 'Nurse']:
            session.clear() 
            flash("You do not have permission to access this page.", "danger")
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper