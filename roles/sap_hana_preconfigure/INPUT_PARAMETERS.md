## Input Parameters for sap_hana_preconfigure Ansible Role
<!-- BEGIN Role Input Parameters -->
## Role Input Parameters

#### Minimum required parameters:

This role does not require any parameter to be set in the playbook or inventory.


### sap_hana_preconfigure_config_all
- _Type:_ `bool`

If set to `false`, the role will only execute or verify the installation or configuration steps of SAP notes.<br>
Default is to perform installation and configuration steps.<br>

### sap_hana_preconfigure_installation
- _Type:_ `bool`

If `sap_hana_preconfigure_config_all` is set to `false`, set this variable to `true` to perform only the<br>
installation steps of SAP notes.<br>

### sap_hana_preconfigure_configuration
- _Type:_ `bool`

If `sap_hana_preconfigure_config_all` is set to `false`, set this variable to `true` to perform only the<br>
configuration steps of SAP notes for which the corresponding SAP notes parameters have been set to `true`.<br>

Example:

```yaml
sap_hana_preconfigure_config_all: false
sap_hana_preconfigure_configuration: true
sap_hana_preconfigure_2772999_04: true
sap_hana_preconfigure_2382421: true
```

### sap_hana_preconfigure_assert
- _Type:_ `bool`
- _Default:_ `false`

If set to `true`, the role will run in assertion mode instead of the default configuration mode.<br>

### sap_hana_preconfigure_assert_all_config
- _Type:_ `bool`
- _Default:_ `false`

In assertion mode, the role will check either tuned or static settings.<br>
If this parameter is set to to `true`, the role will check both tuned and static settings.<br>

### sap_hana_preconfigure_assert_ignore_errors
- _Type:_ `bool`
- _Default:_ `false`

In assertion mode, the role will abort when encountering any assertion error.<br>
If this parameter is set to `false`, the role will *not* abort when encountering an assertion error.<br>
This is useful if the role is used for reporting a system's SAP notes compliance.<br>

### sap_hana_preconfigure_system_roles_collection
- _Type:_ `str`
- _Default:_ `'fedora.linux_system_roles'`
- _Possible Values:_<br>
  - `fedora.linux_system_roles`
  - `redhat.rhel_system_roles`

Set which Ansible Collection to use for the Linux System Roles.<br>
For community/upstream, use 'fedora.linux_system_roles'<br>
For the RHEL System Roles for SAP, or for Red Hat Automation Hub, use 'redhat.rhel_system_roles'<br>

### sap_hana_preconfigure_min_rhel_release_check
- _Type:_ `bool`
- _Default:_ `false`

Check the RHEL release against parameter `sap_hana_preconfigure_supported_rhel_minor_releases`, which is a list of<br>
known SAP HANA supported RHEL minor releases. By default, the role will display a message and continue running if<br>
the RHEL release is not part of that list. If set to `true`, the role will fail in such a case.<br>

### sap_hana_preconfigure_supported_rhel_minor_releases
- _Type:_ `list` with elements of type `str`
- _Default:_ (set by platform/environment specific variables)

Use this parameter to set your own list of SAP HANA supported RHEL minor releases.<br>

### sap_hana_preconfigure_enable_sap_hana_repos
- _Type:_ `bool`
- _Default:_ `false`

Set to 'true' to enable the SAP HANA required RHEL repos.<br>
This parameter is deprecated because the role sap_general_preconfigure can be used for this purpose.<br>
The related parameters are `sap_general_preconfigure_enable_repos` and `sap_general_preconfigure_use_hana_repos`.<br>

### sap_hana_preconfigure_req_repos_redhat_7_x86_64
- _Type:_ `list` with elements of type `str`
- _Default:_ (set by platform/environment specific variables)

Use this parameter to set your own list of SAP HANA required RHEL 7 repos on x86_64'<br>
This parameter is deprecated because the role sap_general_preconfigure can be used for this purpose.<br>
The related parameters are `sap_general_preconfigure_enable_repos` and `sap_general_preconfigure_req_repos`.<br>

### sap_hana_preconfigure_req_repos_redhat_7_ppc64le
- _Type:_ `list` with elements of type `str`
- _Default:_ (set by platform/environment specific variables)

Use this parameter to set your own list of SAP HANA required RHEL 7 repos on ppc64le'<br>
This parameter is deprecated because the role sap_general_preconfigure can be used for this purpose.<br>
The related parameters are `sap_general_preconfigure_enable_repos` and `sap_general_preconfigure_req_repos`.<br>

