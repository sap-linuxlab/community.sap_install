# sap_anydb_install_oracle Ansible Role

Ansible role for Oracle DB 19.x installation for SAP

## Prerequisites

### SAP HANA Software Installation .SAR Files

Download installation media from SAP Download Center on host, and set Ansible Variable `sap_anydb_install_oracle_extract_path` to this path.

### Default Parameters

Please check the default parameters file for more information on other parameters that can be used as an input
- [**sap_anydb_install_oracle** default parameters](defaults/main.yml)

## Execution

Sample Ansible Playbook Execution:

- Local Host Installation
    - `ansible-playbook --connection=local --limit localhost -i "localhost," sap-anydb-oracle-install.yml -e "@inputs/oracledb.install"`

- Target Host Installation
    - `ansible-playbook -i "<target-host>" sap-anydb-oracle-install.yml -e "@inputs/oracledb.install"`

## Sample playbook

### Sample playbook for installing a new scale-up (=single node) SAP HANA system

```yaml
---
- hosts: all
  become: true

  collections:
    - community.sap_install

  vars:
    sap_anydb_install_oracle_method: minimal
    sap_anydb_install_oracle_sid: "OR1"
    sap_anydb_install_oracle_base: "/oracle"
    sap_anydb_install_oracle_system_password: "Password1%"
    sap_anydb_install_oracle_extract_path: "/software/oracledb_extracted"

    - name: Execute Ansible Role sap_anydb_install_oracle
      include_role:
        name: { role: community.sap_install.sap_anydb_install_oracle }
```

## License

Apache license 2.0

## Author Information

Sean Freeman
