from flask import render_template, session
from utils.decorators import patient_login_required
import sqlite3


def patient_routes(app):
    @app.route("/patient/dashboard")
    @patient_login_required
    def patient_dashboard():
        """
        Patient dashboard  loads a single patient's data
        and displays their bio assessment history.
        """

        patient_id = session.get("patient_id")

        conn = sqlite3.connect('hospital.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
        patient = cursor.fetchone()

        # cursor.execute("""
        #     SELECT *
        #     FROM assessments
        #     WHERE patient_id = ?
        #     ORDER BY created_at DESC
        # """, (patient_id,))
        # assessments = cursor.fetchall()

        conn.close()

        return render_template(
            "pages/patient_user/patient_dashboard.html",
            patient=patient
        )

