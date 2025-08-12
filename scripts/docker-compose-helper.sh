#!/bin/bash

# Docker Compose Helper Script for Azure App Service
# This script provides common operations for managing the development environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to check if docker-compose is available
check_docker_compose() {
    if ! command -v docker-compose > /dev/null 2>&1; then
        print_error "docker-compose is not installed. Please install it and try again."
        exit 1
    fi
}

# Function to start services
start_services() {
    print_header "Starting Azure App Service Development Environment"
    check_docker
    check_docker_compose
    
    print_status "Starting PostgreSQL, Redis, and web interfaces..."
    docker-compose up -d
    
    print_status "Waiting for services to be ready..."
    sleep 10
    
    print_status "Checking service health..."
    check_health
    
    print_header "Services Started Successfully"
    print_status "PostgreSQL: localhost:5432"
    print_status "Redis: localhost:6379"
    print_status "pgAdmin: http://localhost:8080 (admin@azure-app-service.com / admin123)"
    print_status "Redis Commander: http://localhost:8081 (admin / admin123)"
}

# Function to stop services
stop_services() {
    print_header "Stopping Azure App Service Development Environment"
    docker-compose down
    print_status "Services stopped successfully"
}

# Function to restart services
restart_services() {
    print_header "Restarting Azure App Service Development Environment"
    docker-compose down
    docker-compose up -d
    print_status "Services restarted successfully"
}

# Function to check service health
check_health() {
    print_header "Checking Service Health"
    
    # Check PostgreSQL
    if docker-compose exec -T postgres pg_isready -U app_user > /dev/null 2>&1; then
        print_status "PostgreSQL: ✅ Healthy"
    else
        print_warning "PostgreSQL: ⚠️ Starting up..."
    fi
    
    # Check Redis
    if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
        print_status "Redis: ✅ Healthy"
    else
        print_warning "Redis: ⚠️ Starting up..."
    fi
}

# Function to view logs
view_logs() {
    local service=${1:-""}
    
    if [ -z "$service" ]; then
        print_header "Viewing All Service Logs"
        docker-compose logs -f
    else
        print_header "Viewing $service Logs"
        docker-compose logs -f "$service"
    fi
}

# Function to backup database
backup_database() {
    local backup_file=${1:-"backup_$(date +%Y%m%d_%H%M%S).sql"}
    
    print_header "Backing Up PostgreSQL Database"
    print_status "Creating backup: $backup_file"
    
    docker-compose exec -T postgres pg_dump -U app_user azure_app_service_db > "$backup_file"
    
    if [ $? -eq 0 ]; then
        print_status "Backup created successfully: $backup_file"
    else
        print_error "Backup failed"
        exit 1
    fi
}

# Function to restore database
restore_database() {
    local backup_file=${1:-""}
    
    if [ -z "$backup_file" ]; then
        print_error "Please specify a backup file to restore"
        echo "Usage: $0 restore <backup_file.sql>"
        exit 1
    fi
    
    if [ ! -f "$backup_file" ]; then
        print_error "Backup file not found: $backup_file"
        exit 1
    fi
    
    print_header "Restoring PostgreSQL Database"
    print_warning "This will overwrite the current database!"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Restoring from: $backup_file"
        docker-compose exec -T postgres psql -U app_user -d azure_app_service_db < "$backup_file"
        print_status "Database restored successfully"
    else
        print_status "Restore cancelled"
    fi
}

# Function to clean up everything
cleanup() {
    print_header "Cleaning Up Development Environment"
    print_warning "This will remove all containers, volumes, and data!"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose down -v
        docker system prune -f
        print_status "Cleanup completed"
    else
        print_status "Cleanup cancelled"
    fi
}

# Function to show status
show_status() {
    print_header "Service Status"
    docker-compose ps
    
    echo
    print_header "Connection Information"
    echo "PostgreSQL: postgresql://app_user:app_password@localhost:5432/azure_app_service_db"
    echo "Redis: redis://localhost:6379/0"
    echo "pgAdmin: http://localhost:8080"
    echo "Redis Commander: http://localhost:8081"
}

# Function to show help
show_help() {
    print_header "Docker Compose Helper Script"
    echo "Usage: $0 <command> [options]"
    echo
    echo "Commands:"
    echo "  start              Start all services"
    echo "  stop               Stop all services"
    echo "  restart            Restart all services"
    echo "  status             Show service status"
    echo "  health             Check service health"
    echo "  logs [service]     View logs (all or specific service)"
    echo "  backup [file]      Backup PostgreSQL database"
    echo "  restore <file>     Restore PostgreSQL database"
    echo "  cleanup            Remove all containers and volumes"
    echo "  help               Show this help message"
    echo
    echo "Examples:"
    echo "  $0 start"
    echo "  $0 logs postgres"
    echo "  $0 backup my_backup.sql"
    echo "  $0 restore my_backup.sql"
}

# Main script logic
case "${1:-help}" in
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    status)
        show_status
        ;;
    health)
        check_health
        ;;
    logs)
        view_logs "$2"
        ;;
    backup)
        backup_database "$2"
        ;;
    restore)
        restore_database "$2"
        ;;
    cleanup)
        cleanup
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        echo
        show_help
        exit 1
        ;;
esac
