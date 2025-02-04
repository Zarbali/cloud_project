readme_content = """Task Management System (Flask + React + Redis)

# Task Management System (Flask + React + Redis)

A full-stack Task Management System built using Flask, React, and Redis. The system includes authentication, task management, user roles, and data caching using Redis.

📌 PROJECT OVERVIEW:
Task Manager is a full-stack web application allowing users to manage tasks, create accounts, and authenticate via JWT. 



---

## Project Functionalities

📍 Frontend URL: 
http://localhost:3000/index.html

✅ User Authentication:
- Users can **register** and **login**.
- Admins have extra permissions.
- Authentication via **JWT tokens**.

✅ Task Management:
- **Create, Read, Update, Delete (CRUD)** tasks.
- **Admins** can view all users' tasks.
- **Users** can only manage their own tasks.

✅ Redis Caching:
- Frequently fetched tasks are **cached** in Redis.
- Admin task list and user-specific tasks are stored with a 60s TTL.
- Cached data automatically refreshes when tasks are modified.

✅ PostgreSQL Database:
- Stores all users and tasks.
- Accessible via **PgAdmin** (instructions below).

1️⃣ Make sure **PostgreSQL** is installed and running.

2️⃣ Connect to **PgAdmin**:
   - Open **PgAdmin4**
   - Click **Add New Server**
   - Enter the following details:
     - Name: cloud_db
     - Hostname: **localhost**
     - Port: **5432**
     - Username: postgres
     - Password: postgres
     - Database: cloud_db

        DB_HOST=db
      - DB_PORT=5432
      - DB_USER=postgres
      - DB_PASSWORD=postgres
      - DB_NAME=cloud_db
   - Click **Save** to connect.
  
✅ API Documentation:
- Uses **Swagger** for API testing.
- Access at: 
  👉 http://localhost:5000/apidocs/

### User Authentication
- Users can register and log in (`/register.html`, `/login.html`).
- Admins can log in separately via (`/admin_login.html`).
- JWT Authentication is used for secured endpoints.

### Task Management
- Users can:
  - Create, update, and delete their tasks.
  - Search for tasks using keywords.
  - Mark tasks as completed.
- Admins can:
  - View tasks of all users.
  - Delete any task.

### Admin Panel
- Admins can manage users & tasks via `/admin_panel.html`.

### Redis Caching
- Tasks are cached in Redis for faster retrieval.
- Cached tasks are stored for 60 seconds before refreshing.

### REST API with Swagger
- Swagger UI documentation available at:
  - `http://localhost:5000/api/docs`
- The API supports:
  - CRUD operations on tasks
  - User authentication
  - Admin controls

## Installation & Setup
### Step 1: Clone the Repository
```sh
git clone https://github.com/Zarbali/cloud_project.git
cd task-manager
or just setup zip.file

 2: Run with Docker
docker-compose up --build

Flask API: http://localhost:5000
Redis Server: Runs inside Docker (redis:6379)
React Frontend: http://localhost:3000

Testing Redis
docker exec -it redis-container-name redis-cli
127.0.0.1:6379> keys *
127.0.0.1:6379> get tasks_admin

127.0.0.1:6379> FLUSHALL

**How to Test the Application**
Test Authentication
Register a user: Go to http://localhost:3000/register.html.
Log in: Go to http://localhost:3000/index.html.
Use an admin account to access: http://localhost:3000/admin_login.html.
command for admin role "your directory where the project"> docker exec -it flask_app python /app/src/admin_setup.py

Test Task CRUD
Create a task from the Task Manager.
Edit task via the task list.
Delete task (Only admins can delete all tasks).


Tech Stack
Backend: Flask, SQLAlchemy, JWT Authentication
Frontend: React.js, HTML, CSS, JavaScript
Database: PostgreSQL / SQLite
Caching: Redis
Deployment: Docker

**Contributors**

Arif Zarbaliyev
Student ID : 48232
GitHub: https://github.com/Zarbali

Bozhena Hlotko
Student ID: 47122
GitHub: https://github.com/bozhenamay

Danylo Bevziuk
Student ID: 45564
GitHub: https://github.com/Abemiy