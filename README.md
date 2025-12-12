# Hospital Management System

A practical, security-aware Flask application for storing and viewing patient demographics, emergency contacts and clinical assessments. 

This README uses compact tables for clarity and quick reference.

---

## Quick links

| Section | Purpose |
|--------:|:--------|
| Quick start | Run locally in minutes |
| Architecture | High-level design |
| Routes | What endpoints exist and who can use them |
| Security | Validation and protection highlights |
| Dev & Tests | Seed, run, and test notes |
| Layout | Where to find code |

---

## Quick start (fast path)

1. Clone
```bash
git clone https://github.com/CS-LTU/com7033-assignment-Mbabah251.git
cd com7033-assignment-Mbabah251
```

2. Virtual environment & install
```bash
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows (PowerShell)
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Configure environment (`.env`)

| Variable | Required | Example / Notes |
|:--------|:--------:|:----------------|
| SECRET_KEY | Yes | replace_with_a_secure_value |
| MONGO_URI | Yes | mongodb+srv://user:pass@cluster.mongodb.net/ |
| MONGO_DB | Yes | hospital |
| PATIENT_COLLECTION | No (default) | patients |
| ASSESSMENT_COLLECTION | No (default) | assessments |
| EMERGENCY_CONTACT_COLLECTION | No (default) | emergency_contacts |

4. Seed local data
```bash
python seed_db_from_csv.py
```

5. Run
```bash
python app.py
```
Default host/port: http://localhost:8080 (adjust in app config if needed)

---

## Project snapshot

| Area | Summary |
|------|---------|
| Backend | Flask (Python 3.8+), server-rendered Jinja2 templates |
| Styling | Tailwind CSS (static prebuilt file included) |
| Auth store | SQLite (users, roles) |
| Clinical data | MongoDB (assessments, emergency contacts) |
| Forms / CSRF | Flask-WTF (CSRF tokens) |
| Tests / Tools | unittest, Faker, pandas (seed utilities) |

---

## High-level architecture

| Layer | Responsibilities |
|:------|:-----------------|
| Presentation | Jinja2 templates, server-rendered forms, static assets |
| Application | Flask routes, RBAC decorators, business logic |
| Data | SQLite for auth/registry; MongoDB for clinical documents |

---

## Routes - common workflows

(Note: all modifying endpoints use POST with CSRF protection. See `routes/` for handler names.)

| Area | Method | Route | Access | Purpose / Required fields |
|:----:|:------:|:-----|:------:|:-------------------------|
| Auth | GET | `/` | Public | Landing / login page |
| Auth | POST | `/login` | Public | Authenticate (email, password) |
| Auth | GET | `/signup` | Public | Registration page |
| Auth | POST | `/signup` | Public | Create user (first_name, last_name, email, password, role, patient fields) |
| Auth | GET | `/logout` | Authenticated | Logout (clear session) |
| Dashboard | GET | `/dashboard` | Doctor/Nurse | Paginated patient list (page param) |
| Patient | GET/POST | `/patient/add` | Doctor/Nurse | Create patient (first_name, last_name, dob, gender, email, password) |
| Patient | GET | `/patient/<id>` | Doctor/Nurse | View patient details & assessments |
| Patient | POST | `/patient/<id>/update` | Doctor/Nurse | Update patient demographics |
| Patient | POST | `/patient/<id>/delete` | Doctor only | Delete patient record |
| Assessment | POST | `/patient/<id>/assess` | Doctor only | Create health assessment (age, bmi, hypertension, heart_disease, smoking_status, stroke_risk) |
| Emergency | GET/POST | `/patient/emergency-contact/add` | Patient | Add contact (first_name, last_name, phone_number, relationship) |
| Emergency | POST | `/patient/emergency-contact/<contact_id>/update` | Patient | Update contact |
| Emergency | POST | `/patient/emergency-contact/<contact_id>/delete` | Patient | Delete contact |

---

## Input validation & examples

| Field | Validation |
|:------|:-----------|
| Email | RFC-style regex: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$` |
| Password | Minimum 8 chars; recommend mixed case, digit, special char (`^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W).{8,}$`) |
| Age | Integer, 0–120 |
| BMI | Float, sensible range (e.g., 10–100) |
| Glucose | Float, 0–500 |

Quick test example (create patient via form fields):
- Required POST fields: first_name, last_name, date_of_birth (YYYY-MM-DD), gender, email, password

---

## Security highlights

| Control | Purpose |
|:-------|:--------|
| Password hashing (Werkzeug/bcrypt) | Protect stored credentials |
| CSRF (Flask-WTF) | Protect POST endpoints |
| Session-based auth | Simple server-side sessions storing minimal identifiers |
| Parameterized SQLite queries | Prevent SQL injection |
| Input sanitization for MongoDB | Reduce NoSQL injection risk |
| Decorator-based RBAC | Enforce least-privilege in routes |
| Custom error pages | Avoid leaking stack traces to users |

---

## Developer notes & testing

| Action | Command / Notes |
|:------|:----------------|
| Run app | `python app.py` |
| Run tests | `python test.py -v` (ensure `.env` set; seed DB if tests need data) |
| Seed data | `python seed_db_from_csv.py` (see schema/ and data/ for CSV sources) |
| Templates | `templates/` — main layout: `templates/base.html` |
| Helpers | `utils/` contains decorators, sanitizers, and validation helpers |

Testing notes:
- Tests cover authentication, core routes, and basic DB ops. Add tests for new features and edge cases.

---

## Project layout ( high level )

| Path | Purpose |
|:-----|:--------|
| app.py | App entry point and server start |
| config.py | Configuration and environment handling |
| routes/ | Route handlers: auth.py, users.py, patient.py |
| models/ | SQLite and MongoDB model helpers |
| schema/ | DB initialization scripts |
| templates/ | Jinja2 templates and layouts |
| static/ | Tailwind CSS and static assets |
| utils/ | Decorators, validators, sanitizers |
| seed_db_from_csv.py | Seeding utility |
| test.py | Unit tests |

---

## Author & context

| Field | Value |
|:-----|:------|
| Author | Ekemini Mbabah |
| Course / Purpose | COM7033 - Secure Software Development (educational) |
| Last updated | 2025-12-12 |

---

If you'd like, I can:
- Apply one more pass to add a small sample MongoDB document (assessment JSON) or an ERD table;
- Add a short "How to change port" snippet that shows how to set FLASK_RUN_PORT or edit app config;
- Commit this README on a new branch and open a PR for you to review (suggested branch: `readme/refactor-unique`).

Which of these (if any) would you like me to do next?
