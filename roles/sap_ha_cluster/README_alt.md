<!-- BEGIN: Role Input Parameters -->
## Role Input Parameters

### ha_cluster_hacluster_password <sup>required</sup>

- _Alias:_ `sap_hana_hacluster_password`
- _Type:_ `str`

The password of the `hacluster` user which is created during pacemaker installation.<br>

### sap_hana_cluster_nodes <sup>required</sup>

- _Type:_ `list`

List of cluster nodes and associated attributes (in dictionary format).<br>
This is required for the srHook configuration.<br>

```text
hana_site:
    description:
    - Site of the cluster and/or SAP HANA System Replication node (for example 'DC01').
    - Required for HANA System Replication configuration.
    required: true
node_name:
    description:
    - Name of the cluster node, should match the remote system's hostname.
    required: true
node_role:
    choices:
    - primary
    - secondary
    description:
    - Role of this node in the SAP cluster setup.
    required: true
```

### sap_hana_instance_number <sup>required</sup>

- _Alias:_ `sap_ha_cluster_hana_instance_number`
- _Type:_ `str`

The instance number of the SAP HANA database which is role will configure in the cluster.<br>

### sap_hana_sid <sup>required</sup>

- _Alias:_ `sap_ha_cluster_hana_sid`
- _Type:_ `str`

The SAP System ID of the instance that will be configured in the cluster.<br>
The SAP SID must follow SAP specifications - see SAP Note 1979280.<br>

### sap_hana_vip <sup>required</sup>

- _Type:_ `dict`

Virtual floating IP for SAP HANA DB connections.<br>
This IP will always run on the promoted HANA node.<br>

```text
primary:
    aliases:
    - main
    - promoted
    description:
    - At least one Virtual IP is required to always reach the promoted SAP HANA DB.
    required: true
    type: str
secondary:
    aliases:
    - readonly
    - unpromoted
    description:
    - An additional VIP can be used to run on a secondary node for read-only DB access.
    required: false
    type: str
```


### ha_cluster

- _Type:_ `dict`

Optional **host_vars** parameter, if defined it must be set for each node.<br>
Definition of node name and IP addresses to be used for the pacemaker cluster.<br>
Required for resilient node communication by providing more than one corosync IP.<br>
See https://github.com/linux-system-roles/ha_cluster/blob/master/README.md#nodes-names-and-addresses<br>

```text
corosync_addresses:
    default: <primary ip>
    description:
    - List of IP addresses used by Corosync.
    - All nodes must have the same number of addresses.
    - The order of the listed addresses  matters.
    type: list
node_name:
    default: <play host>
    description:
    - The name of the node in the cluster.
    type: str
pcs_address:
    default: <play host>
    description:
    - An address used by pcs to communicate with the node.
    - Can be a name, FQDN or IP address and can contain a port.
    type: str
```

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

- _Alias:_ `sap_ha_cluster_cluster_name`
- _Type:_ `str`
- _Default:_ `my-cluster`

The name of the pacemaker cluster.<br>

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

### sap_ha_cluster_sap_type

- _Type:_ `str`
- _Default:_ `scaleup`

The SAP landscape to be installed.<br>

<!-- END: Role Input Parameters -->
