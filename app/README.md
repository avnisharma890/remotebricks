FastAPI User Management System

Overview

This is a user management system built with FastAPI and MongoDB. The application includes functionalities such as user registration, login with JWT authentication, and secure access to protected routes. Swagger UI is integrated for API documentation and testing.


Features

User Registration: Register users with email, username, and password.
JWT Authentication: Secure login and token generation.
Protected Routes: Access user-specific data using JWT.
CRUD Operations:
Link external IDs to users.
Fetch user data with related IDs.
Delete user and related data.
API Documentation: Swagger UI available at /docs.


Technologies Used

Backend Framework: FastAPI
Database: MongoDB
Authentication: JSON Web Tokens (JWT)
Password Management: Passlib (bcrypt hashing)
API Documentation: Swagger UI
HTTP Client Testing: cURL/Postman


Installation and Setup

Prerequisites

Python 3.10+
MongoDB installed and running locally or on a server.
A package manager like pip or conda.

Installation
Clone the repository:

bash
Copy code
git clone <repository_url>
cd <repository_directory>

Create a virtual environment:

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

bash
Copy code
pip install -r requirements.txt

Configure MongoDB connection in database.py:

python
Copy code
MONGODB_URL = "mongodb://localhost:27017"


Running the Application

Start the MongoDB server:

bash
Copy code
mongod
Run the FastAPI application:

bash
Copy code
uvicorn main:app --reload

Open Swagger UI: Navigate to http://127.0.0.1:8000/docs.


API Endpoints

Public Endpoints
Register a User
POST /register
Request Body:

json
Copy code
{
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpassword"
}

Login
POST /token
Form Data:

username (email)
password
grant_type: password

Protected Endpoints
Link External ID
POST /link-id
Request Body:

json
Copy code
{
    "external_id": "12345"
}
Get User Data
GET /user-data

Delete User
DELETE /user


Testing the Application

Use Swagger UI at /docs for API testing.
Use Postman or curl for manual API requests.
Example curl command for login:

bash
Copy code
curl -X POST "http://127.0.0.1:8000/token" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=test@example.com&password=testpassword&grant_type=password"