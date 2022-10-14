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

Required parameters:
- [ha_cluster_hacluster_password](#ha_cluster_hacluster_password)
- [sap_hana_cluster_nodes](#sap_hana_cluster_nodes)
- [sap_hana_instance_number](#sap_hana_instance_number)
- [sap_hana_sid](#sap_hana_sid)
- [sap_hana_vip](#sap_hana_vip)

---

### ha_cluster
- _Type:_ `dict`

Optional _**host_vars**_ parameter, if defined it must be set for each node.<br>
Definition of node name and IP addresses to be used for the pacemaker cluster.<br>
Required for resilient node communication by providing more than one corosync IP.<br>
See https://github.com/linux-system-roles/ha_cluster/blob/master/README.md#nodes-names-and-addresses<br>

  - **corosync_addresses**<br>
        _Default:_ `<primary ip>`<br>
        List of one or more IP addresses to be used for Corosync.<br>All nodes must have the same number of addresses.<br>The order of the listed addresses matters.
  - **node_name**<br>
        _Default:_ `<play host name>`<br>
        The name of the node in the cluster.
  - **pcs_address**<br>
        _Default:_ `<play host primary address>`<br>
        An address used by pcs to communicate with the node.<br>Can be a name, FQDN or IP address and can contain a port.

Example:
```yaml
ha_cluster:
  corosync_addresses:
  - 192.168.1.10
  - 192.168.2.10
  node_name: nodeA
  pcs_address: nodeA
```

### ha_cluster_cluster_name
- _Type:_ `str`
- _Default:_ `my-cluster`

The name of the pacemaker cluster.<br>

### ha_cluster_hacluster_password <sup>required</sup>
- _Type:_ `str`

The password of the `hacluster` user which is created during pacemaker installation.<br>

### sap_ha_cluster_aws_access_key_id
- _Type:_ `str`

AWS access key to allow control of instances (for example for fencing operations).<br>
Required for cluster nodes setup on Amazon cloud.<br>

### sap_ha_cluster_aws_region
- _Type:_ `str`

The AWS region in which the instances to be used for the cluster setup are located.<br>
Required for cluster nodes setup on Amazon cloud.<br>

### sap_ha_cluster_aws_secret_access_key
- _Type:_ `str`

AWS secret key, paired with the access key for instance control.<br>
Required for cluster nodes setup on Amazon cloud.<br>

### sap_ha_cluster_create_config_dest
- _Type:_ `str`
- _Default:_ `sap_ha_cluster_resource_config.yml`

The cluster resource configuration created by this role will be saved in a Yaml file in the current working directory.<br>
Specify a path/filename to save the file elsewhere.<br>

### sap_ha_cluster_create_config_only
- _Type:_ `bool`
- _Default:_ `False`

Enable to only create an output of the parameters and values this role will use as input into the 'ha_cluster' role.<br>
The output is saved in a variables file and used for individual execution of the 'ha_cluster' linux system role.<br>
WARNING! This report may include sensitive details like secrets required for certain cluster resources!<br>

### sap_ha_cluster_fence_power_timeout
- _Type:_ `int`
- _Default:_ `240`

STONITH resource parameter to test X seconds for status change after ON/OFF.<br>

### sap_ha_cluster_fence_reboot_retries
- _Type:_ `int`
- _Default:_ `4`

STONITH resource parameter to define how often it retries to restart a node.<br>

### sap_ha_cluster_fence_reboot_timeout
- _Type:_ `int`
- _Default:_ `400`

STONITH resource parameter to define after which timeout a node restart is returned as failed.<br>

### sap_ha_cluster_hana_automated_register
- _Type:_ `bool`
- _Default:_ `True`

Define if a former primary should be re-registered automatically as secondary.<br>

### sap_ha_cluster_hana_duplicate_primary_timeout
- _Type:_ `int`
- _Default:_ `900`

Time difference needed between to primary time stamps, if a dual-primary situation occurs.<br>
If the time difference is less than the time gap, then the cluster holds one or both instances in a "WAITING" status.<br>
This is to give an admin a chance to react on a failover. A failed former primary will be registered after the time difference is passed.<br>

### sap_ha_cluster_hana_prefer_site_takeover
- _Type:_ `bool`
- _Default:_ `True`

Set to "false" if the cluster should first attempt to restart the instance on the same node.<br>
When set to "true" (default) a failover to secondary will be initiated on resource failure.<br>

### sap_ha_cluster_hana_resource_name
- _Type:_ `str`
- _Default:_ `SAPHana_<SID>_<Instance Number>`

Customize the cluster resource name of the SAP HANA DB resource.<br>

### sap_ha_cluster_hana_topology_resource_name
- _Type:_ `str`
- _Default:_ `SAPHanaTopology_<SID>_<Instance Number>`

Customize the cluster resource name of the SAP HANA Topology resource.<br>

### sap_ha_cluster_replication_type
- _Type:_ `str`
- _Default:_ `none`

The type of SAP HANA site replication across multiple hosts.<br>
_Not yet supported_<br>

### sap_ha_cluster_sap_type
- _Type:_ `str`
- _Default:_ `scaleup`

The SAP landscape to be installed.<br>
_Currently only scale-up is supported_<br>

### sap_ha_cluster_vip_client_interface
- _Type:_ `str`
- _Default:_ `<ansible_default_ipv4.interface>`

OS device name of the network interface to use for the Virtual IP configuration.<br>
This is used for VIP agents that require an interface name, for example in cloud platform environments.<br>

### sap_ha_cluster_vip_resource_name
- _Type:_ `str`
- _Default:_ `vip_<SID>_<Instance Number>`

Customize the name of the resource managing the Virtual IP.<br>

### sap_ha_cluster_vip_update_rt
- _Type:_ `list`

List one more routing table IDs for managing Virtual IP failover through routing table changes.<br>
Required for VIP configuration in AWS EC2 environments.<br>

### sap_hana_cluster_nodes <sup>required</sup>
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
        Role of this node in the SAP cluster setup.<br>There must be only *one* primary, but there can be multiple secondary nodes.

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

### sap_hana_sid <sup>required</sup>
- _Type:_ `str`

The SAP System ID of the instance that will be configured in the cluster.<br>
The SAP SID must follow SAP specifications - see SAP Note 1979280.<br>

### sap_hana_vip <sup>required</sup>
- _Type:_ `dict`

One floating IP is required for SAP HANA DB connection by clients.<br>
This main VIP will always run on the promoted HANA node and be moved with it during a failover.<br>

Example:
```yaml
sap_hana_vip:
  primary: 192.168.10.100
```

<!-- END: Role Input Parameters -->
