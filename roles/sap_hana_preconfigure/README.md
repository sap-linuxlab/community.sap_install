# sap_hana_preconfigure Ansible Role

This role installs additional required packages and performs additional configuration steps for installing and running SAP HANA.
If you want to configure a RHEL system for the installation and later usage of SAP HANA, you have to first run role sap_general_preconfigure
and then role sap_hana_preconfigure.  However, if we wish to run SLES for HANA, you may run only this role.

## Requirements

The role requires additional collections which are specified in `meta/collection-requirements.yml`. Before using this role,
make sure that the required collections are installed, for example by using the following command:

`ansible-galaxy install -vv -r meta/collection-requirements.yml`

To use this role, your system needs to be configured with the basic requirements for SAP NetWeaver or SAP HANA. This is typically done by running role sap_general_preconfigure (for RHEL managed nodes before RHEL 7.6, community maintained role sap-base-settings can be used).

It is also strongly recommended to run role linux-system-roles.timesync for all systems running SAP HANA, to maintain an identical system time, before or after running role sap_hana_preconfigure.

Managed nodes need to be properly registered to a repository source and have at least the following Red Hat repositories accessible (see also example playbook):

for RHEL 7.x:
- rhel-7-[server|for-power-le]-e4s-rpms
- rhel-sap-hana-for-rhel-7-[server|for-power-le]-e4s-rpms

for RHEL 8.x:
- rhel-8-for-[x86_64|ppc64le]-baseos-e4s-rpms
- rhel-8-for-[x86_64|ppc64le]-appstream-e4s-rpms
- rhel-8-for-[x86_64|ppc64le]-sap-solutions-e4s-rpms

for SLES 15.x:
- SLE-Module-SAP-Applications15-[SP number]-Pool 
- SLE-Module-SAP-Applications15-[SP number]-Updates
- SLE-Product-SLES_SAP15-[SP number]-Pool
- SLE-Product-SLES_SAP15-[SP number]-Updates

