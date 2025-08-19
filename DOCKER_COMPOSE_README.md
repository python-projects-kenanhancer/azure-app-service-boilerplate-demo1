# Docker Compose Setup for Azure App Service

This directory contains Docker Compose configuration for local development with PostgreSQL and Redis.

## 🚀 Quick Start

### 1. Start the Services

```bash
# Start all services
docker-compose up -d

# Start specific services only
docker-compose up -d postgres redis
```

### 2. Check Service Status

```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f postgres
docker-compose logs -f redis
```

### 3. Stop the Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (⚠️ This will delete all data)
docker-compose down -v
```

## 📊 Services Overview

| Service | Port | Description | Web UI |
| ------------------- | ---- | ------------------------ | ---------------------- |
| **PostgreSQL** | 5432 | Main database | pgAdmin (8080) |
| **Redis** | 6379 | Cache and session store | Redis Commander (8081) |
| **pgAdmin** | 8080 | PostgreSQL web interface | http://localhost:8080 |
| **Redis Commander** | 8081 | Redis web interface | http://localhost:8081 |

## 🔧 Configuration

### PostgreSQL

- **Database**: `azure_app_service_db`
- **Username**: `app_user`
- **Password**: `app_password`
- **Connection String**: `postgresql://app_user:app_password@localhost:5432/azure_app_service_db`

### Redis

- **Host**: `localhost`
- **Port**: `6379`
- **Password**: None (development)
- **Connection String**: `redis://localhost:6379/0`

### Web Interfaces

#### pgAdmin

- **URL**: http://localhost:8080
- **Email**: `admin@azure-app-service.com`
- **Password**: `admin123`

#### Redis Commander

- **URL**: http://localhost:8081
- **Username**: `admin`
- **Password**: `admin123`

## 🗄️ Database Schema

The PostgreSQL database includes the following tables:

- **users** - User accounts
- **organizations** - Organization data
- **user_organizations** - User-organization relationships
- **sessions** - Session management
- **audit_logs** - Audit trail

## 🔍 Useful Commands

### Database Operations

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U app_user -d azure_app_service_db

# Backup database
docker-compose exec postgres pg_dump -U app_user azure_app_service_db > backup.sql

# Restore database
docker-compose exec -T postgres psql -U app_user -d azure_app_service_db < backup.sql
```

### Redis Operations

```bash
# Connect to Redis CLI
docker-compose exec redis redis-cli

# Monitor Redis commands
docker-compose exec redis redis-cli monitor

# Check Redis info
docker-compose exec redis redis-cli info
```

### Container Management

```bash
# Restart a specific service
docker-compose restart postgres

# Rebuild containers
docker-compose build

# View resource usage
docker-compose stats
```

## 🔒 Security Notes

⚠️ **Important**: This configuration is for **development only**!

- Default passwords are used
- No SSL/TLS encryption
- Services are exposed on localhost
- No authentication for Redis

For production:

- Use strong passwords
- Enable SSL/TLS
- Use secrets management
- Restrict network access
- Enable Redis authentication

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**

   ```bash
   # Check what's using the port
   lsof -i :5432
   lsof -i :6379

   # Stop conflicting services
   sudo systemctl stop postgresql
   sudo systemctl stop redis
   ```

1. **Permission denied**

   ```bash
   # Fix volume permissions
   sudo chown -R $USER:$USER ./data
   ```

1. **Container won't start**

   ```bash
   # Check logs
   docker-compose logs postgres

   # Remove and recreate
   docker-compose down -v
   docker-compose up -d
   ```

### Health Checks

```bash
# Check PostgreSQL health
docker-compose exec postgres pg_isready -U app_user

# Check Redis health
docker-compose exec redis redis-cli ping
```

## 📝 Environment Variables

Copy `docker-compose.env` to `.env` and modify as needed:

```bash
cp docker-compose.env .env
```

## 🔄 Updates

To update the services:

```bash
# Pull latest images
docker-compose pull

# Rebuild and restart
docker-compose up -d --build
```

## 📚 Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [pgAdmin Documentation](https://www.pgadmin.org/docs/)
