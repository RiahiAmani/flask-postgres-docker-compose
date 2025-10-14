# Flask Task Manager

A task management web app with user authentication, built with Flask and PostgreSQL.

[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-devopsismail%2Fflask--task--manager-blue)](https://hub.docker.com/r/devopsismail/flask-task-manager)
[![Image Size](https://img.shields.io/badge/image%20size-265MB-brightgreen)](https://hub.docker.com/r/devopsismail/flask-task-manager)

## Features

- 🔐 User authentication (register/login)
- ✅ Task management (create/complete/delete)
- 🗄️ PostgreSQL database
- 🛠️ pgAdmin for database management

## Quick Start

### 1. Pull the Image

```bash
docker pull devopsismail/flask-task-manager:latest
```

### 2. Create Project Files

**Create `.env` file:**

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
SECRET_KEY=your-secret-key-change-this

# pgAdmin
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=admin
```

**Create `docker-compose.yml`:**

```yaml
version: '3.9'

services:
  web:
    image: devopsismail/flask-task-manager:latest
    container_name: flask_app
    ports:
      - "5000:5000"
    depends_on:
      db:
        condition: service_healthy
    env_file:
      - .env
    networks:
      - flask_network
    restart: on-failure

  db:
    image: postgres:16
    container_name: postgres_db
    restart: always
    env_file:
      - .env
    volumes:
      - pgdata:/var/lib/postgresql/data
    networks:
      - flask_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 5s
      timeout: 5s
      retries: 5

  pgadmin:
    image: dpage/pgadmin4:8.12
    container_name: pgadmin
    restart: always
    env_file:
      - .env
    ports:
      - "5050:80"
    depends_on:
      - db
    networks:
      - flask_network

volumes:
  pgdata:

networks:
  flask_network:
    driver: bridge
```

### 3. Run

```bash
docker-compose up -d
```

### 4. Access

- **App**: http://localhost:5000
- **pgAdmin**: http://localhost:5050

## Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f web

# Restart
docker-compose restart

# Update to latest
docker pull devopsismail/flask-task-manager:latest
docker-compose up -d --force-recreate
```

## Usage

1. Open http://localhost:5000
2. Register a new account
3. Login and start managing tasks!

### pgAdmin Setup

1. Go to http://localhost:5050
2. Login: `admin@example.com` / `admin`
3. Add server:
   - Host: `db`
   - Port: `5432`
   - Username: `user`
   - Password: `password`

## Build from Source (Optional)

```bash
git clone https://github.com/iskilicaslan61/flask-postgres-docker-compose.git
cd flask-postgres-docker-compose

# Change in docker-compose.yml:
# image: devopsismail/flask-task-manager:latest
# to: build: .

docker-compose up --build -d
```

## Troubleshooting

**Port 5000 in use?** Change port in `docker-compose.yml`:
```yaml
ports:
  - "5001:5000"
```

**Database connection error?** Wait 10 seconds for PostgreSQL to initialize.

**Check logs:**
```bash
docker-compose logs web
docker-compose logs db
```

## Tech Stack

- Python 3.10
- Flask 3.0.3
- PostgreSQL 16
- pgAdmin 8.12
- Docker & Docker Compose

## Links

- **GitHub**: https://github.com/iskilicaslan61/flask-postgres-docker-compose
- **Docker Hub**: https://hub.docker.com/r/devopsismail/flask-task-manager

## Security Note

⚠️ **Change default passwords before production use!**

---

**Made with ❤️ using Flask & Docker**
