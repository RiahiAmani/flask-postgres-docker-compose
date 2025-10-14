# Flask Task Manager with PostgreSQL

A task management web application with user authentication, built with Flask and PostgreSQL, fully containerized with Docker Compose.

## Features

- User registration and login system
- Create, complete, and delete tasks
- User-specific task lists
- PostgreSQL database with SQLAlchemy ORM
- pgAdmin for database management
- Fully containerized with Docker Compose

## Prerequisites

- Docker
- Docker Compose

## Quick Start

### 1. Create `.env` file

```env
# PostgreSQL
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=mydb

# Flask App
DATABASE_HOST=db
DATABASE_NAME=mydb
DATABASE_USER=user
DATABASE_PASSWORD=password
SECRET_KEY=your-secret-key-change-this-in-production

# pgAdmin
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=admin
```

### 2. Run the application

```bash
docker-compose up --build
```

### 3. Access services

- **Flask App**: http://localhost:5000
- **pgAdmin**: http://localhost:5050

## Using the Application

1. Open http://localhost:5000
2. Register a new account
3. Login with your credentials
4. Start adding tasks!

## Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild
docker-compose up --build
```

## pgAdmin Setup

1. Login at http://localhost:5050 with credentials from `.env`
2. Add server:
   - Host: `db`
   - Port: `5432`
   - Username/Password: from `.env`

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `password`: Hashed password

### Tasks Table
- `id`: Primary key
- `title`: Task description
- `completed`: Boolean status
- `created_at`: Timestamp
- `user_id`: Foreign key to users

## Tech Stack

- Python 3.10
- Flask 3.0.3
- Flask-SQLAlchemy 3.0.5
- Flask-Login 0.6.3
- PostgreSQL 16
- pgAdmin 8.12

---

**Note**: Change default credentials and SECRET_KEY before production use!
