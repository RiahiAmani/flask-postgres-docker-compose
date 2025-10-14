# Flask + PostgreSQL + Docker Compose

A simple Flask web application with PostgreSQL database and pgAdmin, fully containerized with Docker Compose.

## Features

- Flask web app with contact form
- PostgreSQL database for data persistence
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
- **Contact Form**: http://localhost:5000/contact
- **pgAdmin**: http://localhost:5050

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

## Tech Stack

- Python 3.10
- Flask 3.0.3
- PostgreSQL 16
- pgAdmin 8.12

---

**Note**: Change default credentials before production use!
