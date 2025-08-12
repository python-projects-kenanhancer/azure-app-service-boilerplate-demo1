# Azure App Service deployment
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "${var.basic_config.project_name}-${var.basic_config.environment}-rg"
  location = var.basic_config.azure_region
}

# App Service Plan
resource "azurerm_service_plan" "main" {
  name                = "${var.basic_config.project_name}-${var.basic_config.environment}-plan"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = var.app_service_config.sku_name
}

# Storage Account for application files
resource "azurerm_storage_account" "main" {
  name                     = "${var.basic_config.project_name}${var.basic_config.environment}storage"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# Storage Container for application files
resource "azurerm_storage_container" "app_files" {
  name                  = "app-files"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}

# App Service
resource "azurerm_linux_web_app" "main" {
  name                = "${var.basic_config.project_name}-${var.basic_config.environment}-app"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    application_stack {
      python_version = var.app_service_config.python_version
    }
    
    app_command_line = var.app_service_config.startup_command
  }

  app_settings = var.app_service_config.app_settings

  # Application logs
  logs {
    application_logs {
      file_system_level = "Information"
    }
  }
}
