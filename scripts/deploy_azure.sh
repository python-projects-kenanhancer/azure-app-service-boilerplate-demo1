#!/bin/bash

# Azure App Service deployment script

set -e

echo "Starting Azure App Service deployment..."

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "Azure CLI is not installed. Please install it first."
    exit 1
fi

# Check if user is logged in
if ! az account show &> /dev/null; then
    echo "Please login to Azure first: az login"
    exit 1
fi

# Load environment variables
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Set variables
RESOURCE_GROUP="${RESOURCE_GROUP:-ovo-kenan-boilerplate-dev-rg}"
APP_NAME="${APP_NAME:-ovo-kenan-boilerplate-dev-app}"
LOCATION="${LOCATION:-West Europe}"

echo "Deploying to Azure App Service..."
echo "Resource Group: $RESOURCE_GROUP"
echo "App Name: $APP_NAME"
echo "Location: $LOCATION"

# Create resource group if it doesn't exist
echo "Creating resource group if it doesn't exist..."
az group create --name "$RESOURCE_GROUP" --location "$LOCATION" --output none

# Create App Service Plan if it doesn't exist
PLAN_NAME="${APP_NAME}-plan"
echo "Creating App Service Plan: $PLAN_NAME"
az appservice plan create \
    --name "$PLAN_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --sku B1 \
    --is-linux \
    --output none

# Create App Service if it doesn't exist
echo "Creating App Service: $APP_NAME"
az webapp create \
    --name "$APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --plan "$PLAN_NAME" \
    --runtime "PYTHON:3.12" \
    --output none

# Configure App Service
echo "Configuring App Service..."
az webapp config set \
    --name "$APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --startup-file "python -m src.main" \
    --output none

# Set app settings
echo "Setting app settings..."
az webapp config appsettings set \
    --name "$APP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --settings \
        WEBSITES_PORT=8000 \
        SCM_DO_BUILD_DURING_DEPLOYMENT=true \
        PYTHON_VERSION=3.12 \
        ENVIRONMENT=dev \
    --output none

# Deploy the application
echo "Deploying application..."
az webapp deployment source config-zip \
    --resource-group "$RESOURCE_GROUP" \
    --name "$APP_NAME" \
    --src dist/app.zip \
    --output none

echo "Deployment completed successfully!"
echo "App Service URL: https://$APP_NAME.azurewebsites.net"
echo "Health check: https://$APP_NAME.azurewebsites.net/health"
