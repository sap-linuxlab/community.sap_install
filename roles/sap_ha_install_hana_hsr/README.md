<!-- BEGIN Title -->
# sap_ha_install_hana_hsr Ansible Role
<!-- END Title -->
![Ansible Lint for sap_ha_install_hana_hsr](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_ha_install_hana_hsr.yml/badge.svg)

## Description
<!-- BEGIN Description -->
The Ansible Role `sap_ha_install_hana_hsr` is used to configure and enable SAP HANA System Replication between 2 nodes.
<!-- END Description -->

<!-- BEGIN Dependencies -->
<!-- END Dependencies -->

<!-- BEGIN Prerequisites -->
## Prerequisites
Managed nodes:
- Same Operating system version
- SAP HANA is installed with same version on both nodes.
<!-- END Prerequisites -->

## Execution
<!-- BEGIN Execution -->
<!-- END Execution -->

<!-- BEGIN Execution Recommended -->
### Recommended
It is recommended to execute this role together with other roles in this collection, in the following order:
1. [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure)
2. [sap_hana_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_preconfigure)
3. [sap_install_media_detect](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_install_media_detect)
4. [sap_hana_install](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_install)
5. *`sap_ha_install_hana_hsr`*
<!-- END Execution Recommended -->

### Execution Flow
<!-- BEGIN Execution Flow -->
1. Assert that required inputs were provided.
2. Verify connection between nodes.
3. Update /etc/hosts, hdbuserstore, Log mode, PKI
4. Execute database backup
5. Configure SAP HANA System Replication
<!-- END Execution Flow -->

### Example
<!-- BEGIN Execution Example -->
```yaml
---
- name: Ansible Play for SAP HANA System Replication setup
  hosts: hana_primary, hana_secondary
  become: true
  tasks:
    - name: Execute Ansible Role sap_ha_install_hana_hsr
      ansible.builtin.include_role:
        name: community.sap_install.sap_ha_install_hana_hsr
      vars:
        sap_ha_install_hana_hsr_cluster_nodes:
          - node_name: h01hana0
            node_ip: "10.10.10.10"
            node_role: primary
            hana_site: DC01

          - node_name: h01hana1
            node_ip: "10.10.10.11"
            node_role: secondary
            hana_site: DC02

        sap_ha_install_hana_hsr_sid: H01
        sap_ha_install_hana_hsr_instance_number: "01"
        sap_ha_install_hana_hsr_hdbuserstore_system_backup_user: "HDB_SYSTEMDB"
        sap_ha_install_hana_hsr_db_system_password: "Password"
        sap_ha_install_hana_hsr_fqdn: example.com
```
<!-- END Execution Example -->

<!-- BEGIN Role Tags -->
<!-- END Role Tags -->

<!-- BEGIN Further Information -->
## Further Information
For more examples on how to use this role in different installation scenarios, refer to the [ansible.playbooks_for_sap](https://github.com/sap-linuxlab/ansible.playbooks_for_sap) playbooks.
<!-- END Further Information -->

## License
<!-- BEGIN License -->
Apache 2.0
<!-- END License -->

## Maintainers
<!-- BEGIN Maintainers -->
- [Janine Fuchs](https://github.com/ja9fuchs)
<!-- END Maintainers -->

## Role Variables
<!-- BEGIN Role Variables -->
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
<!-- END Role Variables -->