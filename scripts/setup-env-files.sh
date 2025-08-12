#!/bin/bash

# Setup script for environment files
# This script creates .env files from templates

set -e

echo "🔧 Setting up environment files..."

# Function to create env file from template
create_env_file() {
    local template_file=$1
    local env_file=$2
    
    if [ ! -f "$env_file" ]; then
        echo "📝 Creating $env_file from template..."
        cp "$template_file" "$env_file"
        echo "✅ Created $env_file"
    else
        echo "⚠️  $env_file already exists, skipping..."
    fi
}

# Create environment files from templates
create_env_file "env.postgres.template" ".env.postgres"
create_env_file "env.redis.template" ".env.redis"
create_env_file "env.redis-commander.template" ".env.redis-commander"
create_env_file "env.pgadmin.template" ".env.pgadmin"

echo ""
echo "🎉 Environment files setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Review and modify the .env files if needed"
echo "2. Run: docker-compose up -d"
echo "3. Access services:"
echo "   - PostgreSQL: localhost:5432"
echo "   - Redis: localhost:6379"
echo "   - pgAdmin: http://localhost:8080"
echo "   - Redis Commander: http://localhost:8081"
echo ""
echo "🔒 Security note: Add .env.* files to .gitignore to keep credentials secure"

