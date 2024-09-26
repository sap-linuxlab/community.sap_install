## Input Parameters for sap_ha_pacemaker_cluster Ansible Role
<!-- BEGIN Role Input Parameters -->

### sap_ha_install_hana_hsr_sid

- _Type:_ `string`
- _Default:_ `{{ sap_hana_sid }}`

Enter SID of SAP HANA database.

### sap_ha_install_hana_hsr_instance_number

- _Type:_ `string`
- _Default:_ `{{ sap_hana_instance_number }}`

Enter string value of SAP HANA SID.

### sap_ha_install_hana_hsr_cluster_nodes

- _Type:_ `list`
- _Default:_ `{{ sap_hana_cluster_nodes }}`

List of cluster nodes and associated attributes to describe the target SAP HA environment.<br>
This is required for the HANA System Replication configuration.<br>

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
sap_ha_install_hana_hsr_cluster_nodes:
  - node_name: node1
    node_ip: 192.168.1.11
    node_role: primary
    hana_site: DC01

  - node_name: node2
    node_ip: 192.168.1.12
    node_role: secondary
    hana_site: DC02
```

### sap_ha_install_hana_hsr_hdbuserstore_system_backup_user

- _Type:_ `string`
- _Default:_ `HDB_SYSTEMDB`

Enter name of SYSTEM user for backup execution.

### sap_ha_install_hana_hsr_db_system_password

- _Type:_ `string`
- _Default:_ `{{ sap_hana_install_master_password }}`

Enter password of SYSTEM user for backup execution.

### sap_ha_install_hana_hsr_fqdn

- _Type:_ `string`
- _Default:_ {{ sap_domain }}

Enter domain of SAP system, for example `example.com`.

### sap_ha_install_hana_hsr_rep_mode

- _Type:_ `string`
- _Default:_ `sync`

Enter SAP HANA System Replication mode.

### sap_ha_install_hana_hsr_oper_mode

- _Type:_ `string`
- _Default:_ `logreplay`

Enter SAP HANA System Replication operation mode.

### sap_ha_install_hana_hsr_update_etchosts
- _Type:_ `bool`
- _Default:_ `True`

Enable to update /etc/hosts file.
<!-- END Role Input Parameters -->