from flask import render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import check_password_hash
from utils.users_utils import validate_if_email_exist, insert_user
import re
from utils.patient_utils import insert_patient


# Register authentication routes
def auth_routes(app):
    # Home page route
    @app.route('/')
    def home():
        return render_template("home.html")

    # User signup route with form validation
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == "POST":
            try:
                # Get form data and strip whitespace
                role = request.form.get("role", "").strip()
                first_name = request.form.get("first_name", "").strip()
                last_name = request.form.get("last_name", "").strip()
                email = request.form.get("email", "").strip().lower()
                password = request.form.get("password", "").strip()
                confirm = request.form.get("confirmPassword", "").strip()

                # Patient-specific fields
                date_of_birth = request.form.get("date_of_birth", "").strip()
                gender = request.form.get("gender", "").strip()

                # Validate all required fields are filled
                if not first_name or not last_name or not email or not password or not role:
                    flash("Please fill in all required fields.", "danger")
                    return redirect(url_for("signup"))

                # Validate email format
                email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                if not re.match(email_pattern, email):
                    raise ValueError("Please enter a valid email address.")

                # Validate password strength (8+ chars, uppercase, lowercase, digit, special char)
                pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W).{8,}$'
                if not re.match(pattern, password):
                    raise ValueError(
                        "Password must be 8+ chars and include upper, lower, digit, and special char."
                    )

                # Confirm passwords match
                if password != confirm:
                    raise ValueError("Passwords do not match.")

                # Check if email already registered
                validate_if_email_exist(email)

                # Insert user or patient based on role
                if role == "Patient":
                    if not date_of_birth:
                        raise ValueError("Please provide Date of Birth for patients.")
                    if not gender:
                        raise ValueError("Please select a gender for patients.")

                    insert_patient(
                        first_name=first_name,
                        last_name=last_name,
                        date_of_birth=date_of_birth,
                        gender=gender,
                        email=email,
                        password=password,
                    )
                else:
                    # Insert doctor or nurse
                    insert_user(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        password=password,
                        role=role,
                    )

                flash("Account created successfully!", "success")
                return redirect(url_for("login"))

            except ValueError as ve:
                flash(str(ve), "danger")
                return redirect(url_for("signup"))

            except sqlite3.IntegrityError:
                flash("An account with this email may already exist.", "danger")
                return redirect(url_for("signup"))

        return render_template("pages/auth/signup.html")


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == "POST":
            # Get and normalize email
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password")

            # Connect to database
            conn = sqlite3.connect('hospital.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Check if user exists in users table (doctor/nurse)
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()

            # Check if user exists in patients table
            cursor.execute("SELECT * FROM patients WHERE email = ?", (email,))
            patient = cursor.fetchone()

            conn.close()

            # Authenticate user (doctor/nurse)
            if user:
                if check_password_hash(user[4], password):
                    # Create session for authenticated user
                    session["user_id"] = user["id"]
                    session["role"] = user["role"]
                    flash("Login successful!", "success")
                    return redirect(url_for("dashboard")) 
                else:
                    flash("Invalid password.", "danger")
                    return redirect(url_for("login"))

            # Authenticate patient
            if patient:
                if check_password_hash(patient[6], password):
                    # Create session for authenticated patient
                    session["patient_id"] = patient["id"]
                    flash("Login successful!", "success")
                    return redirect(url_for("patient_dashboard")) 
                else:
                    flash("Invalid password.", "danger")
                    return redirect(url_for("login"))

            # No matching user or patient found
            flash("Email not found.", "danger")
            return redirect(url_for("login"))

        return render_template("pages/auth/login.html")


    @app.route('/logout')
    def logout():
        # Clear all session data to log user out
        session.clear()
        flash("You have been logged out.", "info")
        return redirect(url_for("login"))
