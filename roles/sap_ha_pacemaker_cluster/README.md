<!-- BEGIN Title -->
# sap_ha_pacemaker_cluster Ansible Role
<!-- END Title -->
![Ansible Lint for sap_ha_pacemaker_cluster](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_ha_pacemaker_cluster.yml/badge.svg)

## Description
<!-- BEGIN Description -->
The Ansible Role `sap_ha_pacemaker_cluster` is used to install and configure Linux Pacemaker High Availability clusters for SAP HANA and SAP Netweaver systems on various infrastructure platforms.
<!-- END Description -->

<!-- BEGIN Dependencies -->
## Dependencies
- `fedora.linux_system_roles`
    - Roles:
        - `ha_cluster`

Install required collections by `ansible-galaxy install -vv -r meta/collection-requirements.yml`.
<!-- END Dependencies -->

<!-- BEGIN Prerequisites -->
## Prerequisites
Infrastructure:
- It is required to create them manually or using [sap_vm_provision](https://github.com/sap-linuxlab/community.sap_infrastructure/tree/main/roles/sap_vm_provision) role, because this role does not create any Cloud platform resources that are required by Resource Agents.

Managed nodes:
- Supported SAP system is installed. See [Recommended](#recommended) section.
- SAP HANA System Replication is configured for SAP HANA HA cluster. See [Recommended](#recommended) section.
- Operating system has access to all required packages
- All required ports are open (details below)

| SAP HANA System Replication process | Port |
| --- | --- |
| hdbnameserver<br/><sub> used for log and data shipping from a primary site to a secondary site.<br/>System DB port number plus 10,000</sub> | 4`<sap_hana_instance_number>`01 |
| hdbnameserver<br/><sub> unencrypted metadata communication between sites.<br/>System DB port number plus 10,000</sub> | 4`<sap_hana_instance_number>`02 |
| hdbnameserver<br/><sub> used for encrypted metadata communication between sites.<br/>System DB port number plus 10,000</sub> | 4`<sap_hana_instance_number>`06 |
| hdbindexserver<br/><sub> used for first MDC Tenant database schema</sub> | 4`<sap_hana_instance_number>`03 |
| hdbxsengine<br/><sub> used for SAP HANA XSC/XSA</sub> | 4`<sap_hana_instance_number>`07|
| hdbscriptserver<br/><sub> used for log and data shipping from a primary site to a secondary site.<br/>Tenant port number plus 10,000</sub> | 4`<sap_hana_instance_number>`40-97 |
| hdbxsengine<br/><sub> used for log and data shipping from a primary site to a secondary site.<br/>Tenant port number plus 10,000</sub> | 4`<sap_hana_instance_number>`40-97 |

| Linux Pacemaker process | Port |
| --- | --- |
| pcsd<br/><sub> cluster nodes requirement for node-to-node communication</sub> | 2224 (TCP)|
| pacemaker<br/><sub> cluster nodes requirement for Pacemaker Remote service daemon</sub> | 3121 (TCP) |
| corosync<br/><sub> cluster nodes requirement for node-to-node communication</sub> | 5404-5412 (UDP) |
<!-- END Prerequisites -->

## Execution
<!-- BEGIN Execution -->
**:warning: This ansible role will destroy and then recreate Linux Pacemaker cluster in process.**</br>
:warning: Do not execute this Ansible Role against existing Linux Pacemaker clusters unless you know what you are doing and you prepare inputs according to existing cluster.

### Supported Platforms
| Platform | Status | Notes |
| -------- | --------- | --------- |
| Physical server | :heavy_check_mark: | Need to specify valid fence agent |
| AWS EC2 Virtual Servers | :heavy_check_mark: | |
| Google Cloud Compute Engine Virtual Machine | :heavy_check_mark: | |
| Microsoft Azure Virtual Machines | :heavy_check_mark: | |
| IBM Cloud Virtual Server | :heavy_check_mark: | |
| IBM Power Virtual Server from IBM Cloud | :heavy_check_mark: | |
| IBM PowerVC hypervisor Virtual Machine | :heavy_check_mark: | |
| OVirt VM | :heavy_check_mark: | |

### Supported scenarios

| Platform | Variant | Status |
| -------- | --------- | --------- |
| SAP HANA scale-up (performance-optimized) 2 nodes | SAPHanaSR Classic | :heavy_check_mark: |
| SAP HANA scale-up (performance-optimized) 2 nodes | SAPHanaSR-angi | :heavy_check_mark: |
| SAP NetWeaver (ABAP) ASCS and ERS 2 nodes | Classic | :heavy_check_mark: |
| SAP NetWeaver (ABAP) ASCS and ERS 2 nodes | Simple Mount | :heavy_check_mark: |
| SAP NetWeaver (JAVA) SCS and ERS 2 nodes | Classic | :heavy_check_mark: |
| SAP NetWeaver (JAVA) SCS and ERS 2 nodes | Simple Mount | :heavy_check_mark: |

**NOTE: SAP Netweaver ASCS/ERS and SCS/ERS are ENSA2 by default, but ENSA1 is also supported.**
<!-- END Execution -->

<!-- BEGIN Execution Recommended -->
### Recommended
It is recommended to execute this role together with other roles in this collection, in the following order:</br>
#### SAP HANA cluster
1. [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure)
2. [sap_hana_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_preconfigure)
3. [sap_install_media_detect](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_install_media_detect)
4. [sap_hana_install](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_install)
5. [sap_ha_install_hana_hsr](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_install_hana_hsr)
6. *`sap_ha_pacemaker_cluster`*

#### SAP Netweaver cluster
1. [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure)
2. [sap_netweaver_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_netweaver_preconfigure) 
3. [sap_install_media_detect](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_install_media_detect)
4. [sap_swpm](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_swpm)
5. *`sap_ha_pacemaker_cluster`*
<!-- END Execution Recommended -->

### Execution Flow
<!-- BEGIN Execution Flow -->
1. Assert that required inputs were provided.
2. Detect target infrastructure platform and prepare recommended inputs unless they were provided.
3. Prepare variables with all cluster parameters and resources.
4. Execute role `ha_cluster` from Ansible Collection `fedora.linux_system_roles` with prepared inputs.
5. Execute SAP product specific post tasks and verify cluster is running.
<!-- END Execution Flow -->

### Example
<!-- BEGIN Execution Example -->
```yaml
---
- name: Ansible Play for SAP HANA HA Scale-up cluster setup
  hosts: hana_primary, hana_secondary
  become: true
  tasks:
    - name: Execute Ansible Role sap_ha_pacemaker_cluster
      ansible.builtin.include_role:
        name: community.sap_install.sap_ha_pacemaker_cluster
      vars:
        sap_ha_pacemaker_cluster_cluster_name: clusterhdb
        sap_ha_pacemaker_cluster_hacluster_user_password: 'clusterpass'

        sap_ha_pacemaker_cluster_sap_type: saphana_scaleup
        sap_ha_pacemaker_cluster_host_type:
          - hana_scaleup_perf

        sap_ha_pacemaker_cluster_hana_sid: "H01"
        sap_ha_pacemaker_cluster_hana_instance_nr: "01"

        sap_ha_pacemaker_cluster_cluster_nodes:
          - node_name: h01hana0
            node_ip: "10.10.10.10"
            node_role: primary
            hana_site: DC01

          - node_name: h01hana1
            node_ip: "10.10.10.11"
            node_role: secondary
            hana_site: DC02
        sap_ha_pacemaker_cluster_replication_type: none
        sap_ha_pacemaker_cluster_vip_resource_group_name: viphdb
```
<!-- END Execution Example -->

<!-- BEGIN Role Tags -->
<!-- END Role Tags -->

<!-- BEGIN Further Information -->
## Further Information
For more examples on how to use this role in different installation scenarios, refer to the [ansible.playbooks_for_sap](https://github.com/sap-linuxlab/ansible.playbooks_for_sap) playbooks.

Cluster can be further customized with inputs available from underlying role [ha_cluster](https://github.com/linux-system-roles/ha_cluster/blob/main/README.md), which will take precedence over `sap_ha_pacemaker_cluster` inputs.
<!-- END Further Information -->

## License
<!-- BEGIN License -->
Apache 2.0
<!-- END License -->

## Maintainers
<!-- BEGIN Maintainers -->
- [Janine Fuchs](https://github.com/ja9fuchs)
- [Marcel Mamula](https://github.com/marcelmamula)
<!-- END Maintainers -->

## Role Variables
<!-- BEGIN Role Variables -->
Minimum required parameters for all clusters:

- [sap_ha_pacemaker_cluster_hacluster_user_password](#sap_ha_pacemaker_cluster_hacluster_user_password)

Additional minimum requirements depend on the type of cluster setup and on the target platform.

### sap_ha_pacemaker_cluster_aws_access_key_id
- _Type:_ `string`<br>

AWS access key to allow control of instances (for example for fencing operations).<br>
Mandatory for the cluster nodes setup on AWS EC2 instances, when:<br>
1. IAM Role or Instance profile is not attached to EC2 instance.<br>
2. `sap_ha_pacemaker_cluster_aws_credentials_setup` is `true`<br>

### sap_ha_pacemaker_cluster_aws_credentials_setup
- _Type:_ `string`<br>

Set this parameter to 'true' to store AWS credentials into /root/.aws/credentials.<br>
Requires: `sap_ha_pacemaker_cluster_aws_access_key_id` and `sap_ha_pacemaker_cluster_aws_secret_access_key`<br>
Mandatory for the cluster nodes setup on AWS EC2 instances, when:<br>
1. IAM Role or Instance profile is not attached to EC2 instance.<br>

### sap_ha_pacemaker_cluster_aws_region
- _Type:_ `string`<br>

The AWS region in which the instances to be used for the cluster setup are located.<br>
Mandatory for cluster nodes setup on AWS EC2 instances.<br>

### sap_ha_pacemaker_cluster_aws_secret_access_key
- _Type:_ `string`<br>

AWS secret key, paired with the access key for instance control.<br>
Mandatory for the cluster nodes setup on AWS EC2 instances, when:<br>
1. IAM Role or Instance profile is not attached to EC2 instance.<br>
2. `sap_ha_pacemaker_cluster_aws_credentials_setup` is `true`<br>

### sap_ha_pacemaker_cluster_aws_vip_update_rt
- _Type:_ `string`<br>

List one more routing table IDs for managing Virtual IP failover through routing table changes.<br>
Multiple routing tables must be defined as a comma-separated string (no spaces).<br>
Mandatory for the VIP resource configuration in AWS EC2 environments.<br>

### sap_ha_pacemaker_cluster_cluster_name
- _Type:_ `string`<br>

The name of the pacemaker cluster.<br>
Inherits the `ha_cluster` LSR native parameter `ha_cluster_cluster_name` if not defined.<br>
If not defined, the `ha_cluster` Linux System Role default will be used.<br>

### sap_ha_pacemaker_cluster_cluster_nodes
- _Type:_ `list`<br>

List of cluster nodes and associated attributes to describe the target SAP HA environment.<br>
This is required for the HANA System Replication configuration.<br>
Synonym for this parameter is `sap_hana_cluster_nodes`.<br>
Mandatory to be defined for HANA clusters.<br>

- **hana_site**<br>
Site of the cluster and/or SAP HANA System Replication node (for example 'DC01').<br>Mandatory for HANA clusters (sudo config for system replication).
- **node_ip**<br>
IP address of the node used for HANA System Replication.<br>_Optional. Currently not needed/used in cluster configuration._
- **node_name**<br>
Hostname of the cluster node.<br>_Optional. Currently not needed/used in cluster configuration._
- **node_role**<br>
_Choices:_ `primary, secondary`<br>
Role of the defined `node_name` in the SAP HANA cluster setup.<br>There must be only **one** primary, but there can be multiple secondary nodes.<br>_Optional. Currently not needed/used in cluster configuration._

Example:
```yaml
sap_ha_pacemaker_cluster_cluster_nodes:
- hana_site: DC01
  node_ip: 192.168.5.1
  node_name: nodeA
  node_role: primary
- hana_site: DC02
```
### sap_ha_pacemaker_cluster_cluster_properties
- _Type:_ `dict`<br>
- _Default:_ `{'concurrent-fencing': True, 'stonith-enabled': True, 'stonith-timeout': 900}`<br>

Standard pacemaker cluster properties are configured with recommended settings for cluster node fencing.<br>
When no STONITH resource is defined, STONITH will be disabled and a warning displayed.<br>

Example:
```yaml
sap_ha_pacemaker_cluster_cluster_properties:
  concurrent-fencing: true
  stonith-enabled: true
  stonith-timeout: 900
```
### sap_ha_pacemaker_cluster_create_config_dest
- _Type:_ `string`<br>
- _Default:_ `review_resource_config.yml`<br>

The pacemaker cluster resource configuration optionally created by this role will be saved in a Yaml file in the current working directory.<br>
Requires `sap_ha_pacemaker_cluster_create_config_varfile` to be enabled for generating the output file.<br>
Specify a path/filename to save the file in a custom location.<br>
The file can be used as input vars file for an Ansible playbook running the 'ha_cluster' Linux System Role.<br>

### sap_ha_pacemaker_cluster_create_config_varfile
- _Type:_ `bool`<br>
- _Default:_ `False`<br>

When enabled, all cluster configuration parameters this role constructs for executing the 'ha_cluster' Linux System role will be written into a file in Yaml format.<br>
This allows using the output file later as input file for additional custom steps using the 'ha_cluster' role and covering the resource configuration in a cluster that was set up using this 'sap_ha_pacemaker_cluster' role.<br>
When enabled this parameters file is also created when the playbook is run in check_mode (`--check`) and can be used to review the configuration parameters without executing actual changes on the target nodes.<br>
WARNING! This report may include sensitive details like secrets required for certain cluster resources!<br>

### sap_ha_pacemaker_cluster_enable_cluster_connector
- _Type:_ `bool`<br>
- _Default:_ `True`<br>

Enables/Disables the SAP HA Interface for SAP ABAP application server instances, also known as `sap_cluster_connector`.<br>
Set this parameter to 'false' if the SAP HA interface should not be installed and configured.<br>

### sap_ha_pacemaker_cluster_extra_packages
- _Type:_ `list`<br>

Additional extra packages to be installed, for instance specific resource packages.<br>
For SAP clusters configured by this role, the relevant standard packages for the target scenario are automatically included.<br>

### sap_ha_pacemaker_cluster_fence_agent_packages
- _Type:_ `list`<br>

Additional fence agent packages to be installed.<br>
This is automatically combined with default packages in:<br>
`__sap_ha_pacemaker_cluster_fence_agent_packages_minimal`<br>
`__sap_ha_pacemaker_cluster_fence_agent_packages_platform`<br>

### sap_ha_pacemaker_cluster_gcp_project
- _Type:_ `string`<br>

Google Cloud project name in which the target instances are installed.<br>
Mandatory for the cluster setup on GCP instances.<br>

### sap_ha_pacemaker_cluster_gcp_region_zone
- _Type:_ `string`<br>

Google Cloud Platform region zone ID.<br>
Mandatory for the cluster setup on GCP instances.<br>

### sap_ha_pacemaker_cluster_ha_cluster
- _Type:_ `dict`<br>

The `ha_cluster` LSR native parameter `ha_cluster` can be used as a synonym.<br>
Optional _**host_vars**_ parameter - if defined it must be set for each node.<br>
Dictionary that can contain various node options for the pacemaker cluster configuration.<br>
Supported options can be reviewed in the `ha_cluster` Linux System Role [https://github.com/linux-system-roles/ha_cluster/blob/master/README.md].<br>
If not defined, the `ha_cluster` Linux System Role default will be used.<br>

Example:
```yaml
sap_ha_pacemaker_cluster_ha_cluster:
  corosync_addresses:
  - 192.168.1.10
  - 192.168.2.10
  node_name: nodeA
```
### sap_ha_pacemaker_cluster_hacluster_user_password <sup>required</sup>
- **Required**<br>
- _Type:_ `string`<br>

The password of the `hacluster` user which is created during pacemaker installation.<br>
Inherits the value of `ha_cluster_hacluster_password`, when defined.<br>

### sap_ha_pacemaker_cluster_hana_automated_register
- _Type:_ `bool`<br>
- _Default:_ `True`<br>

Parameter for the 'SAPHana' cluster resource.<br>
Define if a former primary should be re-registered automatically as secondary.<br>

### sap_ha_pacemaker_cluster_hana_colocation_hana_vip_primary_name
- _Type:_ `string`<br>
- _Default:_ `col_saphana_vip_<SID>_HDB<Instance Number>_primary`<br>

Customize the cluster constraint name for VIP and SAPHana primary clone colocation.<br>

### sap_ha_pacemaker_cluster_hana_colocation_hana_vip_secondary_name
- _Type:_ `string`<br>
- _Default:_ `col_saphana_vip_<SID>_HDB<Instance Number>_readonly`<br>

Customize the cluster constraint name for VIP and SAPHana secondary clone colocation.<br>

### sap_ha_pacemaker_cluster_hana_duplicate_primary_timeout
- _Type:_ `int`<br>
- _Default:_ `7200`<br>

Parameter for the 'SAPHana' cluster resource.<br>
Time difference needed between to primary time stamps, if a dual-primary situation occurs.<br>
If the time difference is less than the time gap, then the cluster holds one or both instances in a "WAITING" status.<br>
This is to give an admin a chance to react on a failover. A failed former primary will be registered after the time difference is passed.<br>

### sap_ha_pacemaker_cluster_hana_filesystem_resource_clone_name
- _Type:_ `string`<br>
- _Default:_ `cln_SAPHanaFil_<SID>_HDB<Instance Number>`<br>

Customize the cluster resource name of the SAP HANA Filesystem clone.<br>

### sap_ha_pacemaker_cluster_hana_filesystem_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_SAPHanaFil_<SID>_HDB<Instance Number>`<br>

Customize the cluster resource name of the SAP HANA Filesystem.<br>

### sap_ha_pacemaker_cluster_hana_global_ini_path
- _Type:_ `string`<br>
- _Default:_ `/usr/sap/<SID>/SYS/global/hdb/custom/config/global.ini`<br>

Path with location of global.ini for srHook update<br>

### sap_ha_pacemaker_cluster_hana_hook_chksrv
- _Type:_ `bool`<br>
- _Default:_ `False`<br>

Controls if ChkSrv srHook is enabled during srHook creation.<br>
It is ignored when sap_ha_pacemaker_cluster_hana_hooks is defined.<br>

### sap_ha_pacemaker_cluster_hana_hook_tkover
- _Type:_ `bool`<br>
- _Default:_ `False`<br>

Controls if TkOver srHook is enabled during srHook creation.<br>
It is ignored when sap_ha_pacemaker_cluster_hana_hooks is defined.<br>

### sap_ha_pacemaker_cluster_hana_hooks
- _Type:_ `list`<br>
- _Default:_ `[]`<br>

Customize required list of SAP HANA Hooks<br>
Mandatory to include SAPHanaSR srHook in list.<br>
Mandatory attributes are provider and path.<br>
Example below shows mandatory SAPHanaSR, TkOver and ChkSrv hooks.<br>

Example:
```yaml
sap_ha_pacemaker_cluster_hana_hooks:
  - options:
    - name: execution_order
      value: 1
    path: /usr/share/SAPHanaSR/
    provider: SAPHanaSR
  - options:
    - name: execution_order
      value: 2
    path: /usr/share/SAPHanaSR/
    provider: susTkOver
  - options:
    - name: execution_order
      value: 3
    - name: action_on_lost
      value: stop
    path: /usr/share/SAPHanaSR/
    provider: susChkSrv
```
### sap_ha_pacemaker_cluster_hana_instance_nr
- _Type:_ `string`<br>

The instance number of the SAP HANA database which this role will configure in the cluster.<br>
Inherits the value of `sap_hana_instance_number`, when defined.<br>
Mandatory for SAP HANA cluster scenarios.<br>

### sap_ha_pacemaker_cluster_hana_order_hana_vip_primary_name
- _Type:_ `string`<br>
- _Default:_ `ord_saphana_vip_<SID>_HDB<Instance Number>_primary`<br>

Customize the cluster constraint name for VIP and SAPHana primary clone order.<br>

### sap_ha_pacemaker_cluster_hana_order_hana_vip_secondary_name
- _Type:_ `string`<br>
- _Default:_ `ord_saphana_vip_<SID>_HDB<Instance Number>_readonly`<br>

Customize the cluster constraint name for VIP and SAPHana secondary clone order.<br>

### sap_ha_pacemaker_cluster_hana_order_topology_hana_name
- _Type:_ `string`<br>
- _Default:_ `ord_saphana_saphanatop_<SID>_HDB<Instance Number>`<br>

Customize the cluster constraint name for SAPHana and Topology order.<br>

### sap_ha_pacemaker_cluster_hana_prefer_site_takeover
- _Type:_ `bool`<br>
- _Default:_ `True`<br>

Parameter for the 'SAPHana' cluster resource.<br>
Set to "false" if the cluster should first attempt to restart the instance on the same node.<br>
When set to "true" (default) a failover to secondary will be initiated on resource failure.<br>

### sap_ha_pacemaker_cluster_hana_resource_clone_msl_name
- _Type:_ `string`<br>
- _Default:_ `msl_SAPHana_<SID>_HDB<Instance Number>`<br>

Customize the cluster resource name of the SAP HANA DB resource master slave clone.<br>
Master Slave clone is specific to Classic SAPHana resource on SUSE (non-angi).<br>

### sap_ha_pacemaker_cluster_hana_resource_clone_name
- _Type:_ `string`<br>
- _Default:_ `cln_SAPHana_<SID>_HDB<Instance Number>`<br>

Customize the cluster resource name of the SAP HANA DB resource clone.<br>

### sap_ha_pacemaker_cluster_hana_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_SAPHana_<SID>_HDB<Instance Number>`<br>

Customize the cluster resource name of the SAP HANA DB resource.<br>

### sap_ha_pacemaker_cluster_hana_sid
- _Type:_ `string`<br>

The SAP HANA System ID (SID) of the instance that will be configured in the cluster.<br>
The SID must follow SAP specifications - see SAP Note 1979280.<br>
Inherits the value of `sap_hana_sid`, when defined.<br>
Mandatory for SAP HANA cluster scenarios.<br>

### sap_ha_pacemaker_cluster_hana_topology_resource_clone_name
- _Type:_ `string`<br>
- _Default:_ `cln_SAPHanaTop_<SID>_HDB<Instance Number>`<br>

Customize the cluster resource name of the SAP HANA Topology resource clone.<br>

### sap_ha_pacemaker_cluster_hana_topology_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_SAPHanaTop_<SID>_HDB<Instance Number>`<br>

Customize the cluster resource name of the SAP HANA Topology resource.<br>

### sap_ha_pacemaker_cluster_hanacontroller_resource_clone_name
- _Type:_ `string`<br>
- _Default:_ `cln_SAPHanaCon_<SID>_HDB<Instance Number>`<br>

Customize the cluster resource name of the SAP HANA Controller clone.<br>

### sap_ha_pacemaker_cluster_hanacontroller_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_SAPHanaCon_<SID>_HDB<Instance Number>`<br>

Customize the cluster resource name of the SAP HANA Controller.<br>

### sap_ha_pacemaker_cluster_healthcheck_hana_primary_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_vip_health_check_<SID>_HDB<Instance Number>_primary`<br>

Name of the Virtual IP Health Check resource for primary HANA instance.<br>

### sap_ha_pacemaker_cluster_healthcheck_hana_secondary_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_vip_health_check_<SID>_HDB<Instance Number>_readonly`<br>

Name of the Virtual IP Health Check resource for read-only HANA instance.<br>

### sap_ha_pacemaker_cluster_healthcheck_nwas_abap_aas_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_vip_health_check_<SID>_AAS<AAS-instance-number>`<br>

Name of the Virtual IP Health Check resource for NetWeaver AAS.<br>

### sap_ha_pacemaker_cluster_healthcheck_nwas_abap_pas_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_vip_health_check_<SID>_PAS<PAS-instance-number>`<br>

Name of the Virtual IP Health Check resource for NetWeaver PAS.<br>

### sap_ha_pacemaker_cluster_healthcheck_nwas_ascs_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_vip_health_check_<SID>_ASCS<ASCS-instance-number>`<br>

Name of the Virtual IP Health Check resource for NetWeaver ABAP Central Services (ASCS).<br>

### sap_ha_pacemaker_cluster_healthcheck_nwas_ers_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_vip_health_check_<SID>_ERS<ERS-instance-number>`<br>

Name of the Virtual IP Health Check resource for NetWeaver Enqueue Replication Service (ERS).<br>

### sap_ha_pacemaker_cluster_healthcheck_nwas_scs_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_vip_health_check_<SID>_SCS<SCS-instance-number>`<br>

Name of the Virtual IP Health Check resource for NetWeaver Central Services (SCS).<br>

### sap_ha_pacemaker_cluster_host_type
- _Type:_ `list`<br>
- _Default:_ `hana_scaleup_perf`<br>
- _Choices:_ `hana_scaleup_perf, nwas_abap_ascs_ers, nwas_java_scs_ers`<br>

The SAP landscape to for which the cluster is to be configured.<br>
The default is a 2-node SAP HANA scale-up cluster.<br>

### sap_ha_pacemaker_cluster_ibmcloud_api_key
- _Type:_ `string`<br>

The API key which is required to allow the control of instances (for example for fencing operations).<br>
Mandatory for the cluster setup on IBM Cloud Virtual Server instances or IBM Power Virtual Server on IBM Cloud.<br>

### sap_ha_pacemaker_cluster_ibmcloud_powervs_api_type
- _Type:_ `string`<br>

IBM Power Virtual Server API Endpoint type (public or private) dependent on network interface attachments for the target instances.<br>
Mandatory for the cluster setup on IBM Power Virtual Server from IBM Cloud.<br>

### sap_ha_pacemaker_cluster_ibmcloud_powervs_forward_proxy_url
- _Type:_ `string`<br>

IBM Power Virtual Server forward proxy url when IBM Power Virtual Server API Endpoint type is set to private.<br>
When public network interface, can be ignored.<br>
When private network interface, mandatory for the cluster setup on IBM Power Virtual Server from IBM Cloud.<br>

### sap_ha_pacemaker_cluster_ibmcloud_powervs_workspace_crn
- _Type:_ `string`<br>

IBM Power Virtual Server Workspace service cloud resource name (CRN) identifier which contains the target instances<br>
Mandatory for the cluster setup on IBM Power Virtual Server from IBM Cloud.<br>

### sap_ha_pacemaker_cluster_ibmcloud_region
- _Type:_ `string`<br>

The IBM Cloud VS region name in which the instances are running.<br>
Mandatory for the cluster setup on IBM Cloud Virtual Server instances or IBM Power Virtual Server on IBM Cloud.<br>

### sap_ha_pacemaker_cluster_msazure_resource_group
- _Type:_ `string`<br>

Resource group name/ID in which the target instances are defined.<br>
Mandatory for the cluster setup on MS Azure instances.<br>

### sap_ha_pacemaker_cluster_msazure_subscription_id
- _Type:_ `string`<br>

Subscription ID of the MS Azure environment containing the target instances.<br>
Mandatory for the cluster setup on MS Azure instances.<br>

### sap_ha_pacemaker_cluster_nwas_abap_aas_instance_nr
- _Type:_ `string`<br>

Instance number of the NetWeaver ABAP AAS instance.<br>
Mandatory for NetWeaver AAS cluster configuration.<br>

### sap_ha_pacemaker_cluster_nwas_abap_pas_instance_nr
- _Type:_ `string`<br>

Instance number of the NetWeaver ABAP PAS instance.<br>
Mandatory for NetWeaver PAS cluster configuration.<br>

### sap_ha_pacemaker_cluster_nwas_ascs_filesystem_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_fs_<SID>_ASCS<ASCS-instance-number>`<br>

Name of the filesystem resource for the ASCS instance.<br>

### sap_ha_pacemaker_cluster_nwas_ascs_instance_nr
- _Type:_ `string`<br>

Instance number of the NetWeaver ABAP Central Services (ASCS) instance.<br>
Mandatory for NetWeaver ASCS/ERS cluster configuration.<br>

### sap_ha_pacemaker_cluster_nwas_ascs_sapinstance_instance_name
- _Type:_ `string`<br>

The name of the ASCS instance, typically the profile name.<br>
Mandatory for the NetWeaver ASCS/ERS cluster setup<br>
Recommended format <SID>_ASCS<ASCS-instance-number>_<ASCS-hostname><br>

### sap_ha_pacemaker_cluster_nwas_ascs_sapinstance_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_SAPInstance_<SID>_ASCS<ASCS-instance-number>`<br>

Name of the ASCS instance resource.<br>

### sap_ha_pacemaker_cluster_nwas_ascs_sapinstance_start_profile_string
- _Type:_ `string`<br>

The full path and name of the ASCS instance profile.<br>
Mandatory for the NetWeaver ASCS/ERS cluster setup.<br>

### sap_ha_pacemaker_cluster_nwas_ascs_sapstartsrv_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_SAPStartSrv_<SID>_ASCS<ASCS-instance-number>`<br>

Name of the ASCS SAPStartSrv resource for simple mount.<br>

### sap_ha_pacemaker_cluster_nwas_colocation_ascs_no_ers_name
- _Type:_ `string`<br>
- _Default:_ `col_ascs_separate_<SID>`<br>

Customize the cluster constraint name for ASCS and ERS separation colocation.<br>

### sap_ha_pacemaker_cluster_nwas_colocation_scs_no_ers_name
- _Type:_ `string`<br>
- _Default:_ `col_ascs_separate_<SID>`<br>

Customize the cluster constraint name for SCS and ERS separation colocation.<br>

### sap_ha_pacemaker_cluster_nwas_cs_ensa1
- _Type:_ `bool`<br>
- _Default:_ `False`<br>

The standard NetWeaver Central Services cluster will be set up as ENSA2.<br>
Set this parameter to 'true' to configure it as ENSA1.<br>

### sap_ha_pacemaker_cluster_nwas_cs_ers_simple_mount
- _Type:_ `bool`<br>
- _Default:_ `True`<br>

Enables preferred method for Central Services (ASCS or SCS) ENSA2 clusters - Simple Mount.<br>
Set this parameter to 'true' to configure ENSA2 Simple Mount.<br>

### sap_ha_pacemaker_cluster_nwas_cs_group_stickiness
- _Type:_ `string`<br>
- _Default:_ `3000`<br>

NetWeaver Central Services (ASCS and SCS) resource group stickiness.<br>
Defines how sticky is Central Services group to the node it was started on.<br>

### sap_ha_pacemaker_cluster_nwas_cs_sapinstance_automatic_recover_bool
- _Type:_ `bool`<br>
- _Default:_ `False`<br>

NetWeaver Central Services (ASCS and SCS) instance resource option "AUTOMATIC_RECOVER".<br>

### sap_ha_pacemaker_cluster_nwas_cs_sapinstance_ensa1_failure_timeout
- _Type:_ `string`<br>
- _Default:_ `60`<br>

NetWeaver Central Services (ASCS and SCS) instance failure-timeout attribute.<br>
Only used for ENSA1 setups (see `sap_ha_pacemaker_cluster_nwas_cs_ensa1`). Default setup is ENSA2.<br>

### sap_ha_pacemaker_cluster_nwas_cs_sapinstance_ensa1_migration_threshold
- _Type:_ `string`<br>
- _Default:_ `1`<br>

NetWeaver Central Services (ASCS and SCS) instance migration-threshold setting attribute.<br>
Only used for ENSA1 setups (see `sap_ha_pacemaker_cluster_nwas_cs_ensa1`). Default setup is ENSA2.<br>

### sap_ha_pacemaker_cluster_nwas_cs_sapinstance_resource_stickiness
- _Type:_ `string`<br>
- _Default:_ `5000`<br>

NetWeaver Central Services (ASCS and SCS) instance resource stickiness attribute.<br>

### sap_ha_pacemaker_cluster_nwas_ers_filesystem_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_fs_<SID>_ERS<ERS-instance-number>`<br>

Name of the filesystem resource for the ERS instance.<br>

### sap_ha_pacemaker_cluster_nwas_ers_instance_nr
- _Type:_ `string`<br>

Instance number of the NetWeaver Enqueue Replication Service (ERS) instance.<br>
Mandatory for NetWeaver ASCS/ERS and SCS/ERS cluster configuration.<br>

### sap_ha_pacemaker_cluster_nwas_ers_sapinstance_automatic_recover_bool
- _Type:_ `bool`<br>
- _Default:_ `False`<br>

NetWeaver ERS instance resource option "AUTOMATIC_RECOVER".<br>

### sap_ha_pacemaker_cluster_nwas_ers_sapinstance_instance_name
- _Type:_ `string`<br>

The name of the ERS instance, typically the profile name.<br>
Mandatory for the NetWeaver ASCS/ERS and SCS/ERS clusters.<br>
Recommended format <SID>_ERS<ERS-instance-number>_<ERS-hostname>.<br>

### sap_ha_pacemaker_cluster_nwas_ers_sapinstance_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_SAPInstance_<SID>_ERS<ERS-instance-number>`<br>

Name of the ERS instance resource.<br>

### sap_ha_pacemaker_cluster_nwas_ers_sapinstance_start_profile_string
- _Type:_ `string`<br>

The full path and name of the ERS instance profile.<br>
Mandatory for the NetWeaver ASCS/ERS and SCS/ERS clusters.<br>

### sap_ha_pacemaker_cluster_nwas_ers_sapstartsrv_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_SAPStartSrv_<SID>_ERS<ERS-instance-number>`<br>

Name of the ERS SAPstartSrv resource for simple mount.<br>

### sap_ha_pacemaker_cluster_nwas_order_ascs_first_name
- _Type:_ `string`<br>
- _Default:_ `ord_ascs_first_<SID>`<br>

Customize the cluster constraint name for ASCS starting before ERS order.<br>

### sap_ha_pacemaker_cluster_nwas_order_scs_first_name
- _Type:_ `string`<br>
- _Default:_ `ord_ascs_first_<SID>`<br>

Customize the cluster constraint name for SCS starting before ERS order.<br>

### sap_ha_pacemaker_cluster_nwas_sapmnt_filesystem_resource_clone_name
- _Type:_ `string`<br>
- _Default:_ `cln_fs_<SID>_sapmnt`<br>

Filesystem resource clone name for the shared filesystem /sapmnt.<br>
Enable this resource setup using `sap_ha_pacemaker_cluster_nwas_shared_filesystems_cluster_managed`.<br>

### sap_ha_pacemaker_cluster_nwas_sapmnt_filesystem_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_fs_<SID>_sapmnt`<br>

Filesystem resource name for the shared filesystem /sapmnt.<br>
Optional, this is typically managed by the OS, but can as well be added to the cluster configuration.<br>
Enable this resource setup using `sap_ha_pacemaker_cluster_nwas_shared_filesystems_cluster_managed`.<br>

### sap_ha_pacemaker_cluster_nwas_scs_filesystem_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_fs_<SID>_SCS<SCS-instance-number>`<br>

Name of the filesystem resource for the SCS instance.<br>

### sap_ha_pacemaker_cluster_nwas_scs_instance_nr
- _Type:_ `string`<br>

Instance number of the NetWeaver Central Services (SCS) instance.<br>
Mandatory for NetWeaver SCS/ERS cluster configuration.<br>

### sap_ha_pacemaker_cluster_nwas_scs_sapinstance_instance_name
- _Type:_ `string`<br>

The name of the SCS instance, typically the profile name.<br>
Mandatory for the NetWeaver SCS/ERS cluster setup<br>
Recommended format <SID>_SCS<SCS-instance-number>_<SCS-hostname><br>

### sap_ha_pacemaker_cluster_nwas_scs_sapinstance_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_SAPInstance_<SID>_SCS<SCS-instance-number>`<br>

Name of the SCS instance resource.<br>

### sap_ha_pacemaker_cluster_nwas_scs_sapinstance_start_profile_string
- _Type:_ `string`<br>

The full path and name of the SCS instance profile.<br>
Mandatory for the NetWeaver SCS/ERS cluster setup.<br>

### sap_ha_pacemaker_cluster_nwas_scs_sapstartsrv_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_SAPStartSrv_<SID>_SCS<SCS-instance-number>`<br>

Name of the SCS SAPStartSrv resource for simple mount.<br>

### sap_ha_pacemaker_cluster_nwas_shared_filesystems_cluster_managed
- _Type:_ `bool`<br>
- _Default:_ `False`<br>

Change this parameter to 'true' if the 3 shared filesystems `/usr/sap/trans`, `/usr/sap/<SID>/SYS` and '/sapmnt' shall be configured as cloned cluster resources.<br>

### sap_ha_pacemaker_cluster_nwas_sid
- _Type:_ `string`<br>

System ID (SID) of the NetWeaver instances in Capital letters.<br>
Defaults to `sap_swpm_sid` if defined.<br>
Mandatory for NetWeaver cluster scenarios.<br>

### sap_ha_pacemaker_cluster_nwas_sys_filesystem_resource_clone_name
- _Type:_ `string`<br>
- _Default:_ `cln_fs_<SID>_sys`<br>

Filesystem resource clone name for the shared filesystem /usr/sap/<SID>/SYS.<br>
Enable this resource setup using `sap_ha_pacemaker_cluster_nwas_shared_filesystems_cluster_managed`.<br>

### sap_ha_pacemaker_cluster_nwas_sys_filesystem_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_fs_<SID>_sys`<br>

Filesystem resource name for the transports filesystem /usr/sap/<SID>/SYS.<br>
Optional, this is typically managed by the OS, but can as well be added to the cluster configuration.<br>
Enable this resource setup using `sap_ha_pacemaker_cluster_nwas_shared_filesystems_cluster_managed`.<br>

### sap_ha_pacemaker_cluster_nwas_transports_filesystem_resource_clone_name
- _Type:_ `string`<br>
- _Default:_ `cln_fs_<SID>_trans`<br>

Filesystem resource clone name for the shared filesystem /usr/sap/trans.<br>
Enable this resource setup using `sap_ha_pacemaker_cluster_nwas_shared_filesystems_cluster_managed`.<br>

### sap_ha_pacemaker_cluster_nwas_transports_filesystem_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_fs_<SID>_trans`<br>

Filesystem resource name for the transports filesystem /usr/sap/trans.<br>
Optional, this is typically managed by the OS, but can as well be added to the cluster configuration.<br>
Enable this resource setup using `sap_ha_pacemaker_cluster_nwas_shared_filesystems_cluster_managed`.<br>

### sap_ha_pacemaker_cluster_operation_defaults
- _Type:_ `dict`<br>
- _Default:_ `{'record-pending': True, 'timeout': 600}`<br>

Set default operation parameters that will be valid for all pacemaker resources.<br>

Example:
```yaml
sap_ha_pacemaker_cluster_operation_defaults:
  record-pending: true
  timeout: 600
```
### sap_ha_pacemaker_cluster_resource_defaults
- _Type:_ `dict`<br>
- _Default:_ `{'migration-threshold': 5000, 'resource-stickiness': 3000}`<br>

Set default parameters that will be valid for all pacemaker resources.<br>

Example:
```yaml
sap_ha_pacemaker_cluster_resource_defaults:
  migration-threshold: 5000
  resource-stickiness: 1000
```
### sap_ha_pacemaker_cluster_saphanasr_angi_detection
- _Type:_ `string`<br>
- _Default:_ `True`<br>

Disabling this variable enables to use Classic SAPHanaSR agents even on server, with SAPHanaSR-angi is available.<br>

### sap_ha_pacemaker_cluster_sbd_devices
- _Type:_ `list`<br>

Required if `sap_ha_pacemaker_cluster_sbd_enabled` is enabled.<br>
Provide list of block devices for Stonith SBD agent<br>

Example:
```yaml
sap_ha_pacemaker_cluster_sbd_devices:
  - /dev/disk/by-id/scsi-3600
```
### sap_ha_pacemaker_cluster_sbd_enabled
- _Type:_ `bool`<br>

Set this parameter to 'true' to enable workflow to add Stonith SBD resource.<br>
Stonith SBD resource has to be provided as part of `sap_ha_pacemaker_cluster_stonith_custom`.<br>
Default SBD agents are: stonith:external/sbd for SLES and stonith:fence_sbd for RHEL<br>

Example:
```yaml
sap_ha_pacemaker_cluster_sbd_devices:
  - /dev/disk/by-id/scsi-3600
sap_ha_pacemaker_cluster_sbd_enabled: true
sap_ha_pacemaker_cluster_stonith_custom:
  - agent: stonith:external/sbd
    id: stonith_sbd
    instance_attrs:
    - attrs:
      - name: pcmk_delay_max
        value: 15
```
### sap_ha_pacemaker_cluster_sbd_options
- _Type:_ `list`<br>

Optional if `sap_ha_pacemaker_cluster_sbd_enabled` is enabled.<br>
Provide list of SBD specific options that are added into SBD configuration file.<br>

Example:
```yaml
sap_ha_pacemaker_cluster_sbd_options:
  - name: startmode
    value: clean
```
### sap_ha_pacemaker_cluster_sbd_watchdog
- _Type:_ `str`<br>
- _Default:_ `/dev/watchdog`<br>

Optional if `sap_ha_pacemaker_cluster_sbd_enabled` is enabled.<br>
Provide watchdog name to override default /dev/watchdog<br>

### sap_ha_pacemaker_cluster_sbd_watchdog_modules
- _Type:_ `list`<br>

Optional if `sap_ha_pacemaker_cluster_sbd_enabled` is enabled.<br>
Provide list of watchdog kernel modules to be loaded (creates /dev/watchdog* devices).<br>

Example:
```yaml
sap_ha_pacemaker_cluster_sbd_watchdog_modules:
  - softdog
```
### sap_ha_pacemaker_cluster_stonith_custom
- _Type:_ `list`<br>

Custom list of STONITH resource(s) to be configured in the cluster.<br>
This definition override any defaults the role would apply otherwise.<br>
Definition follows structure of ha_cluster_resource_primitives in linux-system-roles/ha_cluster<br>

- **agent**<br>
**Required**<br>
_Type:_ `str`<br>
Resource agent name, must contain the prefix "stonith:" to avoid mismatches or failures.
- **id**<br>
_Type:_ `str`<br>
Parameter `id` is required.<br>Name that will be used as the resource ID (name).
- **instance_attrs**<br>
_Type:_ `list`<br>
Defines resource agent params as list of name/value pairs.<br>Requires the mandatory options for the particular stonith resource agent to be defined, otherwise the setup will fail.<br>Example: stonith:fence_sbd agent requires devices option with list of SBD disks.<br>Example: stonith:external/sbd agent does not require devices option, but `sap_ha_pacemaker_cluster_sbd_devices`.
- **meta_attrs**<br>
_Type:_ `list`<br>
Defines meta attributes as list of name/value pairs.
- **name**<br>
_Type:_ `str`<br>
WARNING! This option will be removed in future release.
- **operations**<br>
_Type:_ `list`<br>
Defines list of resource agent operations.
- **options**<br>
_Type:_ `dict`<br>
WARNING! This option will be removed in future release.

Example:
```yaml
sap_ha_pacemaker_cluster_stonith_custom:
  - agent: stonith:fence_rhevm
    id: my-fence-resource
    instance_attrs:
    - attrs:
      - name: ip
        value: rhevm-server
      - name: username
        value: login-user
      - name: password
        value: login-user-password
      - name: pcmk_host_list
        value: node1,node2
      - name: power_wait
        value: 3
    meta_attrs:
    - attrs:
      - name: target-role
        value: Started
    operations:
    - action: start
      attrs:
      - name: interval
        value: 0
      - name: timeout
        value: 180
```
### sap_ha_pacemaker_cluster_storage_definition
- _Type:_ `list`<br>

List of filesystem definitions used for filesystem cluster resources.<br>
Options relevant, see example.<br>
Mandatory for SAP NetWeaver cluster without Simple Mount.<br>
Reuse `sap_storage_setup_definition` if defined.<br>
Reuse `sap_storage_setup_definition` will extract values 'mountpoint', 'nfs_filesystem_type', 'nfs_mount_options', 'nfs_path', 'nfs_server'.<br>
Reuse `sap_storage_setup_definition` all options are documented under Ansible Role `sap_storage_setup`.<br>
Note! For this variable, the argument specification does not list options, to avoid errors during reuse of `sap_storage_setup_definition` if defined.<br>

Example:
```yaml
sap_ha_pacemaker_cluster_storage_definition:
  - mountpoint: /usr/sap
    name: usr_sap
    nfs_path: /usr/sap
    nfs_server: nfs-server.example.com:/
  - mountpoint: /usr/sap/trans
    name: usr_sap_trans
    nfs_path: /usr/sap/trans
    nfs_server: nfs-server.example.com:/
  - mountpoint: /sapmnt
    name: sapmnt
    nfs_filesystem_type: nfs
    nfs_mount_options: defaults
    nfs_path: /sapmnt
    nfs_server: nfs-server.example.com:/
```
### sap_ha_pacemaker_cluster_storage_nfs_filesystem_type
- _Type:_ `string`<br>
- _Default:_ `nfs`<br>

Filesystem type of the NFS filesystems that are part of the cluster configuration.<br>

### sap_ha_pacemaker_cluster_storage_nfs_mount_options
- _Type:_ `string`<br>
- _Default:_ `defaults`<br>

Mount options of the NFS filesystems that are part of the cluster configuration.<br>

### sap_ha_pacemaker_cluster_storage_nfs_server
- _Type:_ `string`<br>

Default address of the NFS server, if not defined individually by filesystem.<br>

### sap_ha_pacemaker_cluster_system_roles_collection
- _Type:_ `string`<br>
- _Default:_ `fedora.linux_system_roles`<br>

Reference to the Ansible Collection used for the Linux System Roles.<br>
For community/upstream, use 'fedora.linux_system_roles'.<br>
For RHEL System Roles for SAP, or Red Hat Automation Hub, use 'redhat.rhel_system_roles'.<br>

### sap_ha_pacemaker_cluster_vip_client_interface
- _Type:_ `string`<br>

OS device name of the network interface to use for the Virtual IP configuration.<br>
When there is only one interface on the system, its name will be used by default.<br>

### sap_ha_pacemaker_cluster_vip_hana_primary_ip_address
- _Type:_ `string`<br>

The virtual IP of the primary HANA instance.<br>
Mandatory parameter for HANA clusters.<br>

### sap_ha_pacemaker_cluster_vip_hana_primary_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_vip_<SID>_HDB<Instance Number>_primary`<br>

Name of the Virtual IP resource for primary HANA instance.<br>

### sap_ha_pacemaker_cluster_vip_hana_secondary_ip_address
- _Type:_ `string`<br>

The virtual IP for read-only access to the secondary HANA instance.<br>
Optional parameter in HANA clusters.<br>

### sap_ha_pacemaker_cluster_vip_hana_secondary_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_vip_<SID>_HDB<Instance Number>_readonly`<br>

Name of the Virtual IP resource for read-only HANA instance.<br>

### sap_ha_pacemaker_cluster_vip_nwas_abap_aas_ip_address
- _Type:_ `string`<br>

Virtual IP of the NetWeaver AAS instance.<br>
Mandatory for NetWeaver AAS cluster setup.<br>

### sap_ha_pacemaker_cluster_vip_nwas_abap_aas_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_vip_<SID>_AAS<AAS-instance-number>`<br>

Name of the Virtual IP resource for NetWeaver AAS.<br>

### sap_ha_pacemaker_cluster_vip_nwas_abap_pas_ip_address
- _Type:_ `string`<br>

Virtual IP of the NetWeaver PAS instance.<br>
Mandatory for NetWeaver PAS cluster setup.<br>

### sap_ha_pacemaker_cluster_vip_nwas_abap_pas_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_vip_<SID>_PAS<PAS-instance-number>`<br>

Name of the Virtual IP resource for NetWeaver PAS.<br>

### sap_ha_pacemaker_cluster_vip_nwas_ascs_ip_address
- _Type:_ `string`<br>

Virtual IP of the NetWeaver ABAP Central Services (ASCS) instance.<br>
Mandatory for NetWeaver ASCS/ERS cluster setup.<br>

### sap_ha_pacemaker_cluster_vip_nwas_ascs_resource_group_name
- _Type:_ `string`<br>
- _Default:_ `grp_<SID>_ASCS<ASCS-instance-number>`<br>

Name of the NetWeaver ASCS resource group.<br>

### sap_ha_pacemaker_cluster_vip_nwas_ascs_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_vip_<SID>_ASCS<ASCS-instance-number>`<br>

Name of the Virtual IP resource for NetWeaver ABAP Central Services (ASCS).<br>

### sap_ha_pacemaker_cluster_vip_nwas_ers_ip_address
- _Type:_ `string`<br>

Virtual IP of the NetWeaver Enqueue Replication Service (ERS) instance.<br>
Mandatory for NetWeaver ASCS/ERS and SCS/ERS cluster setup.<br>

### sap_ha_pacemaker_cluster_vip_nwas_ers_resource_group_name
- _Type:_ `string`<br>
- _Default:_ `grp_<SID>_ERS<ERS-instance-number>`<br>

Name of the NetWeaver ERS resource group.<br>

### sap_ha_pacemaker_cluster_vip_nwas_ers_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_vip_<SID>_ERS<ERS-instance-number>`<br>

Name of the Virtual IP resource for NetWeaver Enqueue Replication Service (ERS).<br>

### sap_ha_pacemaker_cluster_vip_nwas_scs_ip_address
- _Type:_ `string`<br>

Virtual IP of the NetWeaver Central Services (SCS) instance.<br>
Mandatory for NetWeaver SCS/ERS cluster setup.<br>

### sap_ha_pacemaker_cluster_vip_nwas_scs_resource_group_name
- _Type:_ `string`<br>
- _Default:_ `grp_<SID>_SCS<SCS-instance-number>`<br>

Name of the NetWeaver SCS resource group.<br>

### sap_ha_pacemaker_cluster_vip_nwas_scs_resource_name
- _Type:_ `string`<br>
- _Default:_ `rsc_vip_<SID>_SCS<SCS-instance-number>`<br>

Name of the Virtual IP resource for NetWeaver Central Services (SCS).<br>

<!-- END Role Variables -->
