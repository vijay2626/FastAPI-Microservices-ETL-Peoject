FASTAPI MICROSERVICES + JWT + ETL + DOCKER + GITHUB ACTIONS
============================================================

Project name:
    FastAPI Microservices ETL Platform

What this project demonstrates:
    1. FastAPI microservices architecture
    2. API Gateway
    3. User registration and login
    4. Password hashing with bcrypt
    5. JWT access tokens
    6. PostgreSQL database
    7. SQLAlchemy ORM
    8. ETL pipeline:
         Extract -> Transform -> Load
    9. Docker and Docker Compose
   10. GitHub Actions CI
   11. Health-check endpoints
   12. Service-to-service HTTP communication
   13. Environment based configuration
   14. Protected endpoints using JWT

ARCHITECTURE
------------

                    +-------------------+
                    |    API Gateway    |
                    |     :8000         |
                    +---------+---------+
                              |
              +---------------+----------------+
              |                                |
              v                                v
      +---------------+                +---------------+
      | Auth Service  |                | User Service  |
      |     :8001     |                |     :8002     |
      +-------+-------+                +-------+-------+
              |                                |
              +---------------+----------------+
                              |
                              v
                       +-------------+
                       | PostgreSQL  |
                       |    :5432    |
                       +-------------+

                    ETL Service :8003
                          |
                          v
                    PostgreSQL

The API Gateway is the public entry point.
Auth Service handles registration/login/JWT.
User Service handles authenticated user APIs.
ETL Service executes a sample ETL pipeline.

PROJECT STRUCTURE
-----------------

fastapi_microservices_etl/
|
+-- services/
|   +-- auth_service/
|   |   +-- app/
|   |   |   +-- main.py
|   |   |   +-- database.py
|   |   |   +-- models.py
|   |   |   +-- schemas.py
|   |   |   +-- security.py
|   |   |   +-- requirements.txt
|   |   +-- Dockerfile
|   |
|   +-- user_service/
|   |   +-- app/
|   |   |   +-- main.py
|   |   |   +-- database.py
|   |   |   +-- models.py
|   |   |   +-- schemas.py
|   |   |   +-- security.py
|   |   |   +-- requirements.txt
|   |   +-- Dockerfile
|   |
|   +-- etl_service/
|       +-- app/
|       |   +-- main.py
|       |   +-- database.py
|       |   +-- pipeline.py
|       |   +-- requirements.txt
|       +-- Dockerfile
|
+-- gateway/
|   +-- app/
|   |   +-- main.py
|   |   +-- requirements.txt
|   +-- Dockerfile
|
+-- tests/
|   +-- test_auth.py
|
+-- .github/
|   +-- workflows/
|       +-- ci.yml
|
+-- docker-compose.yml
+-- .env.example
+-- .gitignore
+-- README.txt

REQUIREMENTS
------------

Install:
    Docker Desktop
    Git
    Python 3.12+ (optional for running outside Docker)

You do NOT need to install PostgreSQL locally if using Docker Compose.

QUICK START
-----------

1. Extract the project.

2. Open terminal in the project directory.

3. Create environment file:

    copy .env.example .env

Linux/macOS:

    cp .env.example .env

4. Start everything:

    docker compose up --build

5. Open:

    Gateway Swagger:
    http://localhost:8000/docs

    Auth Swagger:
    http://localhost:8001/docs

    User Swagger:
    http://localhost:8002/docs

    ETL Swagger:
    http://localhost:8003/docs

6. Health check:

    http://localhost:8000/health

LOGIN FLOW
----------

Register:

    POST http://localhost:8000/auth/register

JSON:

    {
        "email": "developer@example.com",
        "password": "Password123",
        "full_name": "Developer"
    }

Login:

    POST http://localhost:8000/auth/login

JSON:

    {
        "email": "developer@example.com",
        "password": "Password123"
    }

The response contains:

    {
        "access_token": "...",
        "token_type": "bearer"
    }

In Swagger, click "Authorize" and enter:

    Bearer YOUR_ACCESS_TOKEN

Then call:

    GET /users/me

JWT
---

JWT is used so the client does not need to send the username/password on
every request.

Token structure conceptually:

    header.payload.signature

The server signs the token using JWT_SECRET.

IMPORTANT:
    Change JWT_SECRET in production.

PASSWORD SECURITY
-----------------

Passwords are never stored as plain text.

The project uses:

    bcrypt

A password is converted into a secure hash before it is stored.

