## Input Parameters for sap_ha_pacemaker_cluster Ansible Role
<!-- BEGIN Role Input Parameters -->
### sap_hana_install_sid

- _Type:_ `string`

Enter SAP HANA System ID (SID).

### sap_hana_install_number

- _Type:_ `string`

Enter SAP HANA Instance number.

### sap_hana_install_fapolicyd_integrity

- _Type:_ `string`
- _Default:_ `sha256`

Select fapolicyd integrity check option out of: `none`, `size`, `sha256`, `ima`.

### sap_hana_install_check_sidadm_user

- _Type:_ `bool`
- _Default:_ `True`

If the variable `sap_hana_install_check_sidadm_user` is set to `False`, the role will install SAP HANA even
if the sidadm user exists. Default is `True`, in which case the installation will not be performed if the
sidadm user exists.

### sap_hana_install_new_system

- _Type:_ `bool`
- _Default:_ `True`

The variable `sap_hana_install_new_system` determines if the role will perform a fresh SAP HANA installation
or if it will add further hosts to an existing SAP HANA system as specified by variable
`sap_hana_install_addhosts`. Default is `True` for a fresh SAP HANA installation.

### sap_hana_install_update_firewall

- _Type:_ `bool`
- _Default:_ `False`

The role can be configured to also set the required firewall ports for SAP HANA. If this is desired, set
the variable `sap_hana_install_update_firewall` to `yes` (default is `no`). The firewall ports are defined
in a variable which is compatible with the variable structure used by Linux System Role `firewall`.
The firewall ports for SAP HANA are defined in member `port` of the first field of variable
`sap_hana_install_firewall` (`sap_hana_install_firewall[0].port`), see file `defaults/main.yml`. If the
member `state` is set to `enabled`, the ports will be enabled. If the member `state` is set to `disabled`,
the ports will be disabled, which might be useful for testing.

Certain parameters have identical meanings, for supporting different naming schemes in playbooks and inventories.
You can find those in the task `Rename some variables used by hdblcm configfile` of the file `tasks/main.yml`.
Example: The parameter `sap_hana_install_number`, which is used by the role to define the hdblm parameter `number`
(= SAP HANA instance number) can be defined by setting `sap_hana_instance_number`, `sap_hana_install_instance_nr`,
`sap_hana_install_instance_number`, or `sap_hana_install_number`. The order of precedence is from left to right.

<!-- END Role Input Parameters -->