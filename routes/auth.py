from flask import render_template, request, redirect, url_for, flash, session
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

def auth_routes(app):
    @app.route('/')
    def home():
        return render_template("home.html")
    

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == "POST":
            category = request.form.get("category")
            full_name = request.form.get("fullname")
            email = request.form.get("email")
            password = request.form.get("password")
            confirm = request.form.get("confirmPassword")

            # Validation: Check if all fields are filled
            if not full_name or not email or not password:
                flash("Please fill in all fields.", "danger")
                return redirect(url_for("signup"))

            # Validation: Check if passwords match
            if password != confirm:
                flash("Passwords do not match.", "danger")
                return redirect(url_for("signup"))

            # Normalize email for consistency (lowercase and strip whitespace)
            email = email.strip().lower()
            
            # Check if email already exists in database
            conn = sqlite3.connect('hospital.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            existing_user = cursor.fetchone()
            conn.close()
            
            if existing_user:
                flash("An account already exists with that email.", "warning")
                return redirect(url_for("signup"))

            # Use category from form as the user's role (Admin, Nurse, or Patient)
            role = category

            # Hash password and create new user in database
            password_hash = generate_password_hash(password)
            try:
                conn = sqlite3.connect('hospital.db')
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (full_name, email, password_hash, role) VALUES (?, ?, ?, ?)",
                    (full_name.strip(), email, password_hash, role)
                )
                conn.commit()
                conn.close()
                flash("Account created successfully!", "success")
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                flash("An error occurred while creating your account.", "danger")
                return redirect(url_for("signup"))

        return render_template("signup.html")


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")

            # Get user from database by email
            email = email.strip().lower()
            conn = sqlite3.connect('hospital.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            conn.close()

            # Verify password
            if not user or not check_password_hash(user['password_hash'], password):
                flash("Invalid email or password.", "danger")
                return redirect(url_for("login"))

            # Store user info in session for authentication tracking
            session["user_id"] = user['id']
            session["user_name"] = user['full_name']

            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))

        return render_template("login.html")

    @app.route('/logout')
    def logout():
        # Clear all session data to log user out
        session.clear()
        flash("You have been logged out.", "info")
        return redirect(url_for("home"))
