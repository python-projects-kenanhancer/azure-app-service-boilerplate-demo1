output "app_service_url" {
  description = "The URL of the deployed Azure App Service"
  value       = azurerm_linux_web_app.main.default_hostname
}

output "app_service_name" {
  description = "The name of the deployed Azure App Service"
  value       = azurerm_linux_web_app.main.name
}

output "resource_group_name" {
  description = "The name of the resource group"
  value       = azurerm_resource_group.main.name
}

output "storage_account_name" {
  description = "The name of the storage account"
  value       = azurerm_storage_account.main.name
}

output "storage_account_primary_access_key" {
  description = "The primary access key for the storage account"
  value       = azurerm_storage_account.main.primary_access_key
  sensitive   = true
}

output "app_service_plan_name" {
  description = "The name of the App Service Plan"
  value       = azurerm_service_plan.main.name
}
