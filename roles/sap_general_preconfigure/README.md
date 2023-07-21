# sap_general_preconfigure Ansible Role

This role installs required packages and performs configuration steps which are required for installing and running SAP NetWeaver or SAP HANA. Specific installation and configuration steps on top of these basic steps are performed with roles sap-netweaver-preconfigure and sap-hana-preconfigure. Future implementations may reduce the scope of this role, for example if certain installation or configuration steps are done in the more specific roles.

For SLES systems, this role may not be necessary.  The majority of SAP preparation and tuning is covered by `saptune` which is configured in the `sap_hana_preconfigure` and `sap_netweaver_preconfigure` roles.

## Requirements

The role requires additional collections which are specified in `meta/collection-requirements.yml`. Before using this role,
make sure that the required collections are installed, for example by using the following command:

`ansible-galaxy install -vv -r meta/collection-requirements.yml`

To use this role, your system needs to be installed according to:
- RHEL 7: SAP note 2002167, Red Hat Enterprise Linux 7.x: Installation and Upgrade, section "Installing Red Hat Enterprise Linux 7"
- RHEL 8: SAP note 2772999, Red Hat Enterprise Linux 8.x: Installation and Configuration, section "Installing Red Hat Enterprise Linux 8".

Note
----
Do not run this role against an SAP or other production system. The role will enforce a certain configuration on the managed node(s), which might not be intended.

<!-- BEGIN: Role Input Parameters for sap_general_preconfigure -->
## Role Input Parameters

#### Minimum required parameters:

This role does not require any parameter to be set in the playbook or inventory.


### sap_general_preconfigure_config_all
- _Type:_ `bool`

If set to `false`, the role will only execute or verify the installation or configuration steps of SAP notes.<br>
Default is to perform installation and configuration steps.<br>

### sap_general_preconfigure_installation
- _Type:_ `bool`

If `sap_general_preconfigure_config_all` is set to `false`, set this variable to `true` to perform only the<br>
installation steps of SAP notes.<br>

### sap_general_preconfigure_configuration
- _Type:_ `bool`

If `sap_general_preconfigure_config_all` is set to `false`, set this variable to `true` to perform only the<br>
configuration steps of SAP notes for which the corresponding SAP notes parameters have been set to `true`.<br>

Example:

```yaml
sap_general_preconfigure_config_all: false
sap_general_preconfigure_configuration: true
sap_general_preconfigure_2002167_02: true
sap_general_preconfigure_1391070: true
```

### sap_general_preconfigure_assert
- _Type:_ `bool`
- _Default:_ `false`

If set to `true`, the role will run in assertion mode instead of the default configuration mode.<br>

### sap_general_preconfigure_assert_ignore_errors
- _Type:_ `bool`
- _Default:_ `false`

In assertion mode, the role will abort when encountering any assertion error.<br>
If this parameter is set to `false`, the role will *not* abort when encountering an assertion error.<br>
This is useful if the role is used for reporting a system's SAP notes compliance.<br>

### sap_general_preconfigure_system_roles_collection
- _Type:_ `str`
- _Default:_ `'fedora.linux_system_roles'`
- _Possible Values:_<br>
  - `fedora.linux_system_roles`
  - `redhat.rhel_system_roles`

Set which Ansible Collection to use for the Linux System Roles.<br>
For community/upstream, use 'fedora.linux_system_roles'<br>
For the RHEL System Roles for SAP, or for Red Hat Automation Hub, use 'redhat.rhel_system_roles'<br>

### sap_general_preconfigure_enable_repos
- _Type:_ `bool`
- _Default:_ `false`

Set to `true` if you want the role to enable the repos as configured by the following repo related parameters.<br>
The default is `false`, meaning that the role will not enable repos.<br>

### sap_general_preconfigure_use_netweaver_repos
- _Type:_ `bool`
- _Default:_ `true`

Set to `false` if you want the role to not enable the SAP NetWeaver repo(s).<br>
The default is `true`, meaning that the role will enable the SAP NetWeaver repo(s).<br>
Only valid if `sap_general_preconfigure_enable_repos` is set to `true`.<br>

### sap_general_preconfigure_use_hana_repos
- _Type:_ `bool`
- _Default:_ `true`

Set to `false` if you want the role to not enable the SAP HANA repo(s).<br>
The default is `true`, meaning that the role will enable the SAP HANA repo(s).<br>
Only valid if `sap_general_preconfigure_enable_repos` is set to `true`.<br>

### sap_general_preconfigure_use_ha_repos
- _Type:_ `bool`
- _Default:_ `true`

Set to `false` if you want the role to not enable the high availability repo(s).<br>
The default is `true`, meaning that the role will enable the high availability repo(s).<br>
Only valid if `sap_general_preconfigure_enable_repos` is set to `true`.<br>

### sap_general_preconfigure_disable_all_other_repos
- _Type:_ `bool`
- _Default:_ `true`