ETL PIPELINE
------------

The ETL service demonstrates:

    Extract
        |
        v
    Transform
        |
        v
    Load

Sample source data:

    raw sales records

Transformations include:
    - normalize customer names
    - validate amount
    - convert date
    - calculate status
    - remove invalid records

The transformed records are inserted into PostgreSQL.

Run ETL:

    POST http://localhost:8003/etl/run

Check ETL status:

    GET http://localhost:8003/etl/status

ETL output is stored in:

    etl_records

DOCKER
------

Start:

    docker compose up --build

Run in background:

    docker compose up -d --build

Stop:

    docker compose down

Stop and remove volumes:

    docker compose down -v

View services:

    docker compose ps

View logs:

    docker compose logs -f

View one service:

    docker compose logs -f auth_service

GITHUB ACTIONS
--------------

The workflow is located at:

    .github/workflows/ci.yml

It runs on:
    - push
    - pull request

The CI pipeline:
    1. checks out source code
    2. installs Python
    3. installs dependencies
    4. runs tests
    5. builds Docker images

For a real production deployment, the workflow can be extended to:
    - build images
    - push to Docker Hub / GHCR
    - deploy to AWS ECS
    - deploy to Kubernetes
    - run migrations

DATABASE
--------

PostgreSQL is used.

Database:
    microservices_db

Username:
    postgres

Password:
    postgres

Port:
    5432

Tables are created automatically by the sample services.

For production:
    use Alembic migrations instead of create_all.

SERVICE PORTS
-------------

Gateway:
    8000

Auth:
    8001

User:
    8002

ETL:
    8003

PostgreSQL:
    5432

REDIS
-----

This sample project intentionally keeps Redis optional to make the project
easy to run.

For a larger production architecture Redis can be added for:
    - caching
    - Celery/RQ queues
    - rate limiting
    - background jobs

MICROSERVICE DESIGN
-------------------

Auth Service:
    - register
    - login
    - JWT creation
    - password hashing

User Service:
    - get current user
    - list users
    - authenticated user operations

ETL Service:
    - execute ETL
    - transform source records
    - persist transformed data

Gateway:
    - public API entry point
    - routes requests to internal services

PRODUCTION IMPROVEMENTS
-----------------------

For an enterprise production implementation, add:

    1. Alembic database migrations
    2. Secret Manager / Vault
    3. HTTPS/TLS
    4. API rate limiting
    5. Redis
    6. Celery/Kafka/RabbitMQ
    7. Centralized logging
    8. OpenTelemetry tracing
    9. Prometheus/Grafana
   10. Kubernetes
   11. Separate databases per microservice
   12. API versioning
   13. Refresh tokens
   14. Token revocation
   15. Role-based access control
   16. Automated security scanning

IMPORTANT MICROSERVICE PRINCIPLE
--------------------------------

A true production microservice architecture normally gives each service
ownership of its own database/schema.

This demo uses one PostgreSQL container and separate service tables to keep
local development simple.

For interviews, explain that production would normally isolate data ownership
and use asynchronous communication where appropriate.

TESTING
-------

Install dependencies locally if required:

    pip install -r services/auth_service/app/requirements.txt

Run:

    pytest -q

Or run tests inside a suitable CI environment.

EXAMPLE API CALLS
-----------------

Register:

    curl -X POST http://localhost:8000/auth/register ^
      -H "Content-Type: application/json" ^
      -d "{\"email\":\"developer@example.com\",\"password\":\"Password123\",\"full_name\":\"Developer\"}"

Login:

    curl -X POST http://localhost:8000/auth/login ^
      -H "Content-Type: application/json" ^
      -d "{\"email\":\"developer@example.com\",\"password\":\"Password123\"}"

Get profile:

    curl http://localhost:8000/users/me ^
      -H "Authorization: Bearer YOUR_TOKEN"

Run ETL:

    curl -X POST http://localhost:8003/etl/run

TROUBLESHOOTING
---------------

If port 5432 is already in use:
    Change the PostgreSQL host port in docker-compose.yml.

If a service cannot connect to PostgreSQL:
    Wait for PostgreSQL to become healthy and restart:

        docker compose restart

If Docker build has stale layers:

    docker compose build --no-cache

Then:

    docker compose up

SECURITY NOTE
-------------

This is an interview/learning-ready project, not a complete production
security baseline.

Never commit:
    .env
    private keys
    production passwords
    cloud credentials
    real JWT secrets

Use environment variables or a secret manager in production.

END
