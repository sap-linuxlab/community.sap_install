`EXPERIMENTAL`
<!-- BEGIN Title -->
# sap_ha_install_anydb_ibmdb2 Ansible Role
<!-- END Title -->

## Description
<!-- BEGIN Description -->
The Ansible Role for instantiation of IBM Db2 'Integrated Linux Pacemaker' HADR cluster.

**NOTE:** IBM Db2 with 'Integrated Linux Pacemaker' can use two deployment models:

- Mutual Failover option, **not** covered by this Ansible Role
- High Availability and Disaster Recovery (HADR) option for Idle Standby, initialized by this Ansible Role
<!-- END Description -->

<!-- BEGIN Dependencies -->
<!-- END Dependencies -->

<!-- BEGIN Prerequisites -->
## Prerequisites

Managed nodes:

- Directory with installation media is present and `sap_ha_install_anydb_ibmdb2_software_directory` updated. Download can be completed using [community.sap_launchpad](https://github.com/sap-linuxlab/community.sap_launchpad) Ansible Collection.

Software compatibility:

- This Ansible Role is applicable to IBM Db2 11.5 certified for SAP.
- It is applicable to 11.5.9 and later, which provides `db2cm` binary compatibility for AWS, GCP and MS Azure.
<!-- END Prerequisites -->

## Execution
<!-- BEGIN Execution -->
### Supported Platforms
| Platform | Status | Notes |
| -------- | --------- | --------- |
| AWS EC2 Virtual Servers | :heavy_check_mark: | |
| Google Cloud Compute Engine Virtual Machine | :heavy_check_mark: | |
| Microsoft Azure Virtual Machines | :heavy_check_mark: | |
| IBM Cloud Virtual Server | :heavy_check_mark: | |
<!-- END Execution -->

<!-- BEGIN Execution Recommended -->
<!-- END Execution Recommended -->

### Execution Flow
<!-- BEGIN Execution Flow -->
1. Assert that required inputs were provided.
2. Detect target infrastructure platform.
3. Execute platform specific configuration.
4. Instantiate IBM Db2 'Integrated Linux Pacemaker' HADR cluster.
<!-- END Execution Flow -->

### Example
<!-- BEGIN Execution Example -->
```yaml
---
- name: Ansible Play for IBM Db2 Database installation
  hosts: db2_host
  become: true
  tasks:
    - name: Execute Ansible Role sap_ha_install_anydb_ibmdb2
      ansible.builtin.include_role:
        name: community.sap_install.sap_ha_install_anydb_ibmdb2
      vars:
        sap_ha_install_anydb_ibmdb2_sid: SD1 # Sandbox Database for D01 SAP System
        sap_ha_install_anydb_ibmdb2_hostname_primary: db2-p
        sap_ha_install_anydb_ibmdb2_hostname_secondary: db2-s
        sap_ha_install_anydb_ibmdb2_software_directory: /software/ibmdb2_extracted
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
- [Sean Freeman](https://github.com/sean-freeman)
<!-- END Maintainers -->

## Role Variables
<!-- BEGIN Role Variables -->
### sap_ha_install_anydb_ibmdb2_hostname_primary

- _Type:_ `string`

Enter IBM Db2 Primary node hostname


### sap_ha_install_anydb_ibmdb2_hostname_secondary

- _Type:_ `string`

Enter IBM Db2 Secondary node hostname

### sap_ha_install_anydb_ibmdb2_sid

- _Type:_ `string`

Enter IBM Db2 System ID

### sap_ha_install_anydb_ibmdb2_software_directory

- _Type:_ `string`

Enter IBM Db2 installation media path
<!-- END Role Variables -->