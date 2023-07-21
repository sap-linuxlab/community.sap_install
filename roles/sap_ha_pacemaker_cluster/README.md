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
    - RHEL System Roles for SAP RPM Package `rhel-system-roles-3.6.0` or later
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

Minimum required parameters:

- [ha_cluster_hacluster_password](#ha_cluster_hacluster_password)
- [sap_hana_instance_number](#sap_hana_instance_number)


### ha_cluster

- _Type:_ `dict`

Optional _**host_vars**_ parameter - if defined it must be set for each node.<br>
Dictionary that can contain various node options for the pacemaker cluster configuration.<br>
Supported options can be reviewed in the `ha_cluster` Linux System Role [https://github.com/linux-system-roles/ha_cluster/blob/master/README.md].<br>

Example:

```yaml
ha_cluster:
  corosync_addresses:
  - 192.168.1.10
  - 192.168.2.10
  node_name: nodeA
```

### ha_cluster_cluster_name

- _Type:_ `str`
- _Default:_ `my-cluster`

The name of the pacemaker cluster.<br>

### ha_cluster_hacluster_password <sup>required</sup>

- _Type:_ `str`

The password of the `hacluster` user which is created during pacemaker installation.<br>

### sap_ha_pacemaker_cluster_aws_access_key_id

- _Type:_ `str`

AWS access key to allow control of instances (for example for fencing operations).<br>
Required for cluster nodes setup on Amazon cloud.<br>

### sap_ha_pacemaker_cluster_aws_region

- _Type:_ `str`

The AWS region in which the instances to be used for the cluster setup are located.<br>
Required for cluster nodes setup on Amazon cloud.<br>

### sap_ha_pacemaker_cluster_aws_secret_access_key

- _Type:_ `str`

AWS secret key, paired with the access key for instance control.<br>
Required for cluster nodes setup on Amazon cloud.<br>

### sap_ha_pacemaker_cluster_cluster_properties

- _Type:_ `dict`
- _Default:_ `See example`

Standard pacemaker cluster properties are configured with recommended settings for cluster node fencing.<br>

Example:

```yaml
sap_ha_pacemaker_cluster_cluster_properties:
  concurrent-fencing: true
  stonith-enabled: true
  stonith-timeout: 900
```

### sap_ha_pacemaker_cluster_create_config_dest

- _Type:_ `str`
- _Default:_ `<cluster-name>_resource_config.yml`

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

### sap_ha_pacemaker_cluster_fence_options

- _Type:_ `dict`

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

### sap_ha_pacemaker_cluster_hana_prefer_site_takeover

- _Type:_ `bool`
- _Default:_ `True`

Parameter for the 'SAPHana' cluster resource.<br>
Set to "false" if the cluster should first attempt to restart the instance on the same node.<br>
When set to "true" (default) a failover to secondary will be initiated on resource failure.<br>

### sap_ha_pacemaker_cluster_hana_resource_name

- _Type:_ `str`
- _Default:_ `SAPHana_<SID>_<Instance Number>`

Customize the cluster resource name of the SAP HANA DB resource.<br>

### sap_ha_pacemaker_cluster_hana_topology_resource_name

- _Type:_ `str`
- _Default:_ `SAPHanaTopology_<SID>_<Instance Number>`

Customize the cluster resource name of the SAP HANA Topology resource.<br>

### sap_ha_pacemaker_cluster_ibmcloud_api_key

- _Type:_ `str`

The API key is required to allow control of instances (for example for fencing operations).<br>
Required for cluster nodes setup in IBM Cloud.<br>

### sap_ha_pacemaker_cluster_ibmcloud_region

- _Type:_ `str`

The cloud region key in which the instances are running.<br>
Required for cluster nodes setup in IBM Cloud.<br>

### sap_ha_pacemaker_cluster_replication_type

- _Type:_ `str`
- _Default:_ `none`

The type of SAP HANA site replication across multiple hosts.<br>
_Not yet supported_<br>

### sap_ha_pacemaker_cluster_resource_defaults

- _Type:_ `dict`
- _Default:_ `See example`

Set default parameters that will be valid for all pacemaker resources.<br>

Example:

```yaml
sap_ha_pacemaker_cluster_resource_defaults:
  migration-threshold: 5000
  resource-stickiness: 1000
```

### sap_ha_pacemaker_cluster_vip_client_interface

- _Type:_ `str`
- _Default:_ `eth0`

OS device name of the network interface to use for the Virtual IP configuration.<br>
This is used for VIP agents that require an interface name, for example in cloud platform environments.<br>

### sap_ha_pacemaker_cluster_vip_resource_name

- _Type:_ `str`
- _Default:_ `vip_<SID>_<Instance Number>`

Customize the name of the resource managing the Virtual IP.<br>

### sap_ha_pacemaker_cluster_vip_update_rt

- _Type:_ `list`

List one more routing table IDs for managing Virtual IP failover through routing table changes.<br>
Required for VIP configuration in AWS EC2 environments.<br>

### sap_hana_cluster_nodes

- _Type:_ `list`

List of cluster nodes and associated attributes to describe the target SAP HA environment.<br>
This is required for the HANA System Replication configuration.<br>

- **hana_site**<br>
    Site of the cluster and/or SAP HANA System Replication node (for example 'DC01').<br>This is required for HANA System Replication configuration.
- **node_ip**<br>
    IP address of the node used for HANA System Replication.
- **node_name**<br>
    Name of the cluster node, should match the remote systems' hostnames.<br>This is needed by the cluster members to know all their partner nodes.
- **node_role**<br>
    Role of this node in the SAP cluster setup.<br>There must be only **one** primary, but there can be multiple secondary nodes.

Example:

```yaml
sap_hana_cluster_nodes:
- hana_site: DC01
  node_ip: 192.168.5.1
  node_name: nodeA
  node_role: primary
- hana_site: DC02
  node_ip: 192.168.5.2
  node_name: nodeB
  node_role: secondary
```

### sap_hana_instance_number <sup>required</sup>

- _Type:_ `str`

The instance number of the SAP HANA database which is role will configure in the cluster.<br>

### sap_hana_sid

- _Type:_ `str`

The SAP HANA SID of the instance that will be configured in the cluster.<br>
The SID must follow SAP specifications - see SAP Note 1979280.<br>

### sap_hana_vip

- _Type:_ `dict`

One floating IP is required for SAP HANA DB connection by clients.<br>
This main VIP will always run on the promoted HANA node and be moved with it during a failover.<br>

Example:

```yaml
sap_hana_vip:
  primary: 192.168.10.100
```

<!-- END: Role Input Parameters -->
