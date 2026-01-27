<!-- BEGIN Title -->
# sap_hana_preconfigure Ansible Role
<!-- END Title -->
![Ansible Lint for sap_hana_preconfigure](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_hana_preconfigure.yml/badge.svg)

## Description
<!-- BEGIN Description -->
The Ansible role `sap_hana_preconfigure` installs additional required packages and performs additional OS configuration steps according to applicable SAP notes for installing and running SAP HANA after the role [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure) has been executed.
<!-- END Description -->

<!-- BEGIN Dependencies -->
## Dependencies
- `fedora.linux_system_roles`
    - Roles:
        - `selinux`

Install required collections by `ansible-galaxy collection install -vv -r meta/collection-requirements.yml`.
<!-- END Dependencies -->

<!-- BEGIN Prerequisites -->
## Prerequisites
Managed nodes:

- Ensure that general operating system configuration for SAP is performed by [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure). See [Recommended](#recommended) section.

- (Red Hat) Ensure required repositories are available. See [Further Information Section](#red-hat-ensure-required-repositories-are-available)
<!-- END Prerequisites -->

## Execution
<!-- BEGIN Execution -->
**:warning: Do not execute this Ansible Role against existing SAP systems unless you know what you are doing and you prepare inputs to avoid unintended changes caused by default inputs.**

**NOTE: It is recommended to execute `timesync` role from Ansible Collection `fedora.linux_system_roles` before or after executing this role.**
<!-- END Execution -->

<!-- BEGIN Execution Recommended -->
### Recommended
It is recommended to execute this role together with other roles in this collection, in the following order:</br>

1. [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure)
2. *`sap_hana_preconfigure`*
<!-- END Execution Recommended -->

### Execution Flow
<!-- BEGIN Execution Flow -->
1. Assert that required inputs were provided.
2. Install required packages and patch system if `sap_hana_preconfigure_update:true`
3. Apply configurations
  - Execute configuration tasks based on SAP Notes
  - (SUSE) Execute saptune with solution `sap_hana_preconfigure_saptune_solution` (Default: `HANA`)
4. Reboot Managed nodes if packages were installed or patched and `sap_hana_preconfigure_reboot_ok: true`
<!-- END Execution Flow -->

### Example
<!-- BEGIN Execution Example -->
Example of execution together with prerequisite role [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure)
```yaml
---
- name: Ansible Play for SAP HANA HA Scale-up preconfigure
  hosts: hana_primary, hana_secondary
  become: true
  tasks:
    - name: Execute Ansible Role sap_general_preconfigure
      ansible.builtin.include_role:
        name: community.sap_install.sap_general_preconfigure

    - name: Execute Ansible Role sap_hana_preconfigure
      ansible.builtin.include_role:
        name: community.sap_install.sap_hana_preconfigure
```
<!-- END Execution Example -->

<!-- BEGIN Role Tags -->
<!-- END Role Tags -->

<!-- BEGIN Further Information -->
## Further Information
For more examples on how to use this role in different installation scenarios, refer to the [ansible.playbooks_for_sap](https://github.com/sap-linuxlab/ansible.playbooks_for_sap) playbooks.

### (Red Hat) Ensure required repositories are available

Managed nodes need to be properly registered to a repository source and have at least the following Red Hat repositories accessible:

- RHEL 7.x:
    - rhel-7-[server|for-power-le]-e4s-rpms
    - rhel-sap-hana-for-rhel-7-[server|for-power-le]-e4s-rpms

- RHEL 8.x:
    - rhel-8-for-[x86_64|ppc64le]-baseos-e4s-rpms
    - rhel-8-for-[x86_64|ppc64le]-appstream-e4s-rpms
    - rhel-8-for-[x86_64|ppc64le]-sap-solutions-e4s-rpms

- RHEL 9.x:
    - rhel-9-for-[x86_64|ppc64le]-baseos-e4s-rpms
    - rhel-9-for-[x86_64|ppc64le]-appstream-e4s-rpms
    - rhel-9-for-[x86_64|ppc64le]-sap-solutions-e4s-rpms

For details on configuring Red Hat, see the knowledge base article: [How to subscribe SAP HANA systems to the Update Services for SAP Solutions](https://access.redhat.com/solutions/3075991).<br>
If you set role parameter sap_hana_preconfigure_enable_sap_hana_repos to `yes`, the role can enable these repos.

To install HANA on Red Hat Enterprise Linux 7, 8, or 9, you need some additional packages which are contained in one of following repositories

- rhel-sap-hana-for-rhel-7-[server|for-power-le]-e4s-rpms
- rhel-8-for-[x86_64|ppc64le]-sap-solutions-e4s-rpms
- rhel-9-for-[x86_64|ppc64le]-sap-solutions-e4s-rpms

To get this repository you need to have one of the following products:

- [RHEL for SAP Solutions](https://access.redhat.com/solutions/3082481) (premium, standard)
- RHEL for Business Partner NFRs
- [RHEL Developer Subscription](https://developers.redhat.com/products/sap/download/)

To get a personal developer edition of RHEL for SAP solutions, please register as a developer and download the developer edition.

- [Registration Link](http://developers.redhat.com/register):<br>
  Here you can either register a new personal account or link it to an already existing **personal** Red Hat Network account.
- [Download Link](https://access.redhat.com/downloads/content/69/ver=/rhel---7/7.2/x86_64/product-software):<br>
  Here you can download the Installation DVD for RHEL with your previously registered account.<br>

**NOTE:** This is a regular RHEL installation DVD as RHEL for SAP Solutions is no additional<br>
product but only a special bundling. The subscription grants you access to the additional<br>
packages through our content delivery network (CDN) after installation.<br>

For supported RHEL releases [click here](https://access.redhat.com/solutions/2479121).<br>

It is also important that your disks are setup according to the [SAP storage requirements for SAP HANA](https://www.sap.com/documents/2015/03/74cdb554-5a7c-0010-8F2c7-eda71af511fa.html).<br>
This [BLOG](https://blogs.sap.com/2017/03/07/the-ultimate-guide-to-effective-sizing-of-sap-hana/) is also quite helpful when sizing HANA systems.<br>
You can use the [storage](https://galaxy.ansible.com/linux-system-roles/storage) role to automate this process.<br>

If you want to use this system in production, make sure that the time service is configured correctly.<br>
You can use [rhel-system-roles](https://access.redhat.com/articles/3050101) to automate this.<br>

**NOTE:** For finding out which SAP notes will be used by this role for Red Hat systems, please check the contents of variable `__sap_hana_preconfigure_sapnotes` in files `vars/*.yml` (choose the file which matches your OS distribution and version). 
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

Set which Ansible Collection to use for the Linux System Roles.<br>
Available values:
- `fedora.linux_system_roles` - for community/upstream.<br>
- `redhat.rhel_system_roles` - for the RHEL System Roles for SAP, or for Red Hat Automation Hub.<br>

### sap_hana_preconfigure_min_rhel_release_check
- _Type:_ `bool`
- _Default:_ `false`

(RedHat specific) Check the RHEL release against parameter `sap_hana_preconfigure_supported_rhel_minor_releases`, which is a list of<br>
known SAP HANA supported RHEL minor releases. By default, the role will display a message and continue running if<br>
the RHEL release is not part of that list. If set to `true`, the role will fail in such a case.<br>

### sap_hana_preconfigure_supported_rhel_minor_releases
- _Type:_ `list` with elements of type `str`
- _Default:_ (set by platform/environment specific variables)

(RedHat specific) Use this parameter to set your own list of SAP HANA supported RHEL minor releases.<br>

### sap_hana_preconfigure_enable_sap_hana_repos
- _Type:_ `bool`
- _Default:_ `false`

(RedHat specific) Set to 'true' to enable the SAP HANA required RHEL repos.<br>
This parameter is deprecated because the role sap_general_preconfigure can be used for this purpose.<br>
The related parameters are `sap_general_preconfigure_enable_repos` and `sap_general_preconfigure_use_hana_repos`.<br>

### sap_hana_preconfigure_req_repos_redhat_7_x86_64
- _Type:_ `list` with elements of type `str`
- _Default:_ (set by platform/environment specific variables)

(RedHat specific) Use this parameter to set your own list of SAP HANA required RHEL 7 repos on x86_64'<br>
This parameter is deprecated because the role sap_general_preconfigure can be used for this purpose.<br>
The related parameters are `sap_general_preconfigure_enable_repos` and `sap_general_preconfigure_req_repos`.<br>

### sap_hana_preconfigure_req_repos_redhat_7_ppc64le
- _Type:_ `list` with elements of type `str`
- _Default:_ (set by platform/environment specific variables)

(RedHat specific) Use this parameter to set your own list of SAP HANA required RHEL 7 repos on ppc64le'<br>
This parameter is deprecated because the role sap_general_preconfigure can be used for this purpose.<br>
The related parameters are `sap_general_preconfigure_enable_repos` and `sap_general_preconfigure_req_repos`.<br>

### sap_hana_preconfigure_req_repos_redhat_8_x86_64
- _Type:_ `list` with elements of type `str`
- _Default:_ (set by platform/environment specific variables)

(RedHat specific) Use this parameter to set your own list of SAP HANA required RHEL 8 repos on x86_64'<br>
This parameter is deprecated because the role sap_general_preconfigure can be used for this purpose.<br>
The related parameters are `sap_general_preconfigure_enable_repos` and `sap_general_preconfigure_req_repos`.<br>

### sap_hana_preconfigure_req_repos_redhat_8_ppc64le
- _Type:_ `list` with elements of type `str`
- _Default:_ (set by platform/environment specific variables)

(RedHat specific) Use this parameter to set your own list of SAP HANA required RHEL 8 repos on ppc64le'<br>
This parameter is deprecated because the role sap_general_preconfigure can be used for this purpose.<br>
The related parameters are `sap_general_preconfigure_enable_repos` and `sap_general_preconfigure_req_repos`.<br>

### sap_hana_preconfigure_req_repos_redhat_9_x86_64
- _Type:_ `list` with elements of type `str`
- _Default:_ (set by platform/environment specific variables)

(RedHat specific) Use this parameter to set your own list of SAP HANA required RHEL 9 repos on x86_64'<br>
This parameter is deprecated because the role sap_general_preconfigure can be used for this purpose.<br>
The related parameters are `sap_general_preconfigure_enable_repos` and `sap_general_preconfigure_req_repos`.<br>

### sap_hana_preconfigure_req_repos_redhat_9_ppc64le
- _Type:_ `list` with elements of type `str`
- _Default:_ (set by platform/environment specific variables)

(RedHat specific) Use this parameter to set your own list of SAP HANA required RHEL 9 repos on ppc64le'<br>
This parameter is deprecated because the role sap_general_preconfigure can be used for this purpose.<br>
The related parameters are `sap_general_preconfigure_enable_repos` and `sap_general_preconfigure_req_repos`.<br>

### sap_hana_preconfigure_set_minor_release
- _Type:_ `bool`
- _Default:_ `false`

Use this parameter to set the minor release, which is required for SAP HANA.<br>
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

The list of packages to be installed.<br>
For RHEL 8 and later, you can choose to install either the default list<br>
or a list of the minimum required packages for SAP HANA server (parameter `__sap_hana_preconfigure_packages_min_install`).<br>

### sap_hana_preconfigure_min_package_check
- _Type:_ `bool`
- _Default:_ `true`

SAP HANA requires certain minimum package versions to be supported. These minimum levels are listed in SAP Note 2235581.<br>
Set this parameter to `false` if you want to ignore these requirements.<br>

### sap_hana_preconfigure_patterns
- _Type:_ `list` with elements of type `str`
- _Default:_ (set by platform/environment specific variables)

(SUSE specific) The list of the zypper patterns to install.<br>
The default for this parameter is set in the vars file which corresponds to the detected OS version.<br>

### sap_hana_preconfigure_update
- _Type:_ `bool`
- _Default:_ `false`

Set this parameter to `true` to update the system to the latest package levels.<br>
By setting the parameter `sap_general_preconfigure_set_minor_release` of the<br>
role `sap_general_preconfigure` to `true`, you can install the most recent package updates<br>
without updating to a more recent minor release.<br>

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
- _Default:_ `'{{ ansible_interfaces | difference([''lo'']) }}'`

List of interfaces for which the tso flag will be set.<br>

### sap_hana_preconfigure_use_tuned
- _Type:_ `bool`
- _Default:_ `true`

Use tuned for configuring most of the kernel settings for SAP HANA<br>
Set this parameter to `false` to use static kernel settings<br>

### sap_hana_preconfigure_tuned_profile
- _Type:_ `str`
- _Default:_ `'sap-hana'`

(RedHat specific) Name of the SAP HANA tuned tuned profile to enable.<br>

### sap_hana_preconfigure_modify_grub_cmdline_linux
- _Type:_ `bool`
- _Default:_ `false`

Set this parameter to `true` to modify the Grub boot command line.<br>

### sap_hana_preconfigure_run_grub2_mkconfig
- _Type:_ `bool`
- _Default:_ `true`

By default, the role will run `grub2-mkconfig` to update the Grub configuration if necessary.<br>
Set this parameter to `false` if this is not desired.<br>

### sap_hana_preconfigure_thp
- _Type:_ `str`
- _Default:_ ``

Override the default setting for THP, which is determined automatically by the role, depending on the OS version.

### sap_hana_preconfigure_db_group_name
- _Type:_ `str`

(RedHat specific) Use this parameter to specify the name of the RHEL group which is used for the database processes.<br>
It will be used to configure process limits as per step "Configuring Process Resource Limits" of SAP note 2772999.<br>

Example:

```yaml
sap_hana_preconfigure_db_group_name: dba
```

### sap_hana_preconfigure_saptune_version
- _Type:_ `str`
- _Default:_ `''`

(SUSE specific) Specifies the saptune version.<br>
This will replace the current installed version if present, even downgrade if necessary.<br>

### sap_hana_preconfigure_saptune_solution
- _Type:_ `str`
- _Default:_ `'HANA'`

(SUSE specific) Specifies the saptune solution to apply.<br>
Available values: `HANA`, `NETWEAVER+HANA`, `S4HANA-APP+DB`, `S4HANA-DBSERVER`

### sap_hana_preconfigure_saptune_solution_force
- _Type:_ `bool`
- _Default:_ `false`

(SUSE specific) Apply saptune solution regardless if it is already enabled and verified.<br>

### sap_hana_preconfigure_saptune_azure
- _Type:_ `bool`
- _Default:_ `false`

(SUSE specific) On Azure, TCP timestamps, reuse and recycle should be disabled.<br>
If the variable is set, an override file for saptune will be created (/etc/saptune/override/2382421) to set net.ipv4.tcp_timestamps and net.ipv4.tcp_tw_reuse to 0.<br>
Set this parameter to `true` on Azure.<br>
<!-- END Role Variables -->
