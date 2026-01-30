<!-- BEGIN Title -->
# sap_general_preconfigure Ansible Role
<!-- END Title -->
![Ansible Lint for sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_general_preconfigure.yml/badge.svg)

## Description
<!-- BEGIN Description -->
The Ansible role `sap_general_preconfigure` installs required packages and performs basic OS configuration steps according to applicable SAP notes for installing and running SAP HANA or SAP ABAP Application Platform (formerly known as SAP NetWeaver).

Specific installation and configuration steps then have to be performed with the roles [sap_hana_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_preconfigure) and [sap_netweaver_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_netweaver_preconfigure).
<!-- END Description -->

<!-- BEGIN Dependencies -->
## Dependencies
- `fedora.linux_system_roles`
    - Roles:
        - `selinux`
- `community.sap_install` (This collection)
    - Roles:
        - `sap_maintain_etc_hosts`

Install required collections by `ansible-galaxy collection install -vv -r meta/collection-requirements.yml`.
<!-- END Dependencies -->

<!-- BEGIN Prerequisites -->
## Prerequisites

(Red Hat specific) Ensure system is installed according to:

- RHEL 8: SAP note 2772999, Red Hat Enterprise Linux 8.x: Installation and Configuration, section `Installing Red Hat Enterprise Linux 8`.
- RHEL 9: SAP note 3108316, Red Hat Enterprise Linux 9.x: Installation and Configuration, section `Installing Red Hat Enterprise Linux 9`.

<!-- END Prerequisites -->

## Execution
<!-- BEGIN Execution -->
**:warning: Do not execute this Ansible Role against existing SAP systems unless you know what you are doing and you prepare inputs to avoid unintended changes caused by default inputs.**
<!-- END Execution -->

<!-- BEGIN Execution Recommended -->
<!-- END Execution Recommended -->

### Execution Flow
<!-- BEGIN Execution Flow -->
1. Assert that required inputs were provided.
2. Install required packages and patch system if `sap_general_preconfigure_update:true`
3. Apply configurations based on SAP Notes
4. Reboot Managed nodes if packages were installed or patched and `sap_general_preconfigure_reboot_ok: true`
<!-- END Execution Flow -->

### Example
<!-- BEGIN Execution Example -->
```yaml
---
- name: Ansible Play for SAP HANA HA Scale-up preconfigure
  hosts: hana_primary, hana_secondary
  become: true
  tasks:
    - name: Execute Ansible Role sap_general_preconfigure
      ansible.builtin.include_role:
        name: community.sap_install.sap_general_preconfigure
```
Further referenced as `example.yml`
<!-- END Execution Example -->

<!-- BEGIN Role Tags -->
### Role Tags

With the following tags, the role can be called to perform certain activities only:

- tag `sap_general_preconfigure_installation`: Perform only the installation tasks
- tag `sap_general_preconfigure_configuration`: Perform only the configuration tasks
- tag `sap_general_preconfigure_3108316`: Perform only the tasks(s) related to this SAP note.
- tag `sap_general_preconfigure_2772999_03`: Perform only the tasks(s) related to step 3 of the SAP note.
- tag `sap_general_preconfigure_etc_hosts`: Perform only the tasks(s) related to this step. This step might be one of multiple
  configuration activities of a SAP note. Also this step might be valid for multiple RHEL major releases.

#### How to run sap_general_preconfigure with tags

Perform only installation tasks:
```console
ansible-playbook sap.yml --tags=sap_general_preconfigure_installation
```

Perform only configuration tasks:
```console
ansible-playbook sap.yml --tags=sap_general_preconfigure_configuration
```

Verify and modify /etc/hosts file:
```console
ansible-playbook sap.yml --tags=sap_general_preconfigure_etc_hosts
```

Perform all configuration steps except verifying and modifying the /etc/hosts file
```
ansible-playbook sap.yml --tags=sap_general_preconfigure_configuration --skip_tags=sap_general_preconfigure_etc_hosts
```

(Red Hat) Perform configuration activities related to SAP note 3108316 (RHEL 9)
```
ansible-playbook sap.yml --tags=sap_general_preconfigure_3108316
```

(Red Hat) Perform configuration activities related to step 2 (SELinux settings) of SAP note 3108316 (RHEL 9)
```
ansible-playbook sap.yml --tags=sap_general_preconfigure_3108316_02
```

(Red Hat) Perform all configuration activities except those related to step 2 (SELinux settings) of SAP note 3108316 (RHEL 9 specific)
```
ansible-playbook sap-general-preconfigure.yml --tags=sap_general_preconfigure_configuration --skip_tags=sap_general_preconfigure_3108316_02
```
<!-- END Role Tags -->

