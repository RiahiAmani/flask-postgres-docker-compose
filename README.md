# Flask Task Manager with PostgreSQL

A task management web application with user authentication, built with Flask and PostgreSQL, fully containerized with Docker Compose.

[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-devopsismail%2Fflask--task--manager-blue)](https://hub.docker.com/r/devopsismail/flask-task-manager)
[![Docker Image Size](https://img.shields.io/badge/image%20size-265MB-brightgreen)](https://hub.docker.com/r/devopsismail/flask-task-manager)
[![Docker Pulls](https://img.shields.io/docker/pulls/devopsismail/flask-task-manager)](https://hub.docker.com/r/devopsismail/flask-task-manager)

## Features

- 🔐 User registration and login system
- ✅ Create, complete, and delete tasks
- 👤 User-specific task lists
- 🗄️ PostgreSQL database with SQLAlchemy ORM
- 🛠️ pgAdmin for database management
- 🐳 Fully containerized with Docker Compose
- ☁️ Pre-built image available on Docker Hub

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Quick Start (Using Docker Hub Image)

### 1. Pull the Image

```bash
docker pull devopsismail/flask-task-manager:latest
```

### 2. Create Project Directory

```bash
mkdir flask-task-manager
cd flask-task-manager
```

### 3. Create `.env` File

Create a `.env` file with the following content:

```env
# PostgreSQL Configuration
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=mydb

# Flask App Configuration
DATABASE_HOST=db
DATABASE_NAME=mydb
DATABASE_USER=user
DATABASE_PASSWORD=password
SECRET_KEY=your-secret-key-change-this-in-production

# pgAdmin Configuration
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=admin
```

### 4. Create `docker-compose.yml`

Create a `docker-compose.yml` file:

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

### 5. Start the Application

```bash
docker-compose up -d
```

### 6. Access the Application

- **Flask App**: http://localhost:5000
- **pgAdmin**: http://localhost:5050

## Usage

### First Time Setup

1. Open http://localhost:5000 in your browser
2. Click on **Register** to create a new account
3. Fill in your username and password
4. Login with your credentials
5. Start adding tasks!

### Using pgAdmin

1. Navigate to http://localhost:5050
2. Login with credentials from `.env`:
   - Email: `admin@example.com`
   - Password: `admin`
3. Add a new server:
   - **General Tab**:
     - Name: `PostgreSQL DB` (or any name)
   - **Connection Tab**:
     - Host: `db` (Docker service name)
     - Port: `5432`
     - Username: `user` (from `.env`)
     - Password: `password` (from `.env`)
     - Database: `mydb` (from `.env`)

## Docker Commands

### Start Services

```bash
# Start all services in background
docker-compose up -d

# Start and view logs
docker-compose up

# Rebuild and start (if building from source)
docker-compose up --build
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove all data (including database)
docker-compose down -v
```

### View Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs web
docker-compose logs db
docker-compose logs pgadmin

# Follow logs in real-time
docker-compose logs -f web
```

### Restart Services

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart web
```

### Check Status

```bash
# View running containers
docker-compose ps

# View detailed container info
docker inspect flask_app
```

## Docker Hub

### Available Tags

- `latest` - Latest stable version
- `v1.0` - Version 1.0

### Pull Specific Version

```bash
# Pull latest
docker pull devopsismail/flask-task-manager:latest

# Pull specific version
docker pull devopsismail/flask-task-manager:v1.0
```

### Update to Latest Version

```bash
# Pull the latest image
docker pull devopsismail/flask-task-manager:latest

# Recreate containers with new image
docker-compose up -d --force-recreate
```

## Building from Source (Optional)

If you want to build the image yourself instead of using Docker Hub:

### 1. Clone the Repository

```bash
git clone https://github.com/iskilicaslan61/flask-postgres-docker-compose.git
cd flask-postgres-docker-compose
```

### 2. Modify docker-compose.yml

Change the `web` service from:
```yaml
  web:
    image: devopsismail/flask-task-manager:latest
```

To:
```yaml
  web:
    build: .
```

### 3. Build and Run

```bash
docker-compose up --build -d
```

## Project Structure

```
flask-task-manager/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── auth.py              # Authentication routes
│   ├── models.py            # Database models
│   ├── routes.py            # Main routes
│   ├── static/              # Static files (CSS, JS)
│   └── templates/           # HTML templates
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile              # Docker image definition
├── requirements.txt        # Python dependencies
├── wsgi.py                # Application entry point
├── .env                   # Environment variables (create this)
├── .gitignore             # Git ignore file
└── README.md              # This file
```

## Database Schema

### Users Table
| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key (auto-increment) |
| `username` | VARCHAR(150) | Unique username |
| `password` | VARCHAR(200) | Hashed password |

### Tasks Table
| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key (auto-increment) |
| `title` | VARCHAR(200) | Task description |
| `completed` | BOOLEAN | Completion status (default: false) |
| `created_at` | TIMESTAMP | Creation timestamp |
| `user_id` | INTEGER | Foreign key to users table |

## Tech Stack

- **Backend**: Flask 3.0.3
- **Database**: PostgreSQL 16
- **ORM**: Flask-SQLAlchemy 3.0.5
- **Authentication**: Flask-Login 0.6.3
- **Database Admin**: pgAdmin 8.12
- **Language**: Python 3.10
- **Containerization**: Docker & Docker Compose

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `POSTGRES_USER` | PostgreSQL username | `user` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `password` |
| `POSTGRES_DB` | PostgreSQL database name | `mydb` |
| `DATABASE_HOST` | Database host (use `db` for Docker) | `db` |
| `DATABASE_NAME` | Database name | `mydb` |
| `DATABASE_USER` | Database username | `user` |
| `DATABASE_PASSWORD` | Database password | `password` |
| `SECRET_KEY` | Flask secret key | `your-secret-key` |
| `PGADMIN_DEFAULT_EMAIL` | pgAdmin login email | `admin@example.com` |
| `PGADMIN_DEFAULT_PASSWORD` | pgAdmin login password | `admin` |

## Troubleshooting

### Port Already in Use

If port 5000 is already in use, change it in `docker-compose.yml`:

```yaml
  web:
    ports:
      - "5001:5000"  # Use 5001 instead of 5000
```

Then access the app at http://localhost:5001

### Database Connection Error

Wait a few seconds for PostgreSQL to initialize on first run:

```bash
# Check database logs
docker-compose logs db

# Check if database is ready
docker exec postgres_db pg_isready -U user
```

### Cannot Access Application

```bash
# Check if all containers are running
docker-compose ps

# Check Flask app logs
docker-compose logs web

# Restart services
docker-compose restart
```

### Permission Denied

```bash
# On Linux/Mac, ensure proper permissions
chmod 644 .env

# If volumes have permission issues
docker-compose down -v
docker-compose up -d
```

## Production Deployment

⚠️ **Important**: Before deploying to production:

### Security
- ✅ Change all default passwords in `.env`
- ✅ Use a strong, random `SECRET_KEY`
- ✅ Use Docker secrets or a secrets manager (AWS Secrets Manager, HashiCorp Vault)
- ✅ Enable HTTPS with SSL/TLS certificates
- ✅ Implement rate limiting
- ✅ Use non-root users (already implemented in image)

### Performance
- ✅ Use a production WSGI server (Gunicorn/uWSGI instead of Flask dev server)
- ✅ Set up proper logging and monitoring
- ✅ Configure database connection pooling
- ✅ Use a reverse proxy (Nginx, Traefik)

### Reliability
- ✅ Set up automated backups for PostgreSQL volume
- ✅ Use Docker health checks (already implemented)
- ✅ Implement proper restart policies
- ✅ Monitor container resource usage

### Example Production Setup

```bash
# Use specific version tag
docker pull devopsismail/flask-task-manager:v1.0

# Set resource limits in docker-compose.yml
services:
  web:
    image: devopsismail/flask-task-manager:v1.0
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Links

- **GitHub Repository**: https://github.com/iskilicaslan61/flask-postgres-docker-compose
- **Docker Hub**: https://hub.docker.com/r/devopsismail/flask-task-manager
- **Issues**: https://github.com/iskilicaslan61/flask-postgres-docker-compose/issues

## License

This project is open source and available for educational purposes.

---

**Made with ❤️ using Flask, PostgreSQL, and Docker**

**Happy Coding!** 🚀
