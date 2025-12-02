"""
Sample patient data for seeding the database
Formatted as tuples to match the Patient.bulk_insert() SQL INSERT format
"""

SAMPLE_PATIENTS = [
    # (name, age, gender, email, phone, blood_type, condition, last_visit, status)
    ("John Michael Smith", 45, "Male", "john.smith@email.com", "+1-555-0101", "O+", "Hypertension", "2025-11-05", "Active"),
    ("Sarah Johnson Williams", 32, "Female", "sarah.j@email.com", "+1-555-0102", "A-", "Diabetes Type 2", "2025-11-03", "Active"),
    ("Robert David Brown", 58, "Male", "rbrown@email.com", "+1-555-0103", "B+", "Heart Disease", "2025-10-28", "Monitoring"),
    ("Emily Rose Davis", 27, "Female", "emily.rose@email.com", "+1-555-0104", "AB+", "Asthma", "2025-11-08", "Active"),
    ("Michael James Wilson", 52, "Male", "m.wilson@email.com", "+1-555-0105", "O-", "Arthritis", "2025-11-04", "Active"),
    ("Jennifer Lisa Moore", 38, "Female", "j.moore@email.com", "+1-555-0106", "B-", "Allergies", "2025-11-07", "Active"),
    ("William Charles Taylor", 64, "Male", "wtaylor@email.com", "+1-555-0107", "A+", "Hypertension", "2025-10-30", "Monitoring"),
    ("Jessica Ann Anderson", 29, "Female", "jessica.a@email.com", "+1-555-0108", "AB-", "Migraine", "2025-11-06", "Active"),
    ("Christopher Mark Thomas", 41, "Male", "cthomas@email.com", "+1-555-0109", "O+", "Lower Back Pain", "2025-11-02", "Active"),
    ("Amanda Marie Jackson", 35, "Female", "a.jackson@email.com", "+1-555-0110", "A-", "Thyroid", "2025-11-08", "Active"),
]


def get_sample_patients():
    """Return sample patient data as list of tuples for database insertion"""
    return SAMPLE_PATIENTS
