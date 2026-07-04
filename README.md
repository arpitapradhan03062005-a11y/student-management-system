# 🎓 Student Management System

A full-stack, role-based Student Management System built with Django — featuring attendance tracking, grade/result management, auto-generated smart ID cards, and secure role-based dashboards for Admins, Teachers, and Students.

🔗 **Live Demo:** [ArpitaPradhan.pythonanywhere.com](https://ArpitaPradhan.pythonanywhere.com)

---

## ✨ Features

### 👥 Role-Based Access Control
- Three distinct roles — **Admin**, **Teacher**, and **Student** — each with their own dashboard and permissions
- Admins and Teachers have full access to student records; Students can only view their own data
- Secure, allow-list based permission checks (fail-closed by default — new users have zero access until a role is assigned)

### 🎓 Student Records
- Full CRUD (Create, Read, Update, Delete) for student profiles
- Search and filter by name, email, roll number, department, semester, and gender
- Paginated student list for performance at scale
- Each student record includes photo, signature, blood group, and emergency contact

### 🪪 Smart ID Card Generation
- Auto-generated PDF student ID cards using `reportlab`
- Includes photo, department, semester, blood group, signature, and a scannable QR code

### 📅 Attendance Tracking
- Teachers/Admins can mark daily attendance by department
- Pre-fills existing attendance when re-opening a date (supports corrections)
- Students see their own attendance history and live attendance percentage on their dashboard

### 📝 Grades & Results
- Subject and exam-type based result entry (Midterm / Final / Assignment)
- Auto-filtered by department and semester when entering marks
- Students get a personal report card with per-subject and overall percentage

### 🔒 Security
- Secrets (API keys, email credentials) managed via environment variables, never hardcoded
- Role-based access control enforced at the view level, not just hidden in the UI
- Protected against IDOR (Insecure Direct Object Reference) vulnerabilities on sensitive endpoints
- Password validation enforced on registration

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Database:** SQLite
- **Frontend:** Django Templates, Bootstrap
- **PDF/QR Generation:** ReportLab, qrcode
- **Environment Management:** python-decouple
- **Deployment:** PythonAnywhere

---

## 📸 Screenshots

> _Add screenshots of your Admin dashboard, Student dashboard, and ID card here!_
<img width="959" height="472" alt="image" src="https://github.com/user-attachments/assets/cd2a6e23-e805-48b2-84c1-f1e7db9716fd" />
<img width="959" height="482" alt="image" src="https://github.com/user-attachments/assets/2f18921a-5d72-4ab5-9d33-c7852ac9ebf7" />
<img width="959" height="449" alt="image" src="https://github.com/user-attachments/assets/c56265a6-9647-480e-a178-b07cda0875b1" />
<img width="353" height="266" alt="image" src="https://github.com/user-attachments/assets/5e7ecdf7-09f3-4da8-9ded-6cf64d0d1fd3" />
<img width="959" height="438" alt="image" src="https://github.com/user-attachments/assets/8e6fb396-cff0-492c-ac94-be7d2b8405f8" />

---

## 🚀 Getting Started Locally

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/arpitapradhan03062005-a11y/student-management-system.git
cd student-management-system

# Create and activate a virtual environment
python -m venv myenv
myenv\Scripts\activate      # Windows
source myenv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root with the following:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Run migrations and start the server

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

---

## 👤 Roles & Permissions

| Role    | Permissions                                                        |
|---------|---------------------------------------------------------------------|
| Admin   | Full access — manage students, attendance, results, and users       |
| Teacher | Full access to students, attendance, and results (no user management)|
| Student | View-only access to their own profile, attendance, and results       |

> Roles are assigned via Django's built-in Groups (`/admin/`) after a user registers.

---

## 📄 License

This project is open source and available for educational purposes.

---

## 🙋‍♀️ Author

Built by Arpita Pradhan as a learning project to explore full-stack Django development, role-based access control, and production deployment.