### sap_hana_preconfigure_req_repos_redhat_8_x86_64
- _Type:_ `list` with elements of type `str`
- _Default:_ (set by platform/environment specific variables)

Use this parameter to set your own list of SAP HANA required RHEL 8 repos on x86_64'<br>
This parameter is deprecated because the role sap_general_preconfigure can be used for this purpose.<br>
The related parameters are `sap_general_preconfigure_enable_repos` and `sap_general_preconfigure_req_repos`.<br>

### sap_hana_preconfigure_req_repos_redhat_8_ppc64le
- _Type:_ `list` with elements of type `str`
- _Default:_ (set by platform/environment specific variables)

Use this parameter to set your own list of SAP HANA required RHEL 8 repos on ppc64le'<br>
This parameter is deprecated because the role sap_general_preconfigure can be used for this purpose.<br>
The related parameters are `sap_general_preconfigure_enable_repos` and `sap_general_preconfigure_req_repos`.<br>

### sap_hana_preconfigure_req_repos_redhat_9_x86_64
- _Type:_ `list` with elements of type `str`
- _Default:_ (set by platform/environment specific variables)

Use this parameter to set your own list of SAP HANA required RHEL 9 repos on x86_64'<br>
This parameter is deprecated because the role sap_general_preconfigure can be used for this purpose.<br>
The related parameters are `sap_general_preconfigure_enable_repos` and `sap_general_preconfigure_req_repos`.<br>

### sap_hana_preconfigure_req_repos_redhat_9_ppc64le
- _Type:_ `list` with elements of type `str`
- _Default:_ (set by platform/environment specific variables)

Use this parameter to set your own list of SAP HANA required RHEL 9 repos on ppc64le'<br>
This parameter is deprecated because the role sap_general_preconfigure can be used for this purpose.<br>
The related parameters are `sap_general_preconfigure_enable_repos` and `sap_general_preconfigure_req_repos`.<br>

### sap_hana_preconfigure_set_minor_release
- _Type:_ `bool`
- _Default:_ `false`

Use this parameter to set the RHEL minor release, which is required for SAP HANA.<br>
The related parameter is `sap_general_preconfigure_set_minor_release`.<br>

### sap_hana_preconfigure_create_directories
- _Type:_ `bool`
- _Default:_ `true`

Set to `false` if you do not want the SAP HANA directories to be created by the role.<br>
The SAP HANA directories will always be created if `sap_hana_preconfigure_modify_selinux_labels`<br>
(see below) is set to `true`, no matter how `sap_hana_preconfigure_create_directories` is set.<br>

### sap_hana_preconfigure_hana_directories
- _Type:_ `list` with elements of type `str`
- _Default:_
  - /hana
  - /lss/shared

List of SAP HANA directories to be created.<br>

### sap_hana_preconfigure_modify_selinux_labels
- _Type:_ `bool`
- _Default:_ `true`

For compatibility of SAP HANA with SELinux in enforcing mode, the role will recursively add<br>
the `usr_t` label to directories and files in the directories where HANA is installed.<br>
If relabeling not desired, set this parameter `false`.<br>
If the variable is set to `true`, the SAP HANA directories will be created no matter<br>
how the variable `sap_hana_preconfigure_create_directories` (see above) is set.<br>

### sap_hana_preconfigure_packages
- _Type:_ `list` with elements of type `str`
- _Default:_ (set by platform/environment specific variables)

List of RHEL packages to be installed for SAP HANA. For RHEL 8 and later, you can choose to install either the default list<br>
or a list of the minimum required packages for SAP HANA server (parameter `__sap_hana_preconfigure_packages_min_install`).<br>

### sap_hana_preconfigure_min_package_check
- _Type:_ `bool`
- _Default:_ `true`

SAP HANA requires certain minimum package versions to be supported. These minimum levels are listed in SAP Note 2235581.<br>
Set this parameter to `false` if you want to ignore these requirements.<br>

### sap_hana_preconfigure_update
- _Type:_ `bool`
- _Default:_ `false`

Set this parameter to `true` to update the system to the latest package levels.<br>
By setting the parameter `sap_general_preconfigure_set_minor_release` of the<br>
role `sap_general_preconfigure` to `true`, you can install the most recent package updates<br>
without updating to a more recent RHEL minor release.<br>

### sap_hana_preconfigure_reboot_ok
- _Type:_ `bool`
- _Default:_ `false`

Set to `true` if you want to perform a reboot at the end of the role, if necessary.<br>

