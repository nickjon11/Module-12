# Module 12 – User Authentication and Calculation API

## Overview

This project builds on the Module 11 calculator application. It adds user registration, user login, and full CRUD operations for calculations.

Users can create an account, log in, and create, view, update, or delete calculation records. The application uses FastAPI, PostgreSQL, SQLAlchemy, Pydantic, Docker, and Pytest.

## Features

- User registration
- User login
- Secure password hashing
- Create calculations
- View all calculations
- View one calculation
- Update calculations
- Delete calculations
- PostgreSQL database
- Docker Compose support
- Automated testing with Pytest
- Swagger API documentation

## Technologies

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Psycopg
- Docker
- Docker Compose
- Pytest

## Project Setup

Clone the repository and enter the project directory:

```bash
git clone <your-module-12-repository-url>
cd module-12
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Run with Docker

Start the API and PostgreSQL database:

```bash
docker compose up -d --build
```

Check the containers:

```bash
docker compose ps
```

The API is available at:

```text
http://127.0.0.1:8001
```

Swagger documentation is available at:

```text
http://127.0.0.1:8001/docs
```

## Run Locally

Make sure the PostgreSQL Docker container is running:

```bash
docker compose up -d db
```

Start the FastAPI application:

```bash
uvicorn app.main:app --reload
```

Swagger documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Testing

Run all tests with:

```bash
python -m pytest -v
```

## API Endpoints

### General

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Application status |
| GET | `/health` | Health check |
| GET | `/add` | Add two numbers |
| GET | `/subtract` | Subtract two numbers |
| GET | `/multiply` | Multiply two numbers |
| GET | `/divide` | Divide two numbers |

### Users

| Method | Endpoint | Description |
|---|---|---|
| POST | `/users/register` | Register a new user |
| POST | `/users/login` | Log in an existing user |

### Calculations

| Method | Endpoint | Description |
|---|---|---|
| GET | `/calculations` | View all calculations |
| GET | `/calculations/{calculation_id}` | View one calculation |
| POST | `/calculations` | Create a calculation |
| PUT | `/calculations/{calculation_id}` | Update a calculation |
| DELETE | `/calculations/{calculation_id}` | Delete a calculation |

## Example User Registration

```json
{
  "username": "jonathan",
  "email": "jonathan@example.com",
  "password": "Password123!"
}
```

## Example User Login

```json
{
  "email": "jonathan@example.com",
  "password": "Password123!"
}
```

## Example Calculation

```json
{
  "a": 10,
  "b": 5,
  "type": "Add",
  "user_id": null
}
```