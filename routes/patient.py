from flask import render_template
from utils.decorators import login_required
import sqlite3
import os
from utils.users_utils import get_current_user

def patient_routes(app):

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
            "dashboard.html",
            patients=patients
        )

    @app.route("/patient/<int:patient_id>")
    @login_required
    def patient_detail(patient_id):
        """
        View detailed information for a specific patient
        Only accessible to authenticated users
        
        Args:
            patient_id: ID of the patient to display
        """
        user = get_current_user()
        
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
        patient = cursor.fetchone()
        conn.close()
        
        # # If patient not found, return 404 error
        # if not patient:
        #     abort(404)

        # Render patient detail page with patient information and user context
        return render_template(
            "patient_detail.html",
            user=user['full_name'],
            user_role=user['role']
        )
