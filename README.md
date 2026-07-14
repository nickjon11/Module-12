# Module 10 – Secure User Model, Pydantic Validation, Database Testing, and Docker Deployment

## Overview

This project extends the FastAPI Calculator application from Module 9 by adding a secure user management system using SQLAlchemy and Pydantic.

New features include:

- Secure SQLAlchemy User model
- Password hashing using Argon2 (pwdlib)
- Pydantic validation
- PostgreSQL database integration
- User CRUD functionality
- Unit and integration testing
- Docker containerization
- GitHub Actions CI/CD
- Docker Hub deployment

---

## Technologies Used

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- pwdlib (Argon2)
- Pytest
- Docker
- Docker Compose
- GitHub Actions

---

## Docker Login

Due to Github, you have to supply your own username and token. You can manually change it in 'github\workflows\ci-cd.yml' and in line 73-74, replace: 'DOCKERHUB_USERNAME' and 'DOCKERHUB_TOKEN' with your own. 

---

