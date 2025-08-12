basic_config = {
  project_name = "ovo-kenan-boilerplate"
  environment = "dev"
  azure_region = "West Europe"
  tf_state_bucket = "terraform-state-bucket-for-boilerplate"
  tf_state_prefix = "azure-app-service"
  tf_encryption_key = "GrEs/8Y9T6c8XHppgSClVMopJuXH17XakvmgxHCmawo="
}

app_service_config = {
  python_version = "3.12"
  sku_name = "B1"
  startup_command = "python -m src.main"
  app_settings = {
    "WEBSITES_PORT" = "8000"
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = "true"
    "PYTHON_VERSION" = "3.12"
    "ENVIRONMENT" = "dev"
    "AZURE_KEYVAULT_URL" = "https://app-keyvault-dev.vault.azure.net/"
    "AZURE_STORAGE_ACCOUNT_URL" = "https://ovokenanboilerplatedevstorage.blob.core.windows.net/"
  }
}

azure_keyvault_config = {
  name = "app-keyvault-dev"
  sku_name = "standard"
  enabled_for_disk_encryption = true
  enabled_for_deployment = true
  enabled_for_template_deployment = true
  purge_protection_enabled = false
}

azure_storage_config = {
  account_tier = "Standard"
  account_replication_type = "LRS"
  containers = [
    {
      name = "config"
      access_type = "private"
    },
    {
      name = "app-files"
      access_type = "private"
    }
  ]
}
