<!-- BEGIN Title -->
# sap_ha_install_hana_hsr Ansible Role
<!-- END Title -->
![Ansible Lint for sap_ha_install_hana_hsr](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_ha_install_hana_hsr.yml/badge.svg)

## Description
<!-- BEGIN Description -->
Ansible Role `sap_ha_install_hana_hsr` is used to configure and enable SAP HANA System Replication between 2 nodes.
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
Role can be executed independently or as part of [ansible.playbooks_for_sap](https://github.com/sap-linuxlab/ansible.playbooks_for_sap) playbooks.
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
<!-- END Further Information -->

## License
<!-- BEGIN License -->
Apache 2.0
<!-- END License -->

## Maintainers
<!-- BEGIN Maintainers -->
- [Janine Fuchs](https://github.com/ja9fuchs)
<!-- END Maintainers -->

## Role Input Parameters
All input parameters used by role are described in [INPUT_PARAMETERS.md](https://github.com/sap-linuxlab/community.sap_install/blob/main/roles/sap_ha_install_hana_hsr/INPUT_PARAMETERS.md)