Set to `false` if you want the role to not disable all repos before enabling the desired ones as configured above.<br>
The default is `true`, meaning that the role will disable all repos before enabling the desired ones.<br>
Only valid if `sap_general_preconfigure_enable_repos` is set to `true`.<br>

### sap_general_preconfigure_req_repos
- _Type:_ `list` with elements of type `str`

If you want to provide your own list of repos (e.g. on cloud systems), set this variable accordingly.<br>
Otherwise, the RHEL default repo names with the maximum support duration for the RHEL minor release are chosen automatically<br>
(e.g. normal repos for RHEL 8.3, e4s repos for RHEL 8.4).<br>

Example:

```yaml
sap_general_preconfigure_req_repos:
- rhel-8-for-x86_64-baseos-eus-rpms
- rhel-8-for-x86_64-appstream-eus-rpms
- rhel-8-for-x86_64-sap-solutions-eus-rpms
- rhel-8-for-x86_64-sap-netweaver-eus-rpms
- rhel-8-for-x86_64-highavailability-eus-rpms
```

### sap_general_preconfigure_set_minor_release
- _Type:_ `bool`
- _Default:_ `false`

Set to `true` if you want the role to set the RHEL minor release, which is required for SAP HANA. Default is `false`.<br>
If you set the RHEL minor release, then you must also use the `eus` or `e4s` repos.<br>

### sap_general_preconfigure_packagegroups
- _Type:_ `str`
- _Default:_ (set by platform/environment specific variables)

The name of the software package group to install.<br>
The default for this parameter is set in the vars file which corresponds to the detected OS version.<br>

Example:

```yaml
'@minimal-environment'
```

### sap_general_preconfigure_envgroups
- _Type:_ `str`
- _Default:_ (set by platform/environment specific variables)

The name of the software environment group to check.<br>
The default for this parameter is set in the vars file which corresponds to the detected OS version.<br>

Example:

```yaml
'@minimal-environment'
```

### sap_general_preconfigure_packages
- _Type:_ `list` with elements of type `str`
- _Default:_ (set by platform/environment specific variables)

The list of packages to install.<br>
The default for this variable is set in the vars file which corresponds to the detected OS version.<br>

### sap_general_preconfigure_min_package_check
- _Type:_ `bool`
- _Default:_ `true`

The default is to install or check if the minimum package versions are installed as defined in the vars files.<br>
Set to `false` if you do not install or check these minimum package versions.<br>

### sap_general_preconfigure_install_ibm_power_tools
- _Type:_ `bool`
- _Default:_ `true`

Set this parameter to `false` to not install the IBM Power Systems service and productivity tools.<br>
See also SAP note 2679703.<br>

### sap_general_preconfigure_add_ibm_power_repo
- _Type:_ `bool`
- _Default:_ `true`

Set this parameter to `false` if you do not want to add the IBM Power tools repository (e.g. because the packages<br>
are already available on the local network). The IBM Power Systems service and productivity tools will only<br>
be installed if the variable `sap_general_preconfigure_install_ibm_power_tools` is set to `true`, which is the default.<br>

### sap_general_preconfigure_ibm_power_repo_url
- _Type:_ `str`
- _Default:_ `'https://public.dhe.ibm.com/software/server/POWER/Linux/yum/download/ibm-power-repo-latest.noarch.rpm'`

URL for the IBM Power Systems service and productivity tools, see https://www.ibm.com/support/pages/service-and-productivity-tools<br>

### sap_general_preconfigure_update
- _Type:_ `bool`
- _Default:_ `false`

By default, the role will not update the system, for avoiding an unintentional minor OS release update.<br>
Set this parameter to `true` if you want to update your system to the latest package versions.<br>
When using SAP HANA, make sure to set the release lock properly so the minor OS release will be one of<br>
those for which SAP HANA is supported. See also `sap_general_preconfigure_set_minor_release`.<br>

### sap_general_preconfigure_reboot_ok
- _Type:_ `bool`
- _Default:_ `false`

Set to `true` if you want to perform a reboot at the end of the role, if necessary.<br>

### sap_general_preconfigure_fail_if_reboot_required
- _Type:_ `bool`
- _Default:_ `true`

If `sap_general_preconfigure_reboot_ok` is set to `false`, which is the default, a reboot requirement should not<br>
remain unnoticed. For this reason, we let the role fail. Set this parameter to `false` to override this behavior.<br>
Can be useful if you want to implement your own reboot handling.<br>

### sap_general_preconfigure_selinux_state
- _Type:_ `str`
- _Default:_ `'permissive'`
- _Possible Values:_<br>
  - `enforcing`
  - `permissive`
  - `disabled`

One of the SELinux states to be set on the system.<br>

### sap_general_preconfigure_modify_selinux_labels
- _Type:_ `bool`
- _Default:_ `true`

Set to `false` if you do not want to modify the SELinux labels for the SAP directory `/usr/sap`.<br>

### sap_general_preconfigure_size_of_tmpfs_gb
- _Type:_ `str`
- _Default:_ `"{{ ((0.75 * (ansible_memtotal_mb + ansible_swaptotal_mb)) / 1024) | round | int }}"`

