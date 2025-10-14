# Flask Task Manager with PostgreSQL

A task management web application with user authentication, built with Flask and PostgreSQL, fully containerized with Docker Compose.

[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-devopsismail%2Fflask--task--manager-blue)](https://hub.docker.com/r/devopsismail/flask-task-manager)
[![Image Size](https://img.shields.io/badge/image%20size-265MB-brightgreen)](https://hub.docker.com/r/devopsismail/flask-task-manager)

## Features

- User registration and login system
- Create, complete, and delete tasks
- User-specific task lists
- PostgreSQL database with SQLAlchemy ORM
- pgAdmin for database management
- Fully containerized with Docker Compose
- Available on Docker Hub

## Prerequisites

- Docker
- Docker Compose

## Quick Start

### Option A: Pull from Docker Hub (Recommended)

```bash
# Pull the pre-built image
docker pull devopsismail/flask-task-manager:latest

# Update docker-compose.yml to use the Docker Hub image
# Change: build: .
# To: image: devopsismail/flask-task-manager:latest
```

### Option B: Build Locally

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

## Docker Hub

This image is available on Docker Hub:
- **Repository**: `devopsismail/flask-task-manager`
- **Tags**: `latest`, `v1.0`
- **Size**: 265MB
- **Pull Command**: `docker pull devopsismail/flask-task-manager:latest`

### Using the Docker Hub Image

Update your `docker-compose.yml`:

```yaml
services:
  web:
    image: devopsismail/flask-task-manager:latest
    # Remove or comment out: build: .
    container_name: flask_app
    ports:
      - "5000:5000"
    # ... rest of configuration
```

---

**Note**: Change default credentials and SECRET_KEY before production use!
