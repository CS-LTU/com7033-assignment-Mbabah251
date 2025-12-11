# Hospital Management System

A Flask-based web application for managing patient records and user authentication in a healthcare environment.

## Features

- User authentication (Doctor, Nurse, Patient roles)
- Patient data management with CRUD operations
- SQLite for user authentication
- MongoDB for patient records
- Role-based access control
- CSRF protection
- Password hashing with werkzeug
- Input validation and sanitization

## Installation

### Requirements
- Python 3.8+
- SQLite3
- MongoDB

### Setup

1. Clone the repository
```bash
git clone <repository-url>
cd com7033-assignment-Mbabah251
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Configure environment variables
Create a `.env` file in the root directory:
```
SECRET_KEY=your-secret-key-here
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGO_DB=SecureApp12
```

4. Run the application
```bash
python app.py
```

The app will run on `http://localhost:5000`

## Project Structure

```
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Project dependencies
├── routes/               # Route handlers
│   ├── auth.py          # Authentication routes
│   ├── users.py         # User management routes
│   └── patient.py       # Patient management routes
├── models/              # Database models
│   ├── user.py
│   ├── patient.py
│   └── mongo/          # MongoDB models
├── templates/          # HTML templates
├── static/             # CSS and static files
├── utils/              # Utility functions
└── test.py            # Unit tests
```

## Usage

### User Registration
1. Navigate to `/signup`
2. Select your role (Doctor, Nurse, or Patient)
3. Fill in required information
4. Create account with strong password (8+ chars, uppercase, lowercase, digit, special char)

### Login
1. Go to `/login`
2. Enter email and password
3. Access dashboard based on your role

### Patient Management
- View patient records
- Add new patient information
- Update existing records
- Delete records (Doctor only)

## Security Features

- **CSRF Protection**: All forms are protected against Cross-Site Request Forgery attacks
- **Password Hashing**: Passwords are hashed using werkzeug.security
- **Input Validation**: Email format and password strength validation
- **Database Separation**: User auth in SQLite, patient data in MongoDB
- **Role-Based Access**: Different permissions for Doctor, Nurse, and Patient roles

## Testing

Run unit tests:
```bash
python test.py
```

Tests cover:
- User creation and authentication
- Database operations
- Route functionality
- Error handling

## Technologies Used

- Flask 3.1.2
- SQLite
- MongoDB
- Flask-WTF (CSRF protection)
- Werkzeug (password hashing)

## License

Created for COM7033 Secure Software Development assignment
