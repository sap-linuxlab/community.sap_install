<!-- BEGIN: Role Introduction -->
# sap_ha_pacemaker_cluster Ansible Role

![Ansible Lint for sap_ha_pacemaker_cluster](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_ha_pacemaker_cluster.yml/badge.svg)

Ansible Role for installation and configuration of Linux Pacemaker for High Availability of SAP Systems run on various Infrastructure Platforms.

## Scope

This Ansible Role provides:
- installation of Linux Pacemaker packages and dependencies
- configuration of Linux Pacemaker cluster with all relevant fencing agent and resource agent for an Infrastructure Platform and SAP Software (SAP HANA or SAP NetWeaver)
- setup and instantiation of Linux Pacemaker cluster (using `ha_cluster` Linux System Role)

This Ansible Role has been tested for the following SAP Software Solution scenario deployments:
- SAP HANA Scale-up High Availability
- `Beta:` SAP NetWeaver (ABAP) AS ASCS and ERS High Availability
- `Experimental:` SAP NetWeaver (ABAP) AS PAS and AAS High Availability
- `Experimental:` SAP NetWeaver (JAVA) AS SCS and ERS High Availability

This Ansible Role contains Infrastructure Platform specific alterations for:
- AWS EC2 Virtual Servers
- `Beta:` Microsoft Azure Virtual Machines
- `Experimental:` Google Cloud Compute Engine Virtual Machine
- `Experimental:` IBM Cloud Virtual Server
- `Experimental:` IBM Power Virtual Server from IBM Cloud
- `Experimental:` IBM PowerVC hypervisor Virtual Machine

Please note, this Ansible Role `sap_ha_pacemaker_cluster` is acting as a wrapper and generates the parameter definitions for a given SAP System, Infrastructure Platform specific variables and other additional steps to complete the SAP High Availability setup using Linux Pacemaker clusters.

### Warnings :warning:

- :warning: Do **not** execute this Ansible Role against already configured Linux Pacemaker cluster nodes; unless you know what you are doing and have prepared the input variables for the Ansible Role according to / matching to the existing Linux Pacemaker setup!
- :warning: Infrastructure Platforms not explicitly listed as available/tested are very unlikely to work.

## Functionality

_All of the following functionality is provided as **Technology Preview**._

### SAP HANA scale-up (performance-optimized) with SAP HANA System Replication, High Availability using Linux Pacemaker 2-node cluster

| Platform | Usability |
| -------- | --------- |
| :heavy_check_mark: physical server | expected to work with any fencing method that is supported by the `ha_cluster` Linux System Role |
| :heavy_check_mark: OVirt VM | tested and working |
| :heavy_check_mark: AWS EC2 VS | platform detection and awscli setup included, tested and expected to work |

### SAP NetWeaver (ABAP) ASCS and ERS, High Availability using Linux Pacemaker 2-node cluster

| Platform | Usability |
| -------- | --------- |
| :heavy_check_mark: physical server | expected to work with any fencing method that is supported by the `ha_cluster` Linux System Role |
| :heavy_check_mark: OVirt VM | tested and working |
| :heavy_check_mark: AWS EC2 VS | platform detection and awscli setup included, tested and expected to work |

## Requirements

The Ansible Role requires the SAP HANA Database Server or SAP NetWeaver Application Server software installation to already exist on the target host/s.

The target host must have:
- OS version and license - RHEL4SAP (HA and US) 8.4+
- OS package repositories enabled - SAP and High Availability

