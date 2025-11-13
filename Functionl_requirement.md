# Secure Software Development Documentation  
### Stroke Prediction & Patient Management Flask Application

This project is a secure Python Flask web application designed for healthcare environments. It enables doctors and nurses to store, manage, update, and retrieve patient information from a stroke prediction dataset. The system analyzes demographic, medical, and lifestyle factors to estimate stroke risk.

The application follows **Secure Software Development Lifecycle (SSDLC)** principles, integrating:  
- User authentication (RBAC)  
- Encrypted data storage  
- Input validation & sanitization  
- Secure session management  
- Activity logging  
- Compliance-aligned practices (GDPR/HIPAA-like)

---

## 📌 Stakeholders & Access Rights

| Stakeholder | Description | Access Rights |
|------------|-------------|---------------|
| **Doctor** | Full clinical privileges | Full CRUD, run predictions, manage nurse access |
| **Nurse** | Assist doctors | Limited CRUD (no delete, no prediction) |
| **Patient** | System user | Read-only access to personal data |
| **Admin (IT Staff)** | System overseer | Manage users, roles, logs, system settings |

---

## 🎯 System Goals

| Goal | Description |
|------|-------------|
| **Efficient Patient Data Management** | Centralized CRUD operations for patient info. |
| **Secure Data Storage & Access Control** | Authentication, authorization, encryption. SQLite for auth, MongoDB for records. |
| **Stroke Risk Prediction** | ML model for stroke risk analysis. |
| **Regulatory Compliance** | Privacy and security aligned with GDPR/HIPAA principles. |
| **Clinical Workflow Optimization** | Seamless staff collaboration using RBAC. |
| **Maintainability & Scalability** | Modular Flask design, testing, Git/GitHub workflow. |

---

## 🔄 System Processes & Logic

### **1. User Authentication**
- Secure login with bcrypt hashing  
- Role-based access control  
- Session token management  
- CSRF protection  
- Output: Authenticated user session  

### **2. Patient Data Management (CRUD)**  
- **Create**: Add new patient records  
- **Read**: View patient medical details  
- **Update**: Modify existing patient data  
- **Delete**: Admin-only removal  
- All operations logged and validated  

### **3. Stroke Risk Prediction**
- Doctor selects patient  
- ML model processes features (age, BMI, hypertension, etc.)  
- Displays risk score with insights  
- Results stored securely  

### **4. Audit & Logging**
- Logs login attempts, CRUD changes, prediction actions  
- Admin-only access  
- Encrypted, read-only logs  

---

## 👥 User Requirements

| User | Requirement | Description |
|------|-------------|-------------|
| **Doctor** | Manage patient data | Create, update, delete records |
| **Doctor** | Generate predictions | Run stroke risk model |
| **Nurse** | Update vitals | Limited CRUD |
| **Patient** | Secure access | View personal medical data |
| **Admin** | System oversight | Manage roles, logs, backups |

---

## 🛠️ Technical Requirements

| Category | Requirement | Purpose |
|---------|-------------|---------|
| **Language** | Python | Backend logic |
| **Framework** | Flask | Web framework |
| **Frontend** | HTML, CSS | User interface |
| **Databases** | SQLite, MongoDB | Auth + patient data |
| **Security** | bcrypt, CSRF, HTTPS | Protection mechanisms |
| **Version Control** | Git & GitHub | Collaboration |
| **Deployment** | Flask dev server | Local testing |
| **ML Model** | Stroke prediction model | Analysis engine |

---

## 📂 Functional Requirements

### **Authentication & Authorization**
- Secure registration & login  
- Email uniqueness check  
- Password hashing  
- **Two-Factor Authentication (2FA)**  
- Password recovery  
- Role-Based Access Control  
- Session timeout  

### **Patient Management**
- CRUD operations  
- Audit trails  
- Encrypted storage  

### **Stroke Prediction**
- ML model execution  
- Display risk score  
- Store prediction history  

### **Security**
- Input validation  
- XSS, SQLi, CSRF protection  
- Encrypted sensitive data  
- Regular database backups  

### **System Administration**
- Manage users and roles  
- System monitoring  
- Log reviewing  

---

## 🧪 Testing & Version Control

| Test Type | Purpose |
|-----------|----------|
| **Unit Tests** | Validate functions/modules |
| **Integration Tests** | Validate combined workflows |
| **Git Version Control** | Branching, commits, pull requests |

---

# 📘 Use Cases

## **1. User Registration**
**Users:** Patient, Doctor, Nurse, Admin  
**Flow:**  
1. Enter details  
2. Validate input  
3. Check email existence  
4. Store hashed password  
5. Send verification email  
6. Activate account  

**Security:** bcrypt, input sanitization, HTTPS, audit logging.

---

## **2. User Login**
**Flow:**  
1. Enter email/password  
2. Validate credentials  
3. MFA verification  
4. Redirect to dashboard  

**Security:**  
- MFA  
- bcrypt  
- login attempt limits  
- HTTPS  

---

## **3. Patient Record Management**
**Users:** Doctor, Nurse  
**Flow:**  
- Add/edit/view/delete patient records  
- Log actions  

**Security:** RBAC, encryption, input validation.

---

## **4. Stroke Prediction**
**User:** Doctor  
**Flow:**  
- Select patient  
- Run prediction  
- View/Store results  

**Security:** Encrypted endpoints, secure storage.

---




