from flask import render_template, session, request, flash, redirect, url_for
from utils.decorators import patient_login_required
from utils.patient_utils import validate_emergency_contact_data
from models.mongo.emergency_contact_model import (
    get_emergency_contacts_by_patient_id,
    count_emergency_contacts,
    create_emergency_contact,
    get_emergency_contact_by_id,
    update_emergency_contact,
    delete_emergency_contact
)
from models.mongo.assessment_model import get_assessments_by_patient_id
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

        conn.close()

        # Get emergency contacts from MongoDB
        emergency_contacts = get_emergency_contacts_by_patient_id(patient_id)
        
        # Get assessments from MongoDB
        assessments = get_assessments_by_patient_id(patient_id)

        return render_template(
            "pages/patient_user/patient_dashboard.html",
            patient=patient,
            emergency_contacts=emergency_contacts,
            assessments=assessments
        )

    @app.route("/patient/emergency-contact/add", methods=['POST'])
    @patient_login_required
    def add_emergency_contact():
        patient_id = session.get("patient_id")
        
        try:
            # Check if patient already has 2 emergency contacts
            existing_count = count_emergency_contacts(patient_id)
            if existing_count >= 2:
                raise ValueError("You cannot have more than 2 emergency contacts.")
            
            first_name = request.form.get('first_name', '').strip()
            last_name = request.form.get('last_name', '').strip()
            phone_number = request.form.get('phone_number', '').strip()
            relationship = request.form.get('relationship', '').strip()
            
            validate_emergency_contact_data(first_name, last_name, phone_number, relationship)
            
            create_emergency_contact(patient_id, first_name, last_name, phone_number, relationship)
            
            flash('Emergency contact added successfully!', 'success')
        except ValueError as er:
            flash(str(er), 'error')
        except Exception as e:
            flash(f'Failed to add emergency contact: {str(e)}', 'error')
        
        return redirect(url_for('patient_dashboard'))

    @app.route("/patient/emergency-contact/<contact_id>/update", methods=['POST'])
    @patient_login_required
    def update_emergency_contact_route(contact_id):
        patient_id = session.get("patient_id")
        
        try:
            first_name = request.form.get('first_name', '').strip()
            last_name = request.form.get('last_name', '').strip()
            phone_number = request.form.get('phone_number', '').strip()
            relationship = request.form.get('relationship', '').strip()
            
            validate_emergency_contact_data(first_name, last_name, phone_number, relationship)
            
            updated = update_emergency_contact(contact_id, patient_id, first_name, last_name, phone_number, relationship)
            
            if updated:
                flash('Emergency contact updated successfully!', 'success')
            else:
                flash('No updates were made.', 'warning')
        except ValueError as er:
            flash(str(er), 'error')
        except Exception as e:
            flash(f'Failed to update emergency contact: {str(e)}', 'error')
        
        return redirect(url_for('patient_dashboard'))

    @app.route("/patient/emergency-contact/<contact_id>/delete", methods=['POST'])
    @patient_login_required
    def delete_emergency_contact_route(contact_id):
        try:
            deleted = delete_emergency_contact(contact_id)
            if deleted:
                flash('Emergency contact deleted successfully!', 'success')
            else:
                flash('Emergency contact not found.', 'error')
        except Exception as e:
            flash(f'Failed to delete emergency contact: {str(e)}', 'error')
        
        return redirect(url_for('patient_dashboard'))