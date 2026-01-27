<!-- BEGIN Title -->
# sap_anydb_install_oracle Ansible Role
<!-- END Title -->

## Description
<!-- BEGIN Description -->
The Ansible role `sap_anydb_install_oracle` is used to install Oracle Database 19.x for SAP system.
<!-- END Description -->

<!-- BEGIN Dependencies -->
<!-- END Dependencies -->

<!-- BEGIN Prerequisites -->
## Prerequisites
Managed Nodes:

- Directory with installation media is present and `sap_anydb_install_oracle_extract_path` updated.</br>
  Download can be completed using [community.sap_launchpad](https://github.com/sap-linuxlab/community.sap_launchpad) Ansible Collection.
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

## Role Variables
<!-- BEGIN Role Variables -->
### sap_anydb_install_oracle_prep_reboot_ok

- _Type:_ `bool`
- _Default:_ `True`

Allows reboot of Managed node after packages are installed during pre-steps tasks.

### sap_anydb_install_oracle_prep_fail_if_reboot_required

- _Type:_ `bool`
- _Default:_ `False`

Enable to fail execution if packages are installed during pre-steps tasks, but you don't want to proceed with reboot. 

### sap_anydb_install_oracle_prep_precheck

- _Type:_ `bool`
- _Default:_ `False`

Enable to execute installation in Check mode to verify all inputs. This is extra validation and it does not disable installation.

### sap_anydb_install_oracle_method

- _Type:_ `string`
- _Default:_ `minimal`

Select installation method out of available: `minimal` or `responsefile`.

### sap_anydb_install_oracle_sid: 

- _Type:_ `string`
- _Default:_ `OR1`

Enter Oracle Database SID.

### sap_anydb_install_oracle_base

- _Type:_ `string`
- _Default:_ `/oracle`

Enter base folder for Oracle Database installation.

### sap_anydb_install_oracle_filesystem_storage

- _Type:_ `string`
- _Default:_ `/oradata`

Enter path for `oracle.install.db.config.starterdb.fileSystemStorage.dataLocation`

### sap_anydb_install_oracle_inventory_central

- _Type:_ `string`
- _Default:_ `/oraInventory`

Enter path for `INVENTORY_LOCATION`

### sap_anydb_install_oracle_system_password

- _Type:_ `string`

Enter password for Oracle SYSTEM user.

### sap_anydb_install_oracle_extract_path

- _Type:_ `string`

Enter path of Installation media, for example: `/software`.

### sap_anydb_install_oracle_patch_opatch_zip

- _Type:_ `string`

Enter name of Oracle opatch file, for example: `OPATCH19P_2308-70004508.ZIP`

### sap_anydb_install_oracle_patch_sap_zip 

- _Type:_ `string`

Enter name of Oracle SAP patch file, for example: `SAP19P_2311-70004508.ZIP`

### sap_anydb_install_oracle_patch_enable

- _Type:_ `bool`
- _Default:_ `False`

Enable to allow post-installation patching.
<!-- END Role Variables -->