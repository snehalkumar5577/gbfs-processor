include "root" {
  path = find_in_parent_folders()
}

terraform {
  source = "github.com/claranet/terraform-azurerm-acr?ref=v7.1.0"
}

dependency "resource_group" {
  config_path = "../resource-group"
}

inputs = {
  resource_group_name = dependency.resource_group.outputs["resource_group_name"]
  sku = "Basic"

  custom_name = "devregistry1908"
  logs_destinations_ids = []
}
