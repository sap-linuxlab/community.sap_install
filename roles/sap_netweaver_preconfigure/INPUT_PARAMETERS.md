## Input Parameters for sap_netweaver_preconfigure Ansible Role
<!-- BEGIN Role Input Parameters -->
## Role Input Parameters

Minimum required parameters:
This role does not require any parameter to be set in the playbook or inventory.


### sap_netweaver_preconfigure_config_all
- _Type:_ `bool`
- _Default:_ `true`

If set to `false`, the role will only execute or verify the installation or configuration steps of SAP notes.<br>
Default is to perform installation and configuration steps.<br>

### sap_netweaver_preconfigure_installation
- _Type:_ `bool`
- _Default:_ `false`

If `sap_netweaver_preconfigure_config_all` is set to `false`, set this variable to `true` to perform only the<br>
installation steps of SAP notes.<br>

### sap_netweaver_preconfigure_configuration
- _Type:_ `bool`
- _Default:_ `false`

If `sap_netweaver_preconfigure_config_all` is set to `false`, set this variable to `true` to perform only the<br>
configuration steps of SAP notes.<br>

### sap_netweaver_preconfigure_assert
- _Type:_ `bool`
- _Default:_ `false`

If set to `true`, the role will run in assertion mode instead of the default configuration mode.<br>

### sap_netweaver_preconfigure_assert_ignore_errors
- _Type:_ `bool`
- _Default:_ `false`

In assertion mode, the role will abort when encountering any assertion error.<br>
If this parameter is set to `false`, the role will *not* abort when encountering an assertion error.<br>
This is useful if the role is used for reporting a system's SAP notes compliance.<br>

### sap_netweaver_preconfigure_min_swap_space_mb
- _Type:_ `str`
- _Default:_ `20480`

Specifies the minimum amount of swap space on the system required by SAP NetWeaver.<br>
If this requirement is not met, the role will abort.<br>
Set your own value to override the default of `20480`.<br>

### sap_netweaver_preconfigure_fail_if_not_enough_swap_space_configured
- _Type:_ `bool`
- _Default:_ `true`

If the system does not have the minimum amount of swap space configured as defined<br>
in parameter `sap_netweaver_preconfigure_min_swap_space_mb`, the role will abort.<br>
By setting this parameter to `false`, the role will not abort in such cases.<br>

### sap_netweaver_preconfigure_rpath
- _Type:_ `str`
- _Default:_ `/usr/sap/lib`

Specifies the SAP kernel's `RPATH`. This is where the SAP kernel is searching for libraries, and where the role<br>
is creating a link named `libstdc++.so.6` pointing to `/opt/rh/SAP/lib64/compat-sap-c++-10.so`,<br>
so that newer SAP kernels which are built with GCC10 can find the required symbols.<br>

### sap_netweaver_preconfigure_use_adobe_doc_services
- _Type:_ `bool`
- _Default:_ `false`

Set this parameter to `true` when using Adobe Document Services, to ensure all required packages are installed.<br>

### sap_netweaver_preconfigure_saptune_version
- _Type:_ `str`
- _Default:_ `3.0.2`

On SLES systems, specifies the saptune version<br>

### sap_netweaver_preconfigure_saptune_solution
- _Type:_ `str`
- _Default:_ `NETWEAVER`
- _Possible Values:_<br>
  - `NETWEAVER`
  - `NETWEAVER+HANA`
  - `S4HANA-APP+DB`
  - `S4HANA-APPSERVER`
  - `S4HANA-DBSERVER`

On SLES systems, specifies the saptune solution to apply.<br>

<!-- END Role Input Parameters -->