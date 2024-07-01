`EXPERIMENTAL`

# sap_ha_install_anydb_ibmdb2 Ansible Role

Ansible Role for instantiation of IBM Db2 'Integrated Linux Pacemaker' HADR cluster

Note: IBM Db2 with 'Integrated Linux Pacemaker' can use two deployment models:
- Mutual Failover option, not covered by this Ansible Role
- High Availability and Disaster Recovery (HADR) option for Idle Standby, initialised by this Ansible Role


## Prerequisites

### Software Installation files

Download IBM Db2 installation media from SAP Download Center on host, and set Ansible Variable `sap_ha_install_anydb_ibmdb2_software_directory` to this path.

### Variables

- `sap_ha_install_anydb_ibmdb2_hostname_primary` with the IBM Db2 Primary node hostname
- `sap_ha_install_anydb_ibmdb2_hostname_secondary` with the IBM Db2 Secondary node hostname
- `sap_ha_install_anydb_ibmdb2_sid` with the IBM Db2 System ID
- `sap_ha_install_anydb_ibmdb2_software_directory` with the IBM Db2 installation media path

These are listed in the default variables file, but commented-out to enforce the required variables:
- [**sap_ha_install_anydb_ibmdb2** default parameters](defaults/main.yml)

## Requirements and Dependencies

This Ansible Role is applicable to IBM Db2 11.5 certified for SAP.

It is applicable to 11.5.9 and later, which provides `db2cm` binary compatibility for AWS, GCP and MS Azure.

### Target host - Infrastructure Platforms

Applicable for:

- Amazon Web Services
- Google Cloud
- Microsoft Azure

### Target host - Operating System requirements

Designed for Linux operating systems, e.g. RHEL (7.x and 8.x) and SLES (15.x).

## Execution

Sample Ansible Playbook Execution:

- Local Host Installation
    - `ansible-playbook --connection=local --limit localhost -i "localhost," sap-ha-anydb-ibmdb2-init.yml -e "@inputs/ibmdb2_vars.yml`

- Target Host Installation
    - `ansible-playbook -i "<target-host>" sap-ha-anydb-ibmdb2-init.yml -e "@inputs/ibmdb2_vars.yml"`

## Sample Ansible Playbook

```yaml
---
- hosts: all

  collections:
    - community.sap_install

  vars:
    sap_ha_install_anydb_ibmdb2_hostname_primary: anydb-primary
    sap_ha_install_anydb_ibmdb2_hostname_secondary: anydb-second
    sap_ha_install_anydb_ibmdb2_sid: DB2
    sap_ha_install_anydb_ibmdb2_software_directory: /software/ibmdb2_extracted

    - name: Execute Ansible Role sap_ha_install_anydb_ibmdb2
      ansible.builtin.include_role:
        name: community.sap_install.sap_ha_install_anydb_ibmdb2
```

## License

Apache license 2.0

## Author Information

Sean Freeman
