<!-- BEGIN: Role Introduction -->
# sap_ha_cluster Ansible Role

This role installs pacemaker cluster packages and configures the cluster and SAP cluster resources.
The cluster setup is managed through the `ha_cluster` Linux System Role.<br>
`sap_ha_cluster` is acting as a wrapper that takes care of the SAP environment parameter definitions, platform specific variables and additional steps to complete the SAP HA Cluster setup after pacemaker configuration.

<!-- END: Role Introduction -->

<!-- BEGIN: Requirements -->
## Requirements

Target Systems:
- Supported OS: RHEL 8.4+
- RHEL registration and access to High-Availability repository
- SAP Hana installed and configured, for instance using the provided `sap_hana_*` Ansible roles in this repository

Ansible Control System:
- Ansible 2.9+
- `Linux System Roles` collection from either source:
  - RHEL package: rhel-system-roles-1.16.2
  - Automation Hub: <to be defined>
  - Ansible Galaxy: <to be defined>

<!-- END: Requirements -->

<!-- BEGIN: Role Input Parameters -->
## Role Input Parameters

| Variable Name | Required | Description |
|---------------|----------|-------------|
| **ha_cluster_hacluster_password**<br><sup>Alias: sap_hana_hacluster_password</sup><br><sup>Type: str</sup> | **True** | The password of the `hacluster` user which is created during pacemaker installation. |
| **sap_hana_cluster_nodes**<br><br><sup>Type: list</sup> | **True** | List of cluster nodes and associated attributes (in dictionary format).<br>This is required for the srHook configuration. |
| **sap_hana_instance_number**<br><sup>Alias: sap_ha_cluster_hana_instance_number</sup><br><sup>Type: str</sup> | **True** | The instance number of the SAP HANA database which is role will configure in the cluster. |
| **sap_hana_sid**<br><sup>Alias: sap_ha_cluster_hana_sid</sup><br><sup>Type: str</sup> | **True** | The SAP System ID of the instance that will be configured in the cluster.<br>The SAP SID must follow SAP specifications - see SAP Note 1979280. |
| **sap_hana_vip**<br><br><sup>Type: dict</sup> | **True** | Virtual floating IP for SAP HANA DB connections.<br>This IP will always run on the promoted HANA node. |
| ha_cluster<br><br><sup>Type: dict</sup> | False | Optional **host_vars** parameter, if defined it must be set for each node.<br>Definition of node name and IP addresses to be used for the pacemaker cluster.<br>Required for resilient node communication by providing more than one corosync IP.<br>See https://github.com/linux-system-roles/ha_cluster/blob/master/README.md#nodes-names-and-addresses |
| ha_cluster_cluster_name<br><sup>Alias: sap_ha_cluster_cluster_name</sup><br><sup>Type: str</sup> | False<br><br><sup>Default: "my-cluster"</sup> | The name of the pacemaker cluster. |
| sap_ha_cluster_aws_access_key_id<br><br><sup>Type: str</sup> | False | AWS access key to allow control of instances (for example for fencing operations).<br>Required for cluster nodes setup on Amazon cloud. |
| sap_ha_cluster_aws_region<br><br><sup>Type: str</sup> | False | The AWS region in which the instances to be used for the cluster setup are located.<br>Required for cluster nodes setup on Amazon cloud. |
| sap_ha_cluster_aws_secret_access_key<br><br><sup>Type: str</sup> | False | AWS secret key, paired with the access key for instance control.<br>Required for cluster nodes setup on Amazon cloud. |
| sap_ha_cluster_create_config_dest<br><br><sup>Type: str</sup> | False<br><br><sup>Default: "sap_ha_cluster_resource_config.yml"</sup> | The cluster resource configuration created by this role will be saved in a Yaml file in the current working directory.<br>Specify a path/filename to save the file elsewhere. |
| sap_ha_cluster_create_config_only<br><br><sup>Type: bool</sup> | False<br><br><sup>Default: "False"</sup> | Enable to only create an output of the parameters and values this role will use as input into the 'ha_cluster' role.<br>The output is saved in a variables file and used for individual execution of the 'ha_cluster' linux system role.<br>WARNING! This report may include sensitive details like secrets required for certain cluster resources! |
| sap_ha_cluster_fence_power_timeout<br><br><sup>Type: int</sup> | False<br><br><sup>Default: "240"</sup> | STONITH resource parameter to test X seconds for status change after ON/OFF. |
| sap_ha_cluster_fence_reboot_retries<br><br><sup>Type: int</sup> | False<br><br><sup>Default: "4"</sup> | STONITH resource parameter to define how often it retries to restart a node. |
| sap_ha_cluster_fence_reboot_timeout<br><br><sup>Type: int</sup> | False<br><br><sup>Default: "400"</sup> | STONITH resource parameter to define after which timeout a node restart is returned as failed. |
| sap_ha_cluster_hana_automated_register<br><br><sup>Type: bool</sup> | False<br><br><sup>Default: "True"</sup> | Define if a former primary should be re-registered automatically as secondary. |
| sap_ha_cluster_hana_duplicate_primary_timeout<br><br><sup>Type: int</sup> | False<br><br><sup>Default: "900"</sup> | Time difference needed between to primary time stamps, if a dual-primary situation occurs.<br>If the time difference is less than the time gap, then the cluster holds one or both instances in a "WAITING" status.<br>This is to give an admin a chance to react on a failover. A failed former primary will be registered after the time difference is passed. |
| sap_ha_cluster_hana_prefer_site_takeover<br><br><sup>Type: bool</sup> | False<br><br><sup>Default: "True"</sup> | Set to "false" if the cluster should first attempt to restart the instance on the same node.<br>When set to "true" (default) a failover to secondary will be initiated on resource failure. |
| sap_ha_cluster_hana_resource_name<br><br><sup>Type: str</sup> | False<br><br><sup>Default: "SAPHana_<SID>_<Instance Number>"</sup> | Customize the cluster resource name of the SAP HANA DB resource. |
| sap_ha_cluster_hana_topology_resource_name<br><br><sup>Type: str</sup> | False<br><br><sup>Default: "SAPHanaTopology_<SID>_<Instance Number>"</sup> | Customize the cluster resource name of the SAP HANA Topology resource. |
| sap_ha_cluster_replication_type<br><br><sup>Type: str</sup> | False<br><br><sup>Default: "none"</sup> | The type of SAP HANA site replication across multiple hosts. |
| sap_ha_cluster_sap_type<br><br><sup>Type: str</sup> | False<br><br><sup>Default: "scaleup"</sup> | The SAP landscape to be installed. |
<!-- END: Role Input Parameters -->