The size of the tmpfs in GB. The formula used here is mentioned in SAP note 941735.<br>

### sap_general_preconfigure_modify_etc_hosts
- _Type:_ `bool`
- _Default:_ `true`

Set to `false` if you do not want the role to modify the `/etc/hosts` file.<br>

### sap_general_preconfigure_etc_sysctl_sap_conf
- _Type:_ `str`
- _Default:_ `'/etc/sysctl.d/sap.conf'`

The file name of the sysctl config file to be used<br>

### sap_general_preconfigure_kernel_parameters
- _Type:_ `list` with elements of type `dict`
- _Default:_ (set by platform/environment specific variables)

The Linux kernel parameters to use. By default, these are taken from the vars file.<br>
The default for this parameter is set in the vars file which corresponds to the detected OS version.<br>

Example:

```yaml
sap_general_preconfigure_kernel_parameters:
- name: vm.max_map_count
  value: '2147483647'
- name: fs.aio-max-nr
  value: '18446744073709551615'
```

### sap_general_preconfigure_max_hostname_length
- _Type:_ `str`
- _Default:_ `'13'`

The maximum length of the hostname. See SAP note 611361.<br>

### sap_hostname
- _Type:_ `str`
- _Default:_ `"{{ ansible_hostname }}"`

The hostname to be used for updating or checking `/etc/hosts` entries.<br>

### sap_domain
- _Type:_ `str`
- _Default:_ `"{{ ansible_domain }}"`

The DNS domain name to be used for updating or checking `/etc/hosts` entries.<br>

### sap_ip
- _Type:_ `str`
- _Default:_ `"{{ ansible_default_ipv4.address }}"`

The IPV4 address to be used for updating or checking `/etc/hosts` entries.<br>

### sap_general_preconfigure_db_group_name
- _Type:_ `str`

Use this variable to specify the name of the RHEL group which is used for the database processes.<br>
If defined, it will be used to configure process limits as per step<br>
Configuring Process Resource Limits<br>

Example:

```yaml
sap_general_preconfigure_db_group_name: dba
```

<!-- END: Role Input Parameters for sap_general_preconfigure -->

## Dependencies

This role does not depend on any other role.

## Example Playbook

Simple playbook, named sap.yml:
```yaml
---
- hosts: all
  roles:
    - role: sap_general_preconfigure
```

## Example Usage

Normal run:
```yaml
ansible-playbook sap.yml -l remote_host
```

Extended Check (assert) run, aborting for any error which has been found:
```yaml
ansible-playbook sap.yml -l remote_host -e "{sap_general_preconfigure_assert: yes}"
```

Extended Check (assert) run, not aborting even if an error has been found:
```yaml
ansible-playbook sap.yml -l remote_host -e "{sap_general_preconfigure_assert: yes, sap_general_preconfigure_assert_ignore_errors: no}"
```

Same as above, with a nice compact and colored output, this time for two hosts:
```yaml
ansible-playbook sap.yml -l host_1,host_2 -e "{sap_general_preconfigure_assert: yes, sap_general_preconfigure_assert_ignore_errors: yes}" |
awk '{sub ("    \"msg\": ", "")}
  /TASK/{task_line=$0}
  /fatal:/{fatal_line=$0; nfatal[host]++}
  /...ignoring/{nfatal[host]--; if (nfatal[host]<0) nfatal[host]=0}
  /^[a-z]/&&/: \[/{gsub ("\\[", ""); gsub ("]", ""); gsub (":", ""); host=$2}
  /SAP note/{print "\033[30m[" host"] "$0}
  /FAIL:/{nfail[host]++; print "\033[31m[" host"] "$0}
  /WARN:/{nwarn[host]++; print "\033[33m[" host"] "$0}
  /PASS:/{npass[host]++; print "\033[32m[" host"] "$0}
  /INFO:/{print "\033[34m[" host"] "$0}
  /changed/&&/unreachable/{print "\033[30m[" host"] "$0}
  END{print ("---"); for (var in npass) {printf ("[%s] ", var); if (nfatal[var]>0) {
        printf ("\033[31mFATAL ERROR!!! Playbook might have been aborted!!!\033[30m Last TASK and fatal output:\n"); print task_line, fatal_line
     }
     else printf ("\033[31mFAIL: %d  \033[33mWARN: %d  \033[32mPASS: %d\033[30m\n", nfail[var], nwarn[var], npass[var])}}'
```
Note: For terminals with dark background, replace the color code `30m` by `37m`.
In case you need to make an invisible font readable on a terminal with dark background, run the following command in the terminal:
```yaml
printf "\033[37mreadable font\n"
```
In case you need to make an invisible font readable on a terminal with bright background, run the following command in the terminal:
```yaml
printf "\033[30mreadable font\n"
```

## License

Apache license 2.0

## Author Information

Red Hat for SAP Community of Practice, Bernd Finger, Markus Koch, Rainer Leber
