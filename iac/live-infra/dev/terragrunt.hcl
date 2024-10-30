generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "azurerm" {
  subscription_id      = "ad34a297-311a-4012-b3bb-2b02ee6521ab"
  features {
  }
}
EOF
}

# backend for dev
remote_state {
  backend = "azurerm"
  config = {
    key                  = "${path_relative_to_include()}/terraform.tfstate"
    resource_group_name  = "devops"
    storage_account_name = "devopstg"
    container_name       = "dev-tf-state"
  }
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
}

inputs = {
  location    = "northeurope"
  location_short = "ne"
  environment = "dev"
  client_name = "devops"
  stack       = "infra"
}
