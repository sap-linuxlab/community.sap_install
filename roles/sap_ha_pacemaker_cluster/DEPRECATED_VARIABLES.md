# sap_ha_pacemaker_cluster Deprecated input variables

This deprecation of input variables is part of an ongoing effort to improve the codebase by removing unnecessary elements and streamlining the overall design.

These variables fall into a few categories:
- **Obsolete or unused**
  - These variables are no longer used and are being removed to reduce technical debt and potential confusion.
- **Renamed**
  - These variables are being renamed to better reflect their current purpose and improve code readability.
  - This is especially important when the variable's functionality has evolved over time.

## Backwards compatibility
All deprecated variables offer time limited backwards compatibility that will be removed in future.

## List of deprecated input variables
| Old variable | New variable | Backwards compatible | Reason |
| -------- | --------- | --------- | --------- |
| sap_ha_pacemaker_cluster_nwas_abap_sid | sap_ha_pacemaker_cluster_nwas_sid | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_nwas_abap_ascs_instance_nr | sap_ha_pacemaker_cluster_nwas_ascs_instance_nr | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_nwas_abap_ers_instance_nr | sap_ha_pacemaker_cluster_nwas_ers_instance_nr | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_nwas_abap_ascs_sapinstance_instance_name | sap_ha_pacemaker_cluster_nwas_ascs_sapinstance_instance_name | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_nwas_abap_ers_sapinstance_instance_name | sap_ha_pacemaker_cluster_nwas_ers_sapinstance_instance_name | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_nwas_abap_ascs_sapinstance_start_profile_string | sap_ha_pacemaker_cluster_nwas_ascs_sapinstance_start_profile_string | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_nwas_abap_ers_sapinstance_start_profile_string | sap_ha_pacemaker_cluster_nwas_ers_sapinstance_start_profile_string | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_nwas_abap_ascs_filesystem_resource_name | sap_ha_pacemaker_cluster_nwas_ascs_filesystem_resource_name | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_nwas_abap_ascs_sapinstance_resource_name | sap_ha_pacemaker_cluster_nwas_ascs_sapinstance_resource_name | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_nwas_abap_ascs_sapstartsrv_resource_name | sap_ha_pacemaker_cluster_nwas_ascs_sapstartsrv_resource_name | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_nwas_abap_ers_filesystem_resource_name | sap_ha_pacemaker_cluster_nwas_ers_filesystem_resource_name | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_nwas_abap_ers_sapinstance_resource_name | sap_ha_pacemaker_cluster_nwas_ers_sapinstance_resource_name | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_nwas_abap_ers_sapstartsrv_resource_name | sap_ha_pacemaker_cluster_nwas_ers_sapstartsrv_resource_name | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_nwas_abap_ascs_sapinstance_automatic_recover_bool | sap_ha_pacemaker_cluster_nwas_cs_sapinstance_automatic_recover_bool | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_nwas_abap_ascs_sapinstance_resource_stickiness | sap_ha_pacemaker_cluster_nwas_cs_sapinstance_resource_stickiness | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_nwas_abap_ascs_sapinstance_ensa1_migration_threshold | sap_ha_pacemaker_cluster_nwas_cs_sapinstance_ensa1_migration_threshold | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_nwas_abap_ascs_sapinstance_ensa1_failure_timeout | sap_ha_pacemaker_cluster_nwas_cs_sapinstance_ensa1_failure_timeout | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_nwas_abap_ascs_group_stickiness | sap_ha_pacemaker_cluster_nwas_cs_group_stickiness | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_nwas_abap_ascs_ers_ensa1 | sap_ha_pacemaker_cluster_nwas_cs_ensa1 | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_nwas_abap_ascs_ers_simple_mount | sap_ha_pacemaker_cluster_nwas_cs_ers_simple_mount | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_vip_nwas_abap_ascs_ip_address | sap_ha_pacemaker_cluster_vip_nwas_ascs_ip_address | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_vip_nwas_abap_ascs_resource_name | sap_ha_pacemaker_cluster_vip_nwas_ascs_resource_name | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_vip_nwas_abap_ers_ip_address | sap_ha_pacemaker_cluster_vip_nwas_ers_ip_address | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_vip_nwas_abap_ers_resource_name | sap_ha_pacemaker_cluster_vip_nwas_ers_resource_name | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_vip_nwas_abap_ascs_resource_group_name | sap_ha_pacemaker_cluster_vip_nwas_ascs_resource_group_name | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_vip_nwas_abap_ers_resource_group_name | sap_ha_pacemaker_cluster_vip_nwas_ers_resource_group_name | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_healthcheck_nwas_abap_ascs_resource_name | sap_ha_pacemaker_cluster_healthcheck_nwas_ascs_resource_name | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_healthcheck_nwas_abap_ers_resource_name | sap_ha_pacemaker_cluster_healthcheck_nwas_ers_resource_name | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_healthcheck_nwas_abap_ascs_id | sap_ha_pacemaker_cluster_healthcheck_nwas_ascs_id | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_healthcheck_nwas_abap_ers_id | sap_ha_pacemaker_cluster_healthcheck_nwas_ers_id | :heavy_check_mark: | Removal of `_abap_` |
| sap_ha_pacemaker_cluster_storage_nfs_filesytem_type | sap_ha_pacemaker_cluster_storage_nfs_filesystem_type | :heavy_check_mark: | Typo |


## Status explanation:
- :heavy_check_mark: - Variable is removed from defaults and readme, but still supported.
- :x: - Variable is completely removed and not supported
