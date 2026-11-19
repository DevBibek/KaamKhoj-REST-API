# KaamKhoj REST API

A Django REST Framework-based job portal API that connects companies directly with job seekers.

## About the Project

KaamKhoj is a job platform designed to make the job application process easier and more transparent.

Its main goal is to connect job seekers directly with companies without unnecessary intermediary fees.

Job seekers can explore available jobs, while verified companies can publish job opportunities and manage applications.

## Key Features

- User registration and authentication
- JWT-based authentication
- Role-based access for job seekers and companies
- Company verification system
- Job seeker profile management
- Company profile management
- Public job listing and search
- Job application management
- Application status management
- Pagination and filtering
- API throttling
- Redis caching
- API documentation with Swagger/OpenAPI

## Technologies Used

- Python
- Django
- Django REST Framework
- SQLite (development database)
- Redis
- Simple JWT
- drf-spectacular
- django-filter
- django-environ

## Project Architecture

The project follows a DDD-inspired layered architecture.

```text
src/
├── config/
│   └── settings/
│       ├── base.py
│       ├── development.py
│       ├── production.py
│       └── testing.py
│
├── infrastructure/
│   ├── users/
│   ├── jobs/
│   └── applications/
│
├── application/
├── domain/
├── presentation/
└── manage.py
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd KaamKhoj-REST-API
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Linux/macOS:

```bash
source venv/bin/activate
```

### 4. Install dependencies

Install the packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root.

Use `.env.example` as a reference and provide your own environment values.

Never commit your actual `.env` file or secret keys.

### 6. Run database migrations

```bash
cd src
python manage.py migrate
```

### 7. Start the development server

```bash
python manage.py runserver
```

The development server will be available at:

`http://127.0.0.1:8000/`

## API Documentation

The project uses drf-spectacular for OpenAPI schema generation and Swagger UI documentation.

Add the actual Swagger URL here after confirming your URL configuration.

## Project Status

Currently under development.

## Author

Developed as a backend development project to practice Django REST Framework, API architecture, authentication, caching, and testing.