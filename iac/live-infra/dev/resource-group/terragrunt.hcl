include "root" {
  path = find_in_parent_folders()
}

terraform {
  source = "github.com/claranet/terraform-azurerm-rg?ref=v7.0.0"
}

inputs = {

  custom_name = "rg-infra-devops-dev"

}
