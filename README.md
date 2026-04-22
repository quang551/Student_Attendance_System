# Student Attendance System (CLI Version)

---

## I. Introduction

The **Student Attendance System (SAS)** is a student attendance management system developed in **Python** using a **Layered Architecture**.

The application runs as a **Command Line Interface (CLI)** and supports the following features:

- User login / logout  
- Course, class, and session management  
- Student attendance tracking  
- Attendance correction  
- Report viewing  

Data is stored using **SQLite (`attendance.db`)** instead of plain `.txt` files.

---

## II. Project Structure
student_attendance/
│
├── cli/ # Command Line Interface layer
│ ├── init.py
│ ├── menu.py # Main menu navigation
│ ├── auth_cli.py # Login / logout interface
│ ├── attendance_cli.py # Attendance interaction
│ ├── Course_cli.py # Course management interface
│ ├── class_cli.py # Class management interface
│ ├── Session_cli.py # Session management interface
│ └── report_cli.py # Reporting interface
│
├── services/ # Business logic layer
│ ├── init.py
│ ├── auth_service.py # Authentication logic
│ ├── attendance_service.py # Attendance logic
│ ├── course_service.py # Course logic
│ ├── class_service.py # Class logic
│ ├── session_service.py # Session logic
│ ├── user_service.py # User logic
│ └── report_service.py # Reporting logic
│
├── repositories/ # Data access layer
│ ├── init.py
│ ├── user_repo.py # User queries
│ ├── attendance_repo.py # Attendance queries
│ ├── Course_repo.py # Course queries
│ ├── class_repo.py # Class queries
│ ├── session_repo.py # Session queries
│ └── db.py # Database queries
│
├── models/ # Data models
│ ├── init.py
│ ├── user.py # User model
│ ├── course.py # Course model
│ ├── class_model.py # Class model
│ ├── class_student.py # Class model
│ ├── session.py # Session model
│ └── attendance.py # Attendance model
│
├── attendance.db # SQLite database
├── init.py # Initialize schema
│
├── main.py # Entry point
├── requirements.txt # Dependencies
├── Dockerfile # Docker config
├── .dockerignore
├── .gitignore
├── docker-compose.yml
└── README.md # Documentation


---

## III. System Architecture

The system is divided into **4 main layers**:

### 1. CLI Layer (`cli/`)
- Receives user input  
- Displays menus  
- Calls corresponding services  

### 2. Service Layer (`services/`)
- Handles business logic  
- Validates data  
- Coordinates with repositories  

### 3. Repository Layer (`repositories/`)
- Communicates with SQLite database  
- Performs CRUD operations  

### 4. Model Layer (`models/`)
- Defines data structures (User, Course, Class, etc.)

---

## IV. Requirements

- Python >= 3.11  
- OS: Windows / macOS / Linux  

Install dependencies:

```bash
pip install -r requirements.txt

---

V. How to Run

Run directly:

```bash
python main.py

--- 

VI. Program Interface
The program runs entirely in a Command Line Interface (CLI), where users interact with the system through text-based menus.
After starting the application, the main interface will be displayed in the terminal, allowing users to choose actions based on their role (Student, Lecturer, or Admin).
1. Login Interface

===========================
Student Attendance System
===========================
 Login
Username:
Password:	
After a successful login, the system will authenticate the user and redirect them to the corresponding menu based on their role (Student, Lecturer, or Admin).

2.	Admin Menu
========================================================
                 ADMIN - Administrator
========================================================
1. Manage users
2. Manage courses
3. Manage classes
4. Manage sessions
5. Assign lecturer to class
6. Enroll student
7. View reports
0. Logout
Choose:

3.	Lecturer Menu
========================================================
                LECTURER - Lecturer
========================================================

1.	View Assigned classes
2.	View Student in a class
3.	View Sessions by class
4.    Take attendance
5. Edit attendance
6. View attendance by sessions
7. View Attendance by student
8. View reports
0. Logout
Choose:

4. Student Menu
========================================================
                 STUDENT - Student
========================================================
1. View my classes
2. View my attendance
0. Logout
Choose:	

---

VII. Main Features
 1. Authentication
- Login by role: Student, Lecturer ,Admin  

 2. Course & Class Management
- Create / update / delete courses  
- Create/ update/ detele classes  
- Assign lecturers  
- Add students to classes  

 3. Session Management
- Create / update / delete sessions  
- Manage class schedules  

4. Attendance Management
- Lecturers create attendance sessions, open, close, and take attendance  
- Store attendance status: Present / Absent / Late  	

5. Reporting
- View attendance by session  
- View attendance for each student  

6. Validation
- Validate user input data  
- Prevent logical errors  

7. Database
The system uses:
- SQLite database: attendance.db
Main tables:
- users  
- courses  
- classes  
- sessions  
- attendance  
- class_student  	

8. Testing: pytest –v

9. Docker (Optional)
Build the CLI image (context is the project root):
```bash
docker build -t sas-cli .
Run the CLI inside a disposable container:
docker run -it --rm sas-cli

10. Team Responsibilities
Tuấn	Core+ menu
Quang	Authentication & User
Vy	    Database & session
Linh	Course & class
Khuê	Attendance
Đức	    Report

11.Development tools
- IDE:Visual Studio Code / PyCharm
- Version control:GitHub
- Diagram tool: Draw.io
- Testing tool: pytest
- Optional: Docker
