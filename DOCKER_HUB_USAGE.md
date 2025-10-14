# Using Flask Task Manager from Docker Hub

This guide shows you how to run the Flask Task Manager application using the pre-built image from Docker Hub.

## Quick Start (3 Steps)

### 1. Pull the Image

```bash
docker pull devopsismail/flask-task-manager:latest
```

### 2. Create `.env` File

Create a `.env` file in your project directory:

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

### 3. Run with Docker Compose

**Option A: Use the provided hub config**
```bash
docker-compose -f docker-compose.hub.yml up -d
```

**Option B: Modify existing docker-compose.yml**

Change this line:
```yaml
  web:
    build: .  # Remove this line
```

To:
```yaml
  web:
    image: devopsismail/flask-task-manager:latest  # Add this line
```

Then run:
```bash
docker-compose up -d
```

## Access the Application

- **Flask App**: http://localhost:5000
- **pgAdmin**: http://localhost:5050

## Full Example (From Scratch)

```bash
# 1. Create a new directory
mkdir flask-task-manager
cd flask-task-manager

# 2. Download docker-compose.hub.yml
# (Copy the content or download from GitHub)

# 3. Create .env file
cat > .env << EOF
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=mydb
DATABASE_HOST=db
DATABASE_NAME=mydb
DATABASE_USER=user
DATABASE_PASSWORD=password
SECRET_KEY=your-secret-key-here
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=admin
EOF

# 4. Pull and run
docker pull devopsismail/flask-task-manager:latest
docker-compose -f docker-compose.hub.yml up -d

# 5. Check status
docker-compose -f docker-compose.hub.yml ps

# 6. View logs
docker-compose -f docker-compose.hub.yml logs -f
```

## Management Commands

```bash
# Stop all services
docker-compose -f docker-compose.hub.yml down

# Stop and remove volumes (deletes all data)
docker-compose -f docker-compose.hub.yml down -v

# View logs
docker-compose -f docker-compose.hub.yml logs -f web

# Restart a service
docker-compose -f docker-compose.hub.yml restart web

# Check running containers
docker-compose -f docker-compose.hub.yml ps
```

## Using Different Versions

```bash
# Pull a specific version
docker pull devopsismail/flask-task-manager:v1.0

# Update docker-compose.hub.yml to use specific version
image: devopsismail/flask-task-manager:v1.0
```

## Updating to Latest Version

```bash
# Pull the latest image
docker pull devopsismail/flask-task-manager:latest

# Recreate containers with new image
docker-compose -f docker-compose.hub.yml up -d --force-recreate
```

## Advantages of Using Docker Hub Image

✅ **No Build Required** - Saves time, no need to install build tools  
✅ **Consistent** - Same image everywhere  
✅ **Fast Deployment** - Just pull and run  
✅ **Version Control** - Use specific versions via tags  
✅ **Smaller Download** - Only download what you need  

## Troubleshooting

### Port Already in Use
```bash
# Change port in docker-compose.hub.yml
ports:
  - "5001:5000"  # Use 5001 instead of 5000
```

### Database Connection Error
```bash
# Wait for database to be healthy
docker-compose -f docker-compose.hub.yml logs db

# Check if postgres is ready
docker exec postgres_db pg_isready -U user
```

### Permission Issues
```bash
# Ensure .env file has correct permissions
chmod 644 .env
```

## Production Deployment

**Important**: Before deploying to production:

1. Change all default passwords in `.env`
2. Use a strong `SECRET_KEY`
3. Consider using Docker secrets or environment variable management
4. Use SSL/TLS certificates
5. Set up proper backups for PostgreSQL volume
6. Use a production WSGI server (add to image)

## Support

- **GitHub**: https://github.com/iskilicaslan61/flask-postgres-docker-compose
- **Docker Hub**: https://hub.docker.com/r/devopsismail/flask-task-manager

---

**Happy Coding!** 🚀

