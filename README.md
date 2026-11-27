# Campus Connect – Clubs and Events Management Platform

## 1. Project Overview

**Campus Connect** is a web-based platform designed to simplify the management of university clubs, student memberships and campus events.

In a university, students often need to find clubs, apply for memberships and register for events. Club coordinators need a way to manage members, organize events and track attendance.

Campus Connect brings these activities together in one platform.

The application provides three types of users:

- **Admin:** Manages coordinators and creates clubs.
- **Coordinator:** Manages club information, membership applications and events.
- **Student:** Explores clubs, applies for memberships and registers for events.

The main goal is to make campus activities easier to organize, manage and participate in.

1. Project and Team
Project Name: Campus Connect – Clubs and Events Management Platform
Team Members: Amrutha ,Naidile ,Supriya

## 2. Team Contributions

| Team Member | API Contributions |
| ----------- | ----------------- |
| Amruta      | A2, E6–E10        |
| Supriya     | A3, E1–E5         |
| Naidile     | A1, E11–E15       |
**

Day1:


Amruta:  


Naidile: creating the files and planning how to do and completing the A1   
          creating repo in dockerhub . dockerfilr ,deploy,yml . 

          
Supriya: Created tables, set up project dependencies and implemented -create_token, verify_token , refresh token ,README.md file and setup the base of the project


Day 2:

Amruta :     

Naidile: completing the E11, E12, E13     
          instance launching .

Supriya:  Implemented  coordinatior account , to create a new campus club and dipslay the events of the club (E1 ,E2, E3)   


Day 3:


Amruta :


Naidile:E14 and E15 completing with checking the swager of  my endpoints 
          ec2 working 

Supriya: Implemented  display clubs with the club id and update details of a club (E4,E5) .Testing all endpoints in swagger and final checks 


## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| FastAPI | Used to build the backend APIs |
| SQLite | Stores application data |
| SQLAlchemy | Connects Python code with the database |
| Pydantic | Validates incoming data |
| JWT | Handles user authentication |
| Argon2 | Securely hashes passwords |
| Docker | Packages the application for deployment |
| GitHub Actions | Automates the build and deployment process |
| AWS EC2 | Hosts the application |
| Swagger UI | Allows users to explore and test APIs |

## 4. User Roles and Functionalities

### Admin

The Admin manages the overall platform.

- Creates coordinator accounts.
- Creates campus clubs.
- Assigns coordinators to clubs.

### Coordinator

The Coordinator manages the activities of an assigned club.

- Updates club information.
- Views club members.
- Approves or rejects membership applications.
- Creates events.
- Views event participants.
- Marks student attendance.

### Student

Students use the platform to participate in campus activities.

- Registers and logs in.
- Views available clubs.
- Applies to join clubs.
- Views available events.
- Registers for events.
- Cancels event registrations.
- Views event participation history.

## 5. API Documentation

The application provides 18 APIs divided into Authentication APIs and Project APIs.

### 5.1 Authentication APIs

These APIs handle user registration, login and token management.

| API ID | Method | Endpoint | Description |
|---|---|---|---|
| A1 | POST | `/auth/register` | Registers a new user |
| A2 | POST | `/auth/login` | Logs in a user and generates tokens |
| A3 | POST | `/auth/refresh` | Generates a new access token using a refresh token |

### 5.2 Project APIs

These APIs handle clubs, memberships, events and student participation.

| API ID | Method | Endpoint | Description |
|---|---|---|---|
| E1 | POST | `/coordinators` | Creates a coordinator account |
| E2 | POST | `/clubs` | Creates a new campus club |
| E3 | GET | `/clubs` | Displays all available clubs |
| E4 | GET | `/clubs/{club_id}` | Displays details of a particular club |
| E5 | PATCH | `/clubs/{club_id}` | Updates club information |
| E6 | POST | `/clubs/{club_id}` | Applies to join a club |
| E7 | PATCH | `/clubs/{club_id}/members/{member_id}` | Approves or rejects a membership application |
| E8 | GET | `/clubs/{club_id}` | Retrieves club members |
| E9 | POST | `/events` | Creates a new event |
| E10 | GET | `/events` | Displays all events |
| E11 | POST | `/events/{event_id}/register` | Registers a student for an event |
| E12 | DELETE | `/events/{event_id}/register` | Cancels an event registration |
| E13 | PATCH | `/events/{event_id}/attendance` | Marks student attendance |
| E14 | GET | `/events/{event_id}/participants` | Displays event participants |
| E15 | GET | `/students/participation` | Displays student participation history |


### 6.1 Users

