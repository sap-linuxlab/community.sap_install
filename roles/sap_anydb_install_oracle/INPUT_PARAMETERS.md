## Input Parameters for sap_anydb_install_oracle Ansible Role
<!-- BEGIN Role Input Parameters -->

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

<!-- END Role Input Parameters -->