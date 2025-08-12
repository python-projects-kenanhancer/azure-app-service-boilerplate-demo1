variable "basic_config" {
  description = "Basic configuration for the deployment"
  type = object({
    project_name   = string
    environment    = string
    azure_region   = string
    tf_state_bucket = string
    tf_state_prefix = string
    tf_encryption_key = string
  })
}

variable "app_service_config" {
  description = "Azure App Service configuration"
  type = object({
    python_version = string
    sku_name = string
    startup_command = string
    app_settings = map(string)
  })
  default = {
    python_version = "3.12"
    sku_name = "B1"
    startup_command = "python -m src.main"
    app_settings = {
      "WEBSITES_PORT" = "8000"
      "SCM_DO_BUILD_DURING_DEPLOYMENT" = "true"
      "PYTHON_VERSION" = "3.12"
    }
  }
}

variable "azure_keyvault_config" {
  description = "Azure Key Vault configuration"
  type = object({
    name = string
    sku_name = string
    enabled_for_disk_encryption = bool
    enabled_for_deployment = bool
    enabled_for_template_deployment = bool
    purge_protection_enabled = bool
  })
  default = {
    name = "app-keyvault"
    sku_name = "standard"
    enabled_for_disk_encryption = true
    enabled_for_deployment = true
    enabled_for_template_deployment = true
    purge_protection_enabled = false
  }
}

variable "azure_storage_config" {
  description = "Azure Storage configuration"
  type = object({
    account_tier = string
    account_replication_type = string
    containers = list(object({
      name = string
      access_type = string
    }))
  })
  default = {
    account_tier = "Standard"
    account_replication_type = "LRS"
    containers = [
      {
        name = "config"
        access_type = "private"
      }
    ]
  }
}
