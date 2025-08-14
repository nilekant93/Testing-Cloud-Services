# Cloud Services Course – Backend

**This project is part of my summer 2025 training** and includes the following related repositories:  
- [Cloud Services Course – Student Tool](https://github.com/nilekant93/Cloud-Services-Course-student-tool-)  
- [Cloud Services Course – Admin](https://github.com/nilekant93/Cloud-Services-Course-admin-tool)  

## Overview
This is the **Backend** service for the Cloud Services Course project.  
It contains **all verification tests (Weeks 1–5)**, which are executed upon requests from the frontend **(Student Tool)**.  
It also provides APIs for user registration, login, progress tracking, and administrative functions such as viewing and deleting users.  


## Features
- **User Management**
  - Register and log in students
  - Secure authentication with JWT
  - Password hashing with Werkzeug
- **Assignment Verification**
  - Automated test execution for Weeks 1–5
  - Marks assignments as completed when tests pass
  - Returns detailed results (checks and messages)
- **Progress Tracking**
  - Stores weekly completion status in the database
  - Allows students to retrieve their progress

## Tech Stack
- [Python](https://www.python.org/)  
- [Flask](https://flask.palletsprojects.com/)  
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)  
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)  
- [Flask-CORS](https://flask-cors.readthedocs.io/)  
- [SQLite](https://www.sqlite.org/)  

## API Endpoints (Summary)

### Public Endpoints
- `GET /ping` — Health check endpoint (returns `"pong"`)
- `POST /register` — Register a new user  
- `POST /login` — Student login  

### Student Endpoints (JWT Required)
- `POST /mark_week_done` — Mark a specific week as completed  
- `GET /user/progress` — Retrieve student's weekly progress  
- `POST /receive` — Submit a deployment URL for automated testing (Weeks 1–5)

### Admin Endpoints
- `POST /admin/login` — Admin login  
- `GET /admin/users` — Get all users and their progress  
- `DELETE /admin/users/<user_id>` — Delete a specific user  

## Getting Started

### Prerequisites
- [Python 3.10+](https://www.python.org/downloads/)  
- [pip](https://pip.pypa.io/)  

### Installation
```bash
git clone https://github.com/nilekant93/cloud-services-course-backend.git
cd cloud-services-course-backend
cd backend
pip install flask flask_sqlalchemy flask_cors flask_jwt_extended python-dotenv werkzeug
````
### Running the Project
```bash
python app.py
````
### Environment Variables
This project includes a pre-configured .env file.
In this file, you must set the admin username and password that you want to use when logging into the Admin application.
```bash
ADMIN_USERNAME=<your-admin-username>
ADMIN_PASSWORD=<your-admin-password>
````

