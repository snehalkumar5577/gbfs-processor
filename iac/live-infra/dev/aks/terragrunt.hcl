include "root" {
  path = find_in_parent_folders()
}

terraform {
  source = "github.com/Azure/terraform-azurerm-aks?ref=8.0.0"
}

dependency "resource_group" {
  config_path = "../resource-group"
}

dependency "acr" {
  config_path = "../acr"
}

inputs = {
  cluster_name = "dev-aks"
  kubernetes_version  = "1.29.2"
  resource_group_name = dependency.resource_group.outputs["resource_group_name"]

  prefix = "dev"

  # Cluster configuration
  log_analytics_workspace_enabled    = false
  role_based_access_control_enabled  = true
  rbac_aad                           = false
  node_os_channel_upgrade            = "None"

  # Default node pool configuration
  agents_pool_name             = "default"
  temporary_name_for_rotation  = "defaulttemp"
  only_critical_addons_enabled = false
  agents_size                  = "Standard_D2_v2"
  agents_count                 = 1
  enable_auto_scaling          = false
  agents_pool_max_surge        = "10%"

  # ACR integration
  attached_acr_id_map = {
    "devregistry1908" = dependency.acr.outputs["acr_id"]
  }

# Additional node pool configuration
  node_pools = {
    tooling = {
      name                = "tooling"
      vm_size             = "Standard_D2_v2"
      os_disk_size_gb     = 50
      max_count           = 1
      min_count           = 0
      enable_auto_scaling = true
      eviction_policy     = "Delete"
      priority            = "Spot"
      node_taints         = ["dedicated=tooling:NoSchedule", "kubernetes.azure.com/scalesetpriority=spot:NoSchedule"]
      node_labels = {
        "dedicated" = "tooling",
        "kubernetes.azure.com/scalesetpriority" = "spot"
      }
    },
    application = {
      name                = "app"
      vm_size             = "Standard_D2_v2"
      os_disk_size_gb     = 50
      max_count           = 1
      min_count           = 0
      enable_auto_scaling = true
      eviction_policy     = "Delete"
      priority            = "Spot"
      node_taints         = ["dedicated=apps:NoSchedule", "kubernetes.azure.com/scalesetpriority=spot:NoSchedule"]
      node_labels = {
        "dedicated" = "apps",
        "kubernetes.azure.com/scalesetpriority" = "spot"
      }
    }
  }
}