Stores information about registered users.

| Column | Description |
|---|---|
| id | Unique user ID (Primary Key) |
| username | User's name |
| role | User role |
| email | User's email address |
| password | Hashed password |

### 6.2 Clubs

Stores information about university clubs.

| Column | Description |
|---|---|
| id | Unique club ID (Primary Key) |
| name | Club name |
| description | Description of the club |
| category | Club category |
| coordinator_id | Coordinator's user ID (Foreign Key) |

### 6.3 Clubs_members

Stores student membership applications.

| Column | Description |
|---|---|
| id | Unique membership ID (Primary Key) |
| club_id | Club ID (Foreign Key) |
| stu_id | Student ID (Foreign Key) |
| status | Membership status |

The membership status can be pending, approved or rejected.

### 6.4 Events

Stores information about events organized by clubs.

| Column | Description |
|---|---|
| id | Unique event ID (Primary Key) |
| club_id | Club ID (Foreign Key) |
| title | Event title |
| description | Event description |
| venue | Event location |
| event_date | Date of the event |
| regis_deadline | Last date for registration |
| max_cap | Maximum event capacity |

### 6.5 Event_regis

Stores student event registration and attendance information.

| Column | Description |
|---|---|
| id | Unique registration ID (Primary Key) |
| event_id | Event ID (Foreign Key) |
| stu_id | Student ID (Foreign Key) |
| status | Registration status |
| attended | Indicates whether the student attended |

## 7. Project Structure

```text
campus-connect/
│
├── main.py
├── AM_functions.py
├── NA_functions.py
├── SU_functions.py
├── requirements.txt
├── dockerfile
├── .gitignore
├── campus.db
│
└── .github/
    └── workflows/
        └── deploy.yml
```

### File Descriptions

| File | Purpose |
|---|---|
| `main.py` | Defines the FastAPI application and API endpoints |
| `AM_functions.py` | Contains database models, login and club-related functions |
| `NA_functions.py` | Contains user registration, event registration and attendance functions |
| `SU_functions.py` | Contains authentication, token and coordinator management functions |
| `requirements.txt` | Lists the Python dependencies |
| `dockerfile` | Contains instructions to build the Docker image |
| `.gitignore` | Specifies files Git should ignore |
| `campus.db` | SQLite database |
| `deploy.yml` | Defines the GitHub Actions deployment workflow |

## 8. How to Run the Project Locally

Follow these steps to run Campus Connect on your computer.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Amruta02-stack/campus-connect.git
```

### Step 2: Navigate to the Project Folder

```bash
cd campus-connect
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Start the Application

```bash
uvicorn main:app --reload
```

### Step 7: Open Swagger UI

Open the following address in your browser:

```text
http://127.0.0.1:8000/docs
```

You can now explore and test the APIs.

## 9. Docker Setup

Docker is used to package the application so it can run in a consistent environment.

### Build the Docker Image

```bash
docker build -t campus-connect -f dockerfile .
```

### Run the Docker Container

```bash
docker run -d -p 8000:8000 --name campus-connect campus-connect
```

Access the application through:

```text
http://localhost:8000/docs
```

## 10. CI/CD Pipeline

Campus Connect uses GitHub Actions to automate the application build and deployment process.

CI/CD stands for Continuous Integration and Continuous Deployment.

This means that when code is pushed to the configured GitHub branch, the workflow can automatically build the Docker image and deploy it to the server.

### Deployment Workflow

1. A team member pushes code to the `main` branch.
2. GitHub Actions checks out the latest repository code.
3. Docker logs in to Docker Hub using GitHub Secrets.
4. A Docker image is built.
5. The image is pushed to Docker Hub.
6. GitHub Actions connects to the AWS EC2 instance through SSH.
7. The new image is pulled and the application container is restarted.


### GitHub Secrets

The workflow uses the following secrets:

| Secret | Purpose |
|---|---|
| `DOCKERHUB_USERNAME` | Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token |
| `EC2_HOST` | EC2 server address |
| `EC2_USER` | EC2 login username |
| `EC2_SSH_KEY` | SSH private key used for deployment |
|  `SECRET_KEY` | secret key |

## 11. Project Links

**GitHub Repository:**

https://github.com/Amruta02-stack/campus-connect

**Live Application:**

Add the deployed AWS EC2 application URL here.


## 14. Conclusion

Campus Connect provides a centralized solution for managing university clubs, student memberships and campus events.

By bringing administrators, coordinators and students onto one platform, it simplifies club management and event participation.

The project demonstrates the use of backend development, database management, authentication, API development, containerization and automated deployment.