For details on configuring Red Hat, see the knowledge base article: [How to subscribe SAP HANA systems to the Update Services for SAP Solutions](https://access.redhat.com/solutions/3075991)). If you set role parameter sap_hana_preconfigure_enable_sap_hana_repos to `yes`, the role can enable these repos.

To install HANA on Red Hat Enterprise Linux 6, 7, or 8, you need some additional packages which are contained in the rhel-sap-hana-for-rhel-7-[server|for-power-le]-e4s-rpms or rhel-8-for-[x86_64|ppc64le]-sap-solutions-e4s-rpms repo.

To get this repository you need to have one of the following products:

- [RHEL for SAP Solutions](https://access.redhat.com/solutions/3082481) (premium, standard)
- RHEL for Business Partner NFRs
- [RHEL Developer Subscription](https://developers.redhat.com/products/sap/download/)

To get a personal developer edition of RHEL for SAP solutions, please register as a developer and download the developer edition.

- [Registration Link](http://developers.redhat.com/register) :
  Here you can either register a new personal account or link it to an already existing
  **personal** Red Hat Network account.
- [Download Link](https://access.redhat.com/downloads/content/69/ver=/rhel---7/7.2/x86_64/product-software):
  Here you can download the Installation DVD for RHEL with your previously registered
  account

*NOTE:* This is a regular RHEL installation DVD as RHEL for SAP Solutions is no additional
 product but only a special bundling. The subscription grants you access to the additional
 packages through our content delivery network (CDN) after installation.

For supported RHEL releases [click here](https://access.redhat.com/solutions/2479121).

Details on configuring SLES repositories can be found on the following articles for [on-premise systems](https://www.suse.com/support/kb/doc/?id=000018564) or [BYOS cloud images](https://www.suse.com/c/byos-instances-and-the-suse-public-cloud-update-infrastructure/)


It is also important that your disks are setup according to the [SAP storage requirements for SAP HANA](https://www.sap.com/documents/2015/03/74cdb554-5a7c-0010-8F2c7-eda71af511fa.html). This [BLOG](https://blogs.sap.com/2017/03/07/the-ultimate-guide-to-effective-sizing-of-sap-hana/) is also quite helpful when sizing HANA systems.
You can use the [storage](https://galaxy.ansible.com/linux-system-roles/storage) role to automate this process

If you want to use this system in production, make sure that the time service is configured correctly. You can use [rhel-system-roles](https://access.redhat.com/articles/3050101) to automate this.

Note
----
For finding out which SAP notes will be used by this role for Red Hat systems, please check the contents of variable `__sap_hana_preconfigure_sapnotes` in files `vars/*.yml` (choose the file which matches your OS distribution and version).  

For SLES, notes are applied using the saptune service.  Saptune supports a number of solutions.  A solution implements several SAP notes.  The default solution for this role is 'HANA'.  To see a list of supported solutions and the notes that they implement, you can run `saptune solution list` on the command line.

Do not run this role against an SAP HANA or other production system. The role will enforce a certain configuration on the managed node(s), which might not be intended.

Changes
-------
1) Previous versions of this role used variable sap_hana_preconfigure_use_tuned_where_possible to switch between either tuned settings or kernel command line settings (where applicable).
The current version modifies this behavior:
- The variable sap_hana_preconfigure_use_tuned_where_possible has been renamed to sap_hana_preconfigure_use_tuned
- The variable sap_hana_preconfigure_switch_to_tuned_profile_sap_hana has been removed.
- If sap_hana_preconfigure_use_tuned is set to `yes`, which is also the default, the role will configure the system for using tuned and also switch to tuned profile sap-hana.
  If sap_hana_preconfigure_use_tuned is set to `no`, the role will perform a static configuration, including the modification of the linux command line in grub.
- The role can use tuned, or configure the kernel command line, or both.

2) Previous versions of this role used variable sap_hana_preconfigure_selinux_state to set the SELinux state to disabled, which is
mentioned in SAP notes 2292690 (RHEL 7) and 2777782 (RHEL 8). As role sap_general_preconfigure already allows to specify the desired
SELinux state, and as sap_general_preconfigure is run before sap_hana_preconfigure, there is no need any more to let
sap_hana_preconfigure configure the SELinux state. Same applies to the assertion of the SELinux state.

3) SLES systems are now configured using saptune rather than the ansible implementation of the notes.

<!-- BEGIN: Role Input Parameters for sap_hana_preconfigure -->
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
- _Default:_ `true`

Check the RHEL release against a predefined list of known SAP HANA supported RHEL minor releases.<br>
If this parameter is set to `false`, the role will *not* perform this check.<br>

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

### sap_hana_preconfigure_use_netapp_settings_nfsv3
- _Type:_ `bool`
- _Default:_ `false`

If `sap_hana_preconfigure_use_netapp_settings_nfs` is set to `true` and NFS Version 3 is to be used,<br>
this parameter must be set to `true` as well.<br>

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
- _Default:_ `'3.0.2'`

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
Set this parameter to `true` on Azure.<br>

<!-- END: Role Input Parameters for sap_hana_preconfigure -->

## Example Playbook

Simple playbook, named sap+hana.yml:
```yaml
---
- hosts: all
  roles:
    - role: sap_general_preconfigure
    - role: sap_hana_preconfigure
```

Simple playbook for an extended check (assert) run, named sap+hana-assert.yml:
```yaml
---
- hosts: all
  vars:
    sap_general_preconfigure_assert: yes
    sap_general_preconfigure_assert_ignore_errors: yes
    sap_hana_preconfigure_assert: yes
    sap_hana_preconfigure_assert_ignore_errors: yes
  roles:
    - role: sap_general_preconfigure
    - role: sap_hana_preconfigure
```

## Example Usage

Normal run, for configuring server host_1 for SAP HANA:
```yaml
ansible-playbook sap+hana.yml -l host_1
```

Extended Check (assert) run, not aborting if an error has been found:
```yaml
ansible-playbook sap+hana-assert.yml -l host_1
```

Same as above, with a nice compact and colored output, this time for two hosts:
```yaml
ansible-playbook sap+hana-assert.yml -l host_1,host_2 |
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

## Contribution

Please read the [developer guidelines](./README.DEV.md) if you want to contribute

## License

Apache license 2.0

## Author Information

Red Hat for SAP Community of Practice, Markus Koch, Thomas Bludau, Bernd Finger, Than Ngo, Rainer Leber
