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
        sap_ha_install_hana_hsr_db_system_password: "My_HANA_Password"
        sap_ha_install_hana_hsr_domain: example.com
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
- [Marcel Mamula](https://github.com/marcelmamula)
<!-- END Maintainers -->

## Role Variables
<!-- BEGIN Role Variables -->
### sap_ha_install_hana_hsr_state
- _Type:_ `string`
- _Default:_ `present`

Set the desired state of the HSR configuration.</br>
`present` - Creates and enables the HSR configuration.</br>
`absent`  - Removes the HSR configuration.</br>
Removal of existing configuration requires correctly configured `sap_ha_install_hana_hsr_cluster_nodes`.

### sap_ha_install_hana_hsr_sid
- _Type:_ `string`

SAP HANA Database System ID (SID) in capital letters.</br>
This can be inherited from the variable `sap_hana_sid`.

### sap_ha_install_hana_hsr_instance_number
- _Type:_ `string`

SAP HANA Database Instance Number.</br>
This can be inherited from the variable `sap_hana_instance_number`.

### sap_ha_install_hana_hsr_cluster_nodes
- _Type:_ `list` of `dictionary` type

List of dictionaries defining the nodes in the HSR setup.<br>
This can be inherited from the variable `sap_hana_cluster_nodes`.

- **node_name**<br>
    Short hostname of the node (String).<br>
- **node_ip**<br>
    IP address of the node (String).<br>
- **node_role**<br>
    Role of the node in the HSR setup (String).<br>
    Available options: `primary`, `secondary`.<br>
- **hana_site**<br>
    A unique logical site name (e.g., DC01, EU-WEST) (String).<br>

Example:

```yaml
sap_ha_install_hana_hsr_cluster_nodes:
  - node_name: 'node01'
    node_ip: '192.168.1.11'
    node_role: 'primary'
    hana_site: 'DC01'

  - node_name: 'node02'
    node_ip: '192.168.1.12'
    node_role: 'secondary'
    hana_site: 'DC02'
```

### sap_ha_install_hana_hsr_hdbuserstore_system_backup_user
- _Type:_ `string`
- _Default:_ `HDB_SYSTEMDB`

The hdbuserstore key used for connecting to the SYSTEMDB for administrative tasks like backups.

### sap_ha_install_hana_hsr_db_system_password
- _Type:_ `string`

Password for the HANA `SYSTEM` user.</br>
This can be inherited from the variable `sap_hana_install_master_password`.

### sap_ha_install_hana_hsr_domain
- _Type:_ `string`

The DNS domain name for the HANA nodes.</br>
This is not required if 'node_name' in `sap_ha_install_hana_hsr_cluster_nodes` is a Fully Qualified Domain Name (FQDN).</br>
Originally called as `sap_ha_install_hana_hsr_fqdn`.</br>
If not set, the role attempts to use the value of `sap_domain` or `ansible_facts['domain']`.

### sap_ha_install_hana_hsr_rep_mode
- _Type:_ `string`
- _Default:_ `sync`

HSR Replication mode.</br>
Available values: `sync`, `syncmem`, `async`

### sap_ha_install_hana_hsr_oper_mode
- _Type:_ `string`
- _Default:_ `logreplay`

HSR Operation mode.</br>
Available values: `delta_datashipping`, `logreplay`, `logreplay_readaccess`

### sap_ha_install_hana_hsr_update_etchosts
- _Type:_ `bool`
- _Default:_ `True`

Set to true to update `/etc/hosts` on all nodes with the IP addresses and hostnames of all other nodes in the cluster.

### sap_ha_install_hana_hsr_home_path
- _Type:_ `string`

(Optional) SAP HANA HOME directory path</br>
If not set, it defaults to `/usr/sap/<SID>/home`.

### sap_ha_install_hana_hsr_backup_path
- _Type:_ `string`

(Optional) Directory path for the safety backup created before HSR is configured.</br>
If not specified, the default HANA backup location is used.</br>
Required sub-directories (`SYSTEMDB` and `DB_<SID>`) will be created automatically within this path</br>
The backup created will have a file prefix of `<SID>_PRE_HSR_<TIMESTAMP>`.</br>

<!-- END Role Variables -->