### sap_hana_preconfigure_fail_if_reboot_required
- _Type:_ `bool`
- _Default:_ `true`

If `sap_hana_preconfigure_reboot_ok` is set to `false`, which is the default, a reboot requirement should not<br>
remain unnoticed. For this reason, we let the role fail. Set this parameter to `false` to override this behavior.<br>
Can be useful if you want to implement your own reboot handling.<br>

### sap_hana_preconfigure_kernel_parameters
- _Type:_ `list` with elements of type `str`
- _Default:_ (set by platform/environment specific variables)

Network related linux kernel parameter settings for SAP HANA on all hardware platforms.<br>

### sap_hana_preconfigure_kernel_parameters_ppc64le
- _Type:_ `list` with elements of type `str`
- _Default:_ (set by platform/environment specific variables)

Network related linux kernel parameter settings for platform ppc64le.<br>

### sap_hana_preconfigure_use_netapp_settings_nfs
- _Type:_ `bool`
- _Default:_ `false`

Set to `true` to also set NetApp NFS required kernel parameters.<br>

### sap_hana_preconfigure_install_ibm_power_tools
- _Type:_ `bool`
- _Default:_ `true`

Set this parameter to `false` to not install the IBM Power Systems service and productivity tools.<br>

### sap_hana_preconfigure_add_ibm_power_repo
- _Type:_ `bool`
- _Default:_ `true`

Set this parameter to `false` if you do not want to add the IBM Power tools repository (e.g. because the packages<br>
are already available on the local network). The IBM Power Systems service and productivity tools will only<br>
be installed if the variable `sap_hana_preconfigure_install_ibm_power_tools` is set to `true`, which is the default.<br>

### sap_hana_preconfigure_ibm_power_repo_url
- _Type:_ `str`
- _Default:_ (set by platform/environment specific variables)

URL of the IBM Power tools repository.<br>

### sap_hana_preconfigure_ppcle_mtu9000_if
- _Type:_ `str`
- _Default:_ `''`

List of interfaces for which the MTU size will be set to `9000`.<br>

### sap_hana_preconfigure_ppcle_tso_if
- _Type:_ `list` with elements of type `str`
- _Default:_
  '{{ ansible_interfaces | difference([''lo'']) }}'

List of interfaces for which the tso flag will be set.<br>

### sap_hana_preconfigure_use_tuned
- _Type:_ `bool`
- _Default:_ `true`

Use tuned for configuring most of the kernel settings for SAP HANA<br>
Set this parameter to `false` to use static kernel settings<br>

### sap_hana_preconfigure_tuned_profile
- _Type:_ `str`
- _Default:_ `'sap-hana'`

Name of the SAP HANA tuned tuned profile to enable (RHEL).<br>

### sap_hana_preconfigure_modify_grub_cmdline_linux
- _Type:_ `bool`
- _Default:_ `false`

Set this parameter to `true` to modify the Grub boot command line.<br>

### sap_hana_preconfigure_run_grub2_mkconfig
- _Type:_ `bool`
- _Default:_ `true`

By default, the role will run `grub2-mkconfig` to update the Grub configuration if necessary.<br>
Set this parameter to `false` if this is not desired.<br>

### sap_hana_preconfigure_db_group_name
- _Type:_ `str`

Use this parameter to specify the name of the RHEL group which is used for the database processes.<br>
It will be used to configure process limits as per step "Configuring Process Resource Limits" of SAP note 2772999.<br>

Example:

```yaml
sap_hana_preconfigure_db_group_name: dba
```

### sap_hana_preconfigure_saptune_version
- _Type:_ `str`
- _Default:_ `''`

Version of saptune to install (SLES for SAP Applications).<br>
This will replace the current installed version if present, even downgrade if necessary.<br>

### sap_hana_preconfigure_saptune_solution
- _Type:_ `str`
- _Default:_ `'HANA'`
- _Possible Values:_<br>
  - `HANA`
  - `NETWEAVER+HANA`
  - `S4HANA-APP+DB`
  - `S4HANA-DBSERVER`

The saptune solution to apply (SLES for SAP Applications).<br>

### sap_hana_preconfigure_saptune_azure
- _Type:_ `bool`
- _Default:_ `false`

On Azure, TCP timestamps, reuse and recycle should be disabled (SLES for SAP Applications).<br>
If the variable is set, an override file for saptune will be created (/etc/saptune/override/2382421) to set net.ipv4.tcp_timestamps and net.ipv4.tcp_tw_reuse to 0.<br>
Set this parameter to `true` on Azure.<br>

<!-- END Role Input Parameters -->