> _N.B. At this time SLES4SAP functionality is not available, until `crmsh` commands are provided in dependency Ansible Role [`ha_cluster`](https://github.com/linux-system-roles/ha_cluster)_

The Ansible Control System (where Ansible is executed from) must have:
- Ansible Core 2.9+
- Access to dependency Ansible Collections and Ansible Roles:
  - **Upstream**:
    - Ansible Collection [`community.sap_install` from Ansible Galaxy](https://galaxy.ansible.com/community/sap_install) version `1.3.0` or later
    - Ansible Collection [`fedora.linux_system_roles` from Ansible Galaxy](https://galaxy.ansible.com/fedora/linux_system_roles) version `1.20.0` or later
  - **Supported (Downstream)** via Red Hat Ansible Automation Platform (AAP) license:
    - Ansible Collection [`redhat.sap_install` from Red Hat Ansible Automation Platform Hub](https://console.redhat.com/ansible/automation-hub/repo/published/redhat/sap_install) version `1.3.0` or later
    - Ansible Collection [`redhat.rhel_system_roles` from Red Hat Ansible Automation Platform Hub](https://console.redhat.com/ansible/automation-hub/repo/published/redhat/rhel_system_roles) version `1.20.0` or later
  - **Supported (Downstream)** via RHEL4SAP license:
    - RHEL System Roles for SAP RPM Package `rhel-system-roles-sap-3.6.0` or later
    - RHEL System Roles RPM Package `rhel-system-roles-1.20.0` or later

## Prerequisites

All SAP Software must be installed, and all remote/file storage mounts must be available with correct permissions defined by SAP documentation. For SAP HANA High Availability, SAP HANA System Replication must already be installed.

In addition, the following network ports must be available:

| **SAP Technical Application and Component** | **Port** |
| --- | --- |
| **_SAP HANA Sytem Replication_** | |
| hdbnameserver<br/><sub> used for log and data shipping from a primary site to a secondary site.<br/>System DB port number plus 10,000</sub> | 4`<sap_hana_instance_no>`01 |
| hdbnameserver<br/><sub> unencrypted metadata communication between sites.<br/>System DB port number plus 10,000</sub> | 4`<sap_hana_instance_no>`02 |
| hdbnameserver<br/><sub> used for encrypted metadata communication between sites.<br/>System DB port number plus 10,000</sub> | 4`<sap_hana_instance_no>`06 |
| hdbindexserver<br/><sub> used for first MDC Tenant database schema</sub> | 4`<sap_hana_instance_no>`03 |
| hdbxsengine<br/><sub> used for SAP HANA XSC/XSA</sub> | 4`<sap_hana_instance_no>`07|
| hdbscriptserver<br/><sub> used for log and data shipping from a primary site to a secondary site.<br/>Tenant port number plus 10,000</sub> | 4`<sap_hana_instance_no>`40-97 |
| hdbxsengine<br/><sub> used for log and data shipping from a primary site to a secondary site.<br/>Tenant port number plus 10,000</sub> | 4`<sap_hana_instance_no>`40-97 |
| **_Linux Pacemaker_** | |
| pcsd<br/><sub> cluster nodes requirement for node-to-node communication</sub> | 2224 (TCP)|
| pacemaker<br/><sub> cluster nodes requirement for Pacemaker Remote service daemon</sub> | 3121 (TCP) |
| corosync<br/><sub> cluster nodes requirement for node-to-node communcation</sub> | 5404-5412 (UDP) |

## Execution Flow

The Ansible Role is sequential:
- Validate input Ansible Variables
- Identify host's Infrastructure Platform
- Generate Linux Pacemaker definition for given Infrastructure Platform and SAP Software
- Execute `ha_cluster` Ansible Role with Linux Pacemaker definition
- Instantiate Linux Pacemaker cluster

## Tips

Check out the [role variables of the `ha_cluster` Linux System Role](https://github.com/linux-system-roles/ha_cluster/blob/main/README.md) for additional possible settings that can be applied when using the `sap_ha_pacemaker_cluster` role.

For example:<br>
Adding `ha_cluster_start_on_boot: false` to disable the automatic start of cluster services on boot.

## Sample

Please see a full sample using multiple hosts to create an SAP S/4HANA Distributed deployment in the [/playbooks](../../playbooks/) directory of the Ansible Collection `sap_install`.

## License

Apache 2.0

## Author Information

Red Hat for SAP Community of Practice, Janine Fuchs, IBM Lab for SAP Solutions

<!-- END: Role Introduction -->

---
<!-- BEGIN: Role Input Parameters -->
## Role Input Parameters

Minimum required parameters for all clusters:

- [sap_ha_pacemaker_cluster_hacluster_user_password](#sap_ha_pacemaker_cluster_hacluster_user_password)

Additional minimum requirements depend on the type of cluster setup and on the target platform.

### sap_ha_pacemaker_cluster_aws_access_key_id

- _Type:_ `string`

AWS access key to allow control of instances (for example for fencing operations).<br>
Mandatory for the cluster nodes setup on AWS EC2 instances.<br>

### sap_ha_pacemaker_cluster_aws_region

- _Type:_ `string`

The AWS region in which the instances to be used for the cluster setup are located.<br>
Mandatory for cluster nodes setup on AWS EC2 instances.<br>

### sap_ha_pacemaker_cluster_aws_secret_access_key

- _Type:_ `string`

AWS secret key, paired with the access key for instance control.<br>
Mandatory for the cluster setup on AWS EC2 instances.<br>

### sap_ha_pacemaker_cluster_aws_vip_update_rt

- _Type:_ `string`

List one more routing table IDs for managing Virtual IP failover through routing table changes.<br>
Multiple routing tables must be defined as a comma-separated string (no spaces).<br>
Mandatory for the VIP resource configuration in AWS EC2 environments.<br>

### sap_ha_pacemaker_cluster_cluster_name

- _Type:_ `string`

The name of the pacemaker cluster.<br>
Inherits the `ha_cluster` LSR native parameter `ha_cluster_cluster_name` if not defined.<br>
If not defined, the `ha_cluster` Linux System Role default will be used.<br>

### sap_ha_pacemaker_cluster_cluster_nodes

- _Type:_ `list`

List of cluster nodes and associated attributes to describe the target SAP HA environment.<br>
This is required for the HANA System Replication configuration.<br>
Synonym for this parameter is `sap_hana_cluster_nodes`.<br>
Mandatory to be defined for HANA clusters.<br>

- **hana_site**<br>
    Site of the cluster and/or SAP HANA System Replication node (for example 'DC01').<br>Mandatory for HANA clusters (sudo config for system replication).
- **node_ip**<br>
    IP address of the node used for HANA System Replication.<br>_Optional. Currently not needed/used in cluster configuration._
- **node_name**<br>
    Name of the cluster node, should match the remote systems' hostnames.<br>_Optional. Currently not needed/used in cluster configuration._
- **node_role**<br>
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

- _Type:_ `dict`
- _Default:_ `{'concurrent-fencing': True, 'stonith-enabled': True, 'stonith-timeout': 900}`

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

- _Type:_ `string`
- _Default:_ `review_resource_config.yml`

The pacemaker cluster resource configuration optionally created by this role will be saved in a Yaml file in the current working directory.<br>
Requires `sap_ha_pacemaker_cluster_create_config_varfile` to be enabled for generating the output file.<br>
Specify a path/filename to save the file in a custom location.<br>
The file can be used as input vars file for an Ansible playbook running the 'ha_cluster' Linux System Role.<br>

### sap_ha_pacemaker_cluster_create_config_varfile

- _Type:_ `bool`
- _Default:_ `False`

When enabled, all cluster configuration parameters this role constructs for executing the 'ha_cluster' Linux System role will be written into a file in Yaml format.<br>
This allows using the output file later as input file for additional custom steps using the 'ha_cluster' role and covering the resource configuration in a cluster that was set up using this 'sap_ha_pacemaker_cluster' role.<br>
When enabled this parameters file is also created when the playbook is run in check_mode (`--check`) and can be used to review the configuration parameters without executing actual changes on the target nodes.<br>
WARNING! This report may include sensitive details like secrets required for certain cluster resources!<br>

### sap_ha_pacemaker_cluster_enable_cluster_connector

- _Type:_ `bool`
- _Default:_ `True`

Enables/Disables the SAP HA Interface for SAP ABAP application server instances, also known as `sap_cluster_connector`.<br>
Set this parameter to 'false' if the SAP HA interface should not be installed and configured.<br>

### sap_ha_pacemaker_cluster_extra_packages

- _Type:_ `list`

Additional extra packages to be installed, for instance specific resource packages.<br>
For SAP clusters configured by this role, the relevant standard packages for the target scenario are automatically included.<br>

### sap_ha_pacemaker_cluster_fence_agent_minimal_packages

- _Type:_ `list`
- _Default:_ `['fence-agents-all']`

The minimal set of fence agent packages that will be installed.<br>

### sap_ha_pacemaker_cluster_fence_agent_packages

- _Type:_ `list`

Additional fence agent packages to be installed.<br>
This is automatically combined with `sap_ha_pacemaker_cluster_fence_agent_minimal_packages`.<br>

### sap_ha_pacemaker_cluster_fence_options

- _Type:_ `dict`
- _Default:_ `{'pcmk_reboot_retries': 4, 'pcmk_reboot_timeout': 400, 'power_timeout': 240}`

STONITH resource common parameters that apply to most fencing agents.<br>
These options are applied to fencing resources this role uses automatically for pre-defined platforms (like AWS EC2 VS, IBM Cloud VS).<br>
The listed options are set by default.<br>
Additional options can be added by defining this parameter in dictionary format and adding the defaults plus any valid stonith resource key-value pair.<br>

Example:

```yaml
sap_ha_pacemaker_cluster_fence_options:
  pcmk_reboot_retries: 4
  pcmk_reboot_timeout: 400
  power_timeout: 240
```

### sap_ha_pacemaker_cluster_gcp_project

- _Type:_ `string`

Google Cloud project name in which the target instances are installed.<br>
Mandatory for the cluster setup on GCP instances.<br>

### sap_ha_pacemaker_cluster_gcp_region_zone

- _Type:_ `string`

Google Cloud Platform region zone ID.<br>
Mandatory for the cluster setup on GCP instances.<br>

### sap_ha_pacemaker_cluster_ha_cluster

- _Type:_ `dict`

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

- _Type:_ `string`

The password of the `hacluster` user which is created during pacemaker installation.<br>
Inherits the value of `ha_cluster_hacluster_password`, when defined.<br>

### sap_ha_pacemaker_cluster_hana_automated_register

- _Type:_ `bool`
- _Default:_ `True`

Parameter for the 'SAPHana' cluster resource.<br>
Define if a former primary should be re-registered automatically as secondary.<br>

### sap_ha_pacemaker_cluster_hana_duplicate_primary_timeout

- _Type:_ `int`
- _Default:_ `900`

Parameter for the 'SAPHana' cluster resource.<br>
Time difference needed between to primary time stamps, if a dual-primary situation occurs.<br>
If the time difference is less than the time gap, then the cluster holds one or both instances in a "WAITING" status.<br>
This is to give an admin a chance to react on a failover. A failed former primary will be registered after the time difference is passed.<br>

### sap_ha_pacemaker_cluster_hana_instance_nr

- _Type:_ `string`

The instance number of the SAP HANA database which this role will configure in the cluster.<br>
Inherits the value of `sap_hana_instance_number`, when defined.<br>
Mandatory for SAP HANA cluster setups.<br>

### sap_ha_pacemaker_cluster_hana_prefer_site_takeover

- _Type:_ `bool`
- _Default:_ `True`

Parameter for the 'SAPHana' cluster resource.<br>
Set to "false" if the cluster should first attempt to restart the instance on the same node.<br>
When set to "true" (default) a failover to secondary will be initiated on resource failure.<br>

### sap_ha_pacemaker_cluster_hana_resource_clone_name

- _Type:_ `string`
- _Default:_ `SAPHana_<SID>_<Instance Number>-clone`

Customize the cluster resource name of the SAP HANA DB resource clone.<br>

### sap_ha_pacemaker_cluster_hana_resource_name

- _Type:_ `string`
- _Default:_ `SAPHana_<SID>_<Instance Number>`

Customize the cluster resource name of the SAP HANA DB resource.<br>

### sap_ha_pacemaker_cluster_hana_sid

- _Type:_ `string`

The SAP HANA SID of the instance that will be configured in the cluster.<br>
The SID must follow SAP specifications - see SAP Note 1979280.<br>
Inherits the value of `sap_hana_sid`, when defined.<br>
Mandatory for SAP HANA cluster setups.<br>

### sap_ha_pacemaker_cluster_hana_topology_resource_clone_name

- _Type:_ `string`
- _Default:_ `SAPHanaTopology_<SID>_<Instance Number>-clone`

Customize the cluster resource name of the SAP HANA Topology resource clone.<br>

### sap_ha_pacemaker_cluster_hana_topology_resource_name

- _Type:_ `string`
- _Default:_ `SAPHanaTopology_<SID>_<Instance Number>`

Customize the cluster resource name of the SAP HANA Topology resource.<br>

### sap_ha_pacemaker_cluster_host_type

- _Type:_ `list`
- _Default:_ `hana_scaleup_perf`

The SAP landscape to for which the cluster is to be configured.<br>
The default is a 2-node SAP HANA scale-up cluster.<br>

### sap_ha_pacemaker_cluster_ibmcloud_api_key

- _Type:_ `string`

The API key which is required to allow the control of instances (for example for fencing operations).<br>
Mandatory for the cluster setup on IBM Cloud Virtual Server instances or IBM Power Virtual Server on IBM Cloud.<br>

### sap_ha_pacemaker_cluster_ibmcloud_powervs_api_type

- _Type:_ `string`

IBM Power Virtual Server API Endpoint type (public or private) dependent on network interface attachments for the target instances.<br>
['Mandatory for the cluster setup on IBM Power Virtual Server from IBM Cloud.']<br>

### sap_ha_pacemaker_cluster_ibmcloud_powervs_forward_proxy_url

- _Type:_ `string`

IBM Power Virtual Server forward proxy url when IBM Power Virtual Server API Endpoint type is set to private.<br>
When public network interface, can be ignored.<br>
When private network interface, mandatory for the cluster setup on IBM Power Virtual Server from IBM Cloud.<br>

### sap_ha_pacemaker_cluster_ibmcloud_powervs_workspace_crn

- _Type:_ `string`

IBM Power Virtual Server Workspace service cloud resource name (CRN) identifier which contains the target instances<br>
Mandatory for the cluster setup on IBM Power Virtual Server from IBM Cloud.<br>

### sap_ha_pacemaker_cluster_ibmcloud_region

- _Type:_ `string`

The IBM Cloud VS region name in which the instances are running.<br>
Mandatory for the cluster setup on IBM Cloud Virtual Server instances or IBM Power Virtual Server on IBM Cloud.<br>

### sap_ha_pacemaker_cluster_msazure_resource_group

- _Type:_ `string`

Resource group name/ID in which the target instances are defined.<br>
Mandatory for the cluster setup on MS Azure instances.<br>

### sap_ha_pacemaker_cluster_msazure_subscription_id

- _Type:_ `string`

Subscription ID of the MS Azure environment containing the target instances.<br>
Mandatory for the cluster setup on MS Azure instances.<br>

### sap_ha_pacemaker_cluster_nwas_abap_aas_instance_nr

- _Type:_ `string`

Instance number of the NetWeaver ABAP AAS instance.<br>
Mandatory for NetWeaver AAS cluster configuration.<br>

### sap_ha_pacemaker_cluster_nwas_abap_ascs_ers_ensa1

- _Type:_ `bool`
- _Default:_ `False`

The standard NetWeaver ASCS/ERS cluster will be set up as ENSA2.<br>
Set this parameter to 'true' to configure it as ENSA1.<br>

### sap_ha_pacemaker_cluster_nwas_abap_ascs_filesystem_resource_name

- _Type:_ `string`
- _Default:_ `Filesystem_NWAS_ABAP_ASCS_<SID>_<ASCS-instance-number>`

Name of the filesystem resource for the ASCS instance.<br>

### sap_ha_pacemaker_cluster_nwas_abap_ascs_group_stickiness

- _Type:_ `string`
- _Default:_ `3000`

NetWeaver ASCS resource group stickiness to prefer the ASCS group to stay on the node it was started on.<br>

### sap_ha_pacemaker_cluster_nwas_abap_ascs_instance_nr

- _Type:_ `string`

Instance number of the NetWeaver ABAP ASCS instance.<br>
Mandatory for NetWeaver ASCS/ERS cluster configuration.<br>

### sap_ha_pacemaker_cluster_nwas_abap_ascs_sapinstance_automatic_recover_bool

- _Type:_ `bool`
- _Default:_ `False`

NetWeaver ASCS instance resource option "AUTOMATIC_RECOVER".<br>

### sap_ha_pacemaker_cluster_nwas_abap_ascs_sapinstance_ensa1_failure_timeout

- _Type:_ `string`
- _Default:_ `60`

NetWeaver ASCS instance failure-timeout attribute.<br>
Only used for ENSA1 setups (see `sap_ha_pacemaker_cluster_nwas_abap_ascs_ers_ensa1`). Default setup is ENSA2.<br>

### sap_ha_pacemaker_cluster_nwas_abap_ascs_sapinstance_ensa1_migration_threshold

- _Type:_ `string`
- _Default:_ `1`

NetWeaver ASCS instance migration-threshold setting attribute.<br>
Only used for ENSA1 setups (see `sap_ha_pacemaker_cluster_nwas_abap_ascs_ers_ensa1`). Default setup is ENSA2.<br>

### sap_ha_pacemaker_cluster_nwas_abap_ascs_sapinstance_instance_name

- _Type:_ `string`

The name of the ASCS instance, typically the profile name.<br>
Mandatory for the NetWeaver ASCS/ERS cluster setup<br>

### sap_ha_pacemaker_cluster_nwas_abap_ascs_sapinstance_resource_name

- _Type:_ `string`
- _Default:_ `SAPInstance_NWAS_ABAP_ASCS_<SID>_<ASCS-instance-number>`

Name of the ASCS instance resource.<br>

### sap_ha_pacemaker_cluster_nwas_abap_ascs_sapinstance_resource_stickiness

- _Type:_ `string`
- _Default:_ `5000`

NetWeaver ASCS instance resource stickiness attribute.<br>

### sap_ha_pacemaker_cluster_nwas_abap_ascs_sapinstance_start_profile_string

- _Type:_ `string`

The full path and name of the ASCS instance profile.<br>
Mandatory for the NetWeaver ASCS/ERS cluster setup.<br>

### sap_ha_pacemaker_cluster_nwas_abap_ers_filesystem_resource_name

- _Type:_ `string`
- _Default:_ `Filesystem_NWAS_ABAP_ERS_<SID>_<ERS-instance-number>`

Name of the filesystem resource for the ERS instance.<br>

### sap_ha_pacemaker_cluster_nwas_abap_ers_instance_nr

- _Type:_ `string`

Instance number of the NetWeaver ABAP ERS instance.<br>
Mandatory for NetWeaver ASCS/ERS cluster configuration.<br>

### sap_ha_pacemaker_cluster_nwas_abap_ers_sapinstance_automatic_recover_bool

- _Type:_ `bool`
- _Default:_ `False`

NetWeaver ERS instance resource option "AUTOMATIC_RECOVER".<br>

### sap_ha_pacemaker_cluster_nwas_abap_ers_sapinstance_instance_name

- _Type:_ `string`

The name of the ERS instance, typically the profile name.<br>
Mandatory for the NetWeaver ASCS/ERS cluster setup.<br>

### sap_ha_pacemaker_cluster_nwas_abap_ers_sapinstance_resource_name

- _Type:_ `string`
- _Default:_ `SAPInstance_NWAS_ABAP_ERS_<SID>_<ERS-instance-number>`

Name of the ERS instance resource.<br>

### sap_ha_pacemaker_cluster_nwas_abap_ers_sapinstance_start_profile_string

- _Type:_ `string`

The full path and name of the ERS instance profile.<br>
Mandatory for the NetWeaver ASCS/ERS cluster.<br>

### sap_ha_pacemaker_cluster_nwas_abap_pas_instance_nr

- _Type:_ `string`

Instance number of the NetWeaver ABAP PAS instance.<br>
Mandatory for NetWeaver PAS cluster configuration.<br>

### sap_ha_pacemaker_cluster_nwas_abap_sid

- _Type:_ `string`

SID of the NetWeaver instances.<br>
Mandatory for NetWeaver cluster configuration.<br>
Uses `sap_swpm_sid` if defined.<br>
Mandatory for NetWeaver cluster setups.<br>

### sap_ha_pacemaker_cluster_nwas_sapmnt_filesystem_resource_name

- _Type:_ `string`
- _Default:_ `Filesystem_NWAS_SAPMNT_<SID>`

Filesystem resource name for the shared filesystem /sapmnt.<br>
Optional, this is typically managed by the OS, but can as well be added to the cluster configuration.<br>
Enable this resource setup using `sap_ha_pacemaker_cluster_nwas_shared_filesystems_cluster_managed`.<br>

### sap_ha_pacemaker_cluster_nwas_shared_filesystems_cluster_managed

- _Type:_ `bool`
- _Default:_ `False`

Change this parameter to 'true' if the 3 shared filesystems `/usr/sap/trans`, `/usr/sap/<SID>/SYS` and '/sapmnt' shall be configured as cloned cluster resources.<br>

### sap_ha_pacemaker_cluster_nwas_sys_filesystem_resource_name

- _Type:_ `string`
- _Default:_ `Filesystem_NWAS_SYS_<SID>`

Filesystem resource name for the transports filesystem /usr/sap/<SID>/SYS.<br>
Optional, this is typically managed by the OS, but can as well be added to the cluster configuration.<br>
Enable this resource setup using `sap_ha_pacemaker_cluster_nwas_shared_filesystems_cluster_managed`.<br>

### sap_ha_pacemaker_cluster_nwas_transports_filesystem_resource_name

- _Type:_ `string`
- _Default:_ `Filesystem_NWAS_TRANS_<SID>`

Filesystem resource name for the transports filesystem /usr/sap/trans.<br>
Optional, this is typically managed by the OS, but can as well be added to the cluster configuration.<br>
Enable this resource setup using `sap_ha_pacemaker_cluster_nwas_shared_filesystems_cluster_managed`.<br>

### sap_ha_pacemaker_cluster_resource_defaults

- _Type:_ `dict`
- _Default:_ `{'migration-threshold': 5000, 'resource-stickiness': 3000}`

Set default parameters that will be valid for all pacemaker resources.<br>

Example:

```yaml
sap_ha_pacemaker_cluster_resource_defaults:
  migration-threshold: 5000
  resource-stickiness: 1000
```

### sap_ha_pacemaker_cluster_stonith_custom

- _Type:_ `list`

Custom list of STONITH resource(s) to be configured in the cluster.<br>
This definition override any defaults the role would apply otherwise.<br>

- **agent**<br>
    Resource agent name, must contain the prefix "stonith:" to avoid mismatches or failures.
- **name**<br>
    Name that will be used as the resource ID (name).
- **options**<br>
    The resource options listed in dictionary format, one option per line.<br>Requires the mandatory options for the particular stonith resource agent to be defined, otherwise the setup will fail.

Example:

```yaml
sap_ha_pacemaker_cluster_stonith_custom:
- agent: stonith:fence_rhevm
  name: my-fence-resource
  options:
    ip: rhevm-server
    password: login-user-password
    pcmk_host_list: node1,node2
    power_wait: 3
    username: login-user
```

### sap_ha_pacemaker_cluster_storage_definition

- _Type:_ `list`

List of filesystem definitions used for filesystem cluster resources.<br>
Options relevant, see example.<br>
Mandatory for SAP NetWeaver HA cluster configurations.<br>
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

### sap_ha_pacemaker_cluster_storage_nfs_filesytem_type

- _Type:_ `string`
- _Default:_ `nfs`

Filesystem type of the NFS filesystems that are part of the cluster configuration.<br>

### sap_ha_pacemaker_cluster_storage_nfs_mount_options

- _Type:_ `string`
- _Default:_ `defaults`

Mount options of the NFS filesystems that are part of the cluster configuration.<br>

### sap_ha_pacemaker_cluster_storage_nfs_server

- _Type:_ `string`

Default address of the NFS server, if not defined individually by filesystem.<br>

### sap_ha_pacemaker_cluster_system_roles_collection

- _Type:_ `string`
- _Default:_ `fedora.linux_system_roles`

Reference to the Ansible Collection used for the Linux System Roles.<br>
For community/upstream, use 'fedora.linux_system_roles'.<br>
For RHEL System Roles for SAP, or Red Hat Automation Hub, use 'redhat.rhel_system_roles'.<br>

### sap_ha_pacemaker_cluster_vip_client_interface

- _Type:_ `string`

OS device name of the network interface to use for the Virtual IP configuration.<br>
When there is only one interface on the system, its name will be used by default.<br>

### sap_ha_pacemaker_cluster_vip_hana_primary_ip_address

- _Type:_ `string`

The virtual IP of the primary HANA instance.<br>
Mandatory parameter for HANA clusters.<br>

### sap_ha_pacemaker_cluster_vip_hana_primary_resource_name

- _Type:_ `string`
- _Default:_ `vip_<SID><Instance Number>`

Customize the name of the resource managing the Virtual IP of the primary HANA instance.<br>

### sap_ha_pacemaker_cluster_vip_hana_secondary_ip_address

- _Type:_ `string`

The virtual IP for read-only access to the secondary HANA instance.<br>
Optional parameter in HANA clusters.<br>

### sap_ha_pacemaker_cluster_vip_nwas_abap_aas_ip_address

- _Type:_ `string`

Virtual IP of the NetWeaver AAS instance.<br>
Mandatory for NetWeaver AAS cluster setup.<br>

### sap_ha_pacemaker_cluster_vip_nwas_abap_aas_resource_name

- _Type:_ `string`
- _Default:_ `vip_<SID>_<AAS-instance-number>_aas`

Name of the SAPInstance resource for NetWeaver AAS.<br>

### sap_ha_pacemaker_cluster_vip_nwas_abap_ascs_ip_address

- _Type:_ `string`

Virtual IP of the NetWeaver ASCS instance.<br>
Mandatory for NetWeaver ASCS/ERS cluster setup.<br>

### sap_ha_pacemaker_cluster_vip_nwas_abap_ascs_resource_name

- _Type:_ `string`
- _Default:_ `vip_<SID>_<ASCS-instance-number>_ascs`

Name of the SAPInstance resource for NetWeaver ASCS.<br>

### sap_ha_pacemaker_cluster_vip_nwas_abap_ers_ip_address

- _Type:_ `string`

Virtual IP of the NetWeaver ERS instance.<br>
Mandatory for NetWeaver ASCS/ERS cluster setup.<br>

### sap_ha_pacemaker_cluster_vip_nwas_abap_ers_resource_name

- _Type:_ `string`
- _Default:_ `vip_<SID>_<ERS-instance-number>_ers`

Name of the SAPInstance resource for NetWeaver ERS.<br>

### sap_ha_pacemaker_cluster_vip_nwas_abap_pas_ip_address

- _Type:_ `string`

Virtual IP of the NetWeaver PAS instance.<br>
Mandatory for NetWeaver PAS cluster setup.<br>

### sap_ha_pacemaker_cluster_vip_nwas_abap_pas_resource_name

- _Type:_ `string`
- _Default:_ `vip_<SID>_<PAS-instance-number>_pas`

Name of the SAPInstance resource for NetWeaver PAS.<br>

### sap_ha_pacemaker_cluster_vip_secondary_resource_name

- _Type:_ `string`
- _Default:_ `vip_<SID><Instance Number>`

Customize the name of the resource managing the Virtual IP of read-only access to the secondary HANA instance.<br>

<!-- END: Role Input Parameters -->
