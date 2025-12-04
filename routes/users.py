from flask import render_template, flash, redirect, url_for, request
from utils.decorators import login_required, doctor_or_nurse_required, doctor_required
import sqlite3
from models.patient import Patient

def users_routes(app):

    @app.route("/dashboard")
    @login_required
    @doctor_or_nurse_required
    def dashboard():
        """
        Dashboard route: shows list of all patients ordered by date
        """
        conn = sqlite3.connect('hospital.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Order by newest first in descending order
        cursor.execute("SELECT * FROM patients ORDER BY created_at DESC")
        patients = cursor.fetchall()

        conn.close()
        
        return render_template(
            "pages/users/dashboard.html",
            patients=patients
        )

    @app.route("/patient/<int:patient_id>")
    @login_required
    @doctor_or_nurse_required
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

    @app.route("/patient/<int:patient_id>/update", methods=['POST'])
    @login_required
    @doctor_or_nurse_required
    def update_patient_route(patient_id):
        try:
            first_name = request.form.get('firstname', '').strip()
            last_name = request.form.get('lastname', '').strip()
            date_of_birth = request.form.get('dob', '').strip()
            gender = request.form.get('gender', '').strip()
            
            Patient.validate_patient_data(date_of_birth=date_of_birth, gender=gender)
            Patient.update_patient(patient_id, first_name, last_name, date_of_birth, gender)
            flash('Patient information updated successfully!', 'success')
            return redirect(url_for('patient_detail', patient_id=patient_id))
        
        except ValueError as err:
            flash(str(err), 'error')
            return redirect(url_for('patient_detail', patient_id=patient_id))
        
    @app.route("/patient/<int:patient_id>/delete", methods=['POST'])
    @login_required
    @doctor_required
    def delete_patient_route(patient_id):
        try:
            
            patient = Patient.get_by_id(patient_id)
            
            if not patient:
                flash('Patient not found.', 'error')
                return redirect(url_for('dashboard'))
            
            Patient.delete(patient_id)
            flash(f'Patient deleted successfully!', 'success')
            return redirect(url_for('dashboard'))

        except Exception as err:
            flash(f'Error deleting patient: {str(err)}', 'error')
            return redirect(url_for('dashboard'))