from flask import render_template, flash, redirect, url_for
from utils.decorators import login_required
import sqlite3
from utils.users_utils import get_current_user
from models.patient import Patient

def users_routes(app):

    @app.route("/dashboard")
    @login_required
    def dashboard():
        """
        Dashboard route - shows list of all patients ordered by date
        """
        conn = sqlite3.connect('hospital.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Order by newest first (DESC). Change to ASC if you want oldest first.
        cursor.execute("SELECT * FROM patients ORDER BY created_at DESC")
        patients = cursor.fetchall()

        conn.close()
        
        return render_template(
            "pages/users/dashboard.html",
            patients=patients
        )

    @app.route("/patient/<int:patient_id>")
    @login_required
    def patient_detail(patient_id):

        conn = sqlite3.connect('hospital.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            flash("Patient not found.", "danger")
            return redirect(url_for("dashboard"))

        patient = Patient(*row)

        return render_template(
            "pages/users/patient_detail.html",
            patient=patient
        )
