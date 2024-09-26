<!-- BEGIN Title -->
# sap_anydb_install_oracle Ansible Role
<!-- END Title -->

## Description
<!-- BEGIN Description -->
Ansible role `sap_anydb_install_oracle` is used to install Oracle Database 19.x for SAP system.
<!-- END Description -->

<!-- BEGIN Dependencies -->
<!-- END Dependencies -->

<!-- BEGIN Prerequisites -->
## Prerequisites
Managed nodes:
- Directory with installation media is present and `sap_anydb_install_oracle_extract_path` updated. Download can be completed using [community.sap_launchpad](https://github.com/sap-linuxlab/community.sap_launchpad) Ansible Collection.
<!-- END Prerequisites -->

## Execution
<!-- BEGIN Execution -->
<!-- END Execution -->

<!-- BEGIN Execution Recommended -->
<!-- END Execution Recommended -->

### Execution Flow
<!-- BEGIN Execution Flow -->
1. Prepare OS: Install packages, create users, create folders and copy installation media.
2. Install Oracle Database in desired method
3. Execute post installation tasks
4. Apply Oracle Patches if available
<!-- END Execution Flow -->

### Example
<!-- BEGIN Execution Example -->
```yaml
---
- name: Ansible Play for Oracle Database installation
  hosts: oracle_host
  become: true
  tasks:
    - name: Execute Ansible Role sap_anydb_install_oracle
      ansible.builtin.include_role:
        name: community.sap_install.sap_anydb_install_oracle
      vars:
        sap_anydb_install_oracle_method: minimal
        sap_anydb_install_oracle_sid: "OR1"
        sap_anydb_install_oracle_base: "/oracle"
        sap_anydb_install_oracle_system_password: "Password1%"
        sap_anydb_install_oracle_extract_path: "/software/oracledb_extracted"
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

## Role Input Parameters
All input parameters used by role are described in [INPUT_PARAMETERS.md](https://github.com/sap-linuxlab/community.sap_install/blob/main/roles/sap_anydb_install_oracle/INPUT_PARAMETERS.md)