<!-- BEGIN Further Information -->
## Further Information
For more examples on how to use this role in different installation scenarios, refer to the [ansible.playbooks_for_sap](https://github.com/sap-linuxlab/ansible.playbooks_for_sap) playbooks.
<!-- END Further Information -->

## License
<!-- BEGIN License -->
Apache 2.0
<!-- END License -->

## Maintainers
<!-- BEGIN Maintainers -->
- [Bernd Finger](https://github.com/berndfinger)
<!-- END Maintainers -->

## Role Variables
<!-- BEGIN Role Variables -->
### Controlling execution with input parameters
Extended Check (assert) run, aborting for any error which has been found:
```yaml
ansible-playbook sap.yml -l remote_host -e "{sap_general_preconfigure_assert: yes}"
```

Extended Check (assert) run, not aborting even if an error has been found:
```yaml
ansible-playbook sap.yml -l remote_host -e "{sap_general_preconfigure_assert: yes,sap_general_preconfigure_assert_ignore_errors: no}"
```

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

Set which Ansible Collection to use for the Linux System Roles.<br>
Available values:
- `fedora.linux_system_roles` - for community/upstream.<br>
- `redhat.rhel_system_roles` - for the RHEL System Roles for SAP, or for Red Hat Automation Hub.<br>

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

(RedHat specific) The name of the software package group to install.<br>
The default for this parameter is set in the vars file which corresponds to the detected OS version.<br>

Example:

```yaml
'@minimal-environment'
```

### sap_general_preconfigure_envgroups
- _Type:_ `str`
- _Default:_ (set by platform/environment specific variables)

(RedHat specific) The name of the software environment group to check.<br>
The default for this parameter is set in the vars file which corresponds to the detected OS version.<br>

Example:

```yaml
'@minimal-environment'
```

### sap_general_preconfigure_patterns
- _Type:_ `list` with elements of type `str`
- _Default:_ (set by platform/environment specific variables)

(SUSE specific) The list of the zypper patterns to install.<br>
The default for this parameter is set in the vars file which corresponds to the detected OS version.<br>

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

### sap_general_preconfigure_selinux_mode
- _Type:_ `str`
- _Default:_ `'permissive'`
- _Possible Values:_<br>
  - `enforcing`
  - `permissive`
  - `disabled`

One of the three SELinux modes to be set on the system.<br>
Note: A transition from `disabled` to `enforcing` is not supported, see the `Using SELinux` RHEL product documentation<br>
and Red Hat Bug 2021835.<br>

### sap_general_preconfigure_fail_if_selinux_mode_lowered
- _Type:_ `bool`
- _Default:_ `true`

If the system is running with a higher SELinux mode than demanded by the<br>
variable `sap_general_preconfigure_selinux_mode`, we let the role fail in order to avoid an<br>
unintentional configuration change to a lower SELinux security level.<br>
Set this variable to `false` if you want the role to change the SELinux mode from `enforcing`<br>
to `permissive` or `disabled`, or from `permissive` to `disabled`<br>

### sap_general_preconfigure_create_directories
- _Type:_ `bool`
- _Default:_ `true`

Set to `false` if you do not want the SAP directories to be created by the role.<br>
The SAP directories will always be created if `sap_general_preconfigure_modify_selinux_labels`<br>
(see below) is set to `true`, no matter how `sap_general_preconfigure_create_directories` is set.<br>

### sap_general_preconfigure_sap_directories
- _Type:_ `list` with elements of type `str`
- _Default:_
  - /usr/sap

List of SAP directories to be created.<br>

### sap_general_preconfigure_modify_selinux_labels
- _Type:_ `bool`
- _Default:_ `true`

Set to `false` if you do not want to modify the SELinux labels for the SAP directories set<br>
in variable `sap_general_preconfigure_sap_directories`.<br>

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

### sap_general_preconfigure_hostname
- _Type:_ `str`
- _Default:_ `"{{ ansible_hostname }}"`

The hostname to be used for updating or checking `/etc/hosts` entries.<br>

### sap_general_preconfigure_domain
- _Type:_ `str`
- _Default:_ `"{{ ansible_domain }}"`

The DNS domain name to be used for updating or checking `/etc/hosts` entries.<br>
Mandatory parameter when sap_general_preconfigure_modify_etc_hosts is set to true.<br>

### sap_general_preconfigure_ip
- _Type:_ `str`
- _Default:_ `"{{ ansible_default_ipv4.address }}"`

The IPV4 address to be used for updating or checking `/etc/hosts` entries.<br>

### sap_general_preconfigure_db_group_name
- _Type:_ `str`

(RedHat specific) Use this variable to specify the name of the RHEL group which is used for the database processes.<br>
If defined, it will be used to configure process limits as per step<br>
Configuring Process Resource Limits<br>

Example:

```yaml
sap_general_preconfigure_db_group_name: dba
```
<!-- END Role Variables -->
