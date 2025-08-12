terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "tfstateboilerplate"
    container_name       = "tfstate"
    key                  = "azure-app-service.terraform.tfstate"
  }
}
