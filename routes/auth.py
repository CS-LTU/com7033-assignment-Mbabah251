from flask import render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import check_password_hash
from utils.users_utils import validate_if_email_exist, insert_user
import re
from utils.patient_utils import insert_patient


def auth_routes(app):
    @app.route('/')
    def home():
        return render_template("home.html")

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == "POST":
            try:
                role = request.form.get("role", "").strip()
                first_name = request.form.get("first_name", "").strip()
                last_name = request.form.get("last_name", "").strip()
                email = request.form.get("email", "").strip().lower()
                password = request.form.get("password", "").strip()
                confirm = request.form.get("confirmPassword", "").strip()

                # Patient-only fields 
                date_of_birth = request.form.get("date_of_birth", "").strip()
                gender = request.form.get("gender", "").strip()

                # Basic validation
                if not first_name or not last_name or not email or not password or not role:
                    flash("Please fill in all required fields.", "danger")
                    return redirect(url_for("signup"))

                # Email validation
                email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                if not re.match(email_pattern, email):
                    raise ValueError("Please enter a valid email address.")

                # Password validation
                pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W).{8,}$'
                if not re.match(pattern, password):
                    raise ValueError(
                        "Password must be 8+ chars and include upper, lower, digit, and special char."
                    )

                if password != confirm:
                    raise ValueError("Passwords do not match.")

                # Check if email already exists (in your helper)
                validate_if_email_exist(email)

                # ROLE-BASED INSERT
                if role == "Patient":
                    # Ensure patient-specific fields
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

        return render_template("signup.html")


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == "POST":
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password")

            conn = sqlite3.connect('hospital.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            conn.close()

            #user and Verify password
            if not user or not check_password_hash(user[4], password):
                flash("Invalid email or password.", "danger")
                return redirect(url_for("login"))

            # Store user id in session
            session["user_id"] = user['id']
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))

        return render_template("login.html")

    @app.route('/logout')
    def logout():
        # Clear all session data to log user out
        session.clear()
        flash("You have been logged out.", "info")
        return redirect(url_for("home"))
