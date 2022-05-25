# sap_hana_preconfigure Ansible Role

This role installs additional required packages and performs additional configuration steps for installing and running SAP HANA.
If you want to configure a RHEL system for the installation and later usage of SAP HANA, you have to first run role sap_general_preconfigure
and then role sap_hana_preconfigure.

## Requirements

To use this role, your system needs to be configured with the basic requirements for SAP NetWeaver or SAP HANA. This is typically done by running
role sap_general_preconfigure (for RHEL managed nodes before RHEL 7.6, community maintained role sap-base-settings can be used).
It is also strongly recommended to run role linux-system-roles.timesync for all systems running SAP HANA, to maintain an identical system time,
before or after running role sap_hana_preconfigure.

Managed nodes need to be properly registered to a repository source and have at least the following Red Hat repositories accessable (see also example playbook):

for RHEL 7.x:
- rhel-7-[server|for-power-le]-e4s-rpms
- rhel-sap-hana-for-rhel-7-[server|for-power-le]-e4s-rpms

for RHEL 8.x:
- rhel-8-for-[x86_64|ppc64le]-baseos-e4s-rpms
- rhel-8-for-[x86_64|ppc64le]-appstream-e4s-rpms
- rhel-8-for-[x86_64|ppc64le]-sap-solutions-e4s-rpms

For details, see the Red Hat knowledge base article: [How to subscribe SAP HANA systems to the Update Services for SAP Solutions](https://access.redhat.com/solutions/3075991)). If you set role parameter sap_hana_preconfigure_enable_sap_hana_repos to `yes`, the role can enable these repos.

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

It is also important that your disks are setup according to the [SAP storage requirements for SAP HANA](https://www.sap.com/documents/2015/03/74cdb554-5a7c-0010-8F2c7-eda71af511fa.html). This [BLOG](https://blogs.sap.com/2017/03/07/the-ultimate-guide-to-effective-sizing-of-sap-hana/) is also quite helpful when sizing HANA systems.
You can use the [storage](https://galaxy.ansible.com/linux-system-roles/storage) role to automate this process

If you want to use this system in production, make sure that the time service is configured correctly. You can use [rhel-system-roles](https://access.redhat.com/articles/3050101) to automate this.

Note
----
For finding out which SAP notes will be used by this role, please check the contents of variable `__sap_hana_preconfigure_sapnotes` in files `vars/*.yml` (choose the file which matches your OS distribution and version).

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

2) Previous versions of this role used variable sap_hana_preconfigure_selinux_state to set the SELinux state to disabled, which is mentioned in
SAP notes 2292690 (RHEL 7) and 2777782 (RHEL 8). As role sap_general_preconfigure already allows to specify the desired SELinux state, and as
sap_general_preconfigure is run before sap_hana_preconfigure, there is no need any more to let sap_hana_preconfigure configure the SELinux state.
Same applies to the assertion of the SELinux state. Because of this, variable sap_hana_preconfigure_selinux_state has been removed from this role and
tasks 2292690/08-disable-selinux.yml and 2777782/01-assert-selinux.yml have been commented out.

## Role Variables

- set in `defaults/main.yml`:

### Execute only certain steps of SAP notes
If the following variable is set to `no`, only certain steps of SAP notes will be executed or checked as per setting of variable `sap_hana_preconfigure_<sap_note_number>_<step>`. If this variable is undefined or set to `yes`, all installation and configuration steps of applicable SAP notes will be executed.
```yaml
sap_hana_preconfigure_config_all
```

### Perform installation or configuration steps, or both
If you have set `sap_hana_preconfigure_config_all` (see above) to `no`, you can limit the scope of the role to only execute the installation or the configuration steps. For this purpose, set one of the following variables, or both, to `yes`. The default for both is `no`.
```yaml
sap_hana_preconfigure_installation
sap_hana_preconfigure_configuration
```

### Define configuration steps of SAP notes
For defining one or more configuration steps of SAP notes to be executed or checked only, set variable `sap_hana_preconfigure_config_all` to `no`, `sap_hana_preconfigure_configuration` to `yes`, and one or more of the following variables to `yes`:
```yaml
sap_hana_preconfigure_2777782_[02...10], example: sap_hana_preconfigure_2777782_05
sap_hana_preconfigure_2292690_[01...07,09,10], example: sap_hana_preconfigure_2292690_02
sap_hana_preconfigure_2009879_3_9
sap_hana_preconfigure_2009879_3_14_[1...4]
sap_hana_preconfigure_2009879_3_15
sap_hana_preconfigure_2382421
sap_hana_preconfigure_3024346
```

### Run the role in assert mode
If the following variable is set to `yes`, the role will only check if the configuration of the managed node(s) is according to the applicable SAP notes. Default is `no`.
```yaml
sap_hana_preconfigure_assert
```

### Behavior of the role in assert mode
If the role is run in assert mode (see above) and the following variable is set to `yes`, assertion errors will not cause the role to fail. This can be useful for creating reports.
Default is `no`, meaning that the role will fail for any assertion error which is discovered. This variable has no meaning if the role is not run in assert mode.
```yaml
sap_hana_preconfigure_assert_ignore_errors
```

### Perform all configuration checks in assert mode
If the following variable is set to `yes`, if the role is configured with variable `sap_hana_preconfigure_assert` being set to `yes`, the role will check all configuration steps
no matter of the setting of the tuned and grub variables. Default is `no`, meaning that only those configuration steps are checked which are enabled by the tuned and grub variables.
Example: If variable `sap_hana_preconfigure_modify_grub_cmdline_linux` is set to `no`, when running the role in assert mode, the role will not check if the grub command line
has been modified according to this role.
```yaml
sap_hana_preconfigure_assert_all_config
```

### Perform a RHEL minor release check for SAP HANA
If the following variable is set to `no`, the role will install packages and modify settings on the managed node even if the RHEL release is not contained in the list of
supported RHEL releases. Default is `yes`. In assert mode (`sap_hana_preconfigure_assert` = `yes`), the role will always perform the RHEL release check but will
display display "WARN" or "INFO" if the variable is set to `no`, instead of the default "FAIL" or "PASS".
```yaml
sap_hana_preconfigure_min_rhel_release_check
```

### Override the supported RHEL minor release list for SAP HANA
If you want to provide you own list of supported RHEL releases (e.g. for testing), override the variable. Otherwise, the defaults as set in vars/RedHat_*.yml will be used.
```yaml
sap_hana_preconfigure_supported_rhel_minor_releases
```

### Repo checking and enabling
If you want the role to check and if necessary enable SAP HANA repos, set the following variable to `yes`. Default is `no`.
```yaml
sap_hana_preconfigure_enable_sap_hana_repos
```

### Override default repo list(s)
If you want to provide you own list(s) of repositories for checking and enabling, override one or more of the following variables. Otherwise, the defaults as set in vars/RedHat_*.yml will be used.
```yaml
sap_hana_preconfigure_req_repos_RedHat_7_x86_64
sap_hana_preconfigure_req_repos_RedHat_7_ppc64le
sap_hana_preconfigure_req_repos_RedHat_8_x86_64
sap_hana_preconfigure_req_repos_RedHat_8_ppc64le
```

### Set the RHEL release to a certain fixed minor release
If you want the role to set the RHEL release to a certain fixed minor release (according to installed RHEL release), set the following variable to `yes`. Default is `no`.
```yaml
sap_hana_preconfigure_set_minor_release
```

### Minimum package check
The following variable will make sure packages are installed at minimum required versions as defined in files `vars/*.yml`. Default is `yes`.
```yaml
sap_hana_preconfigure_min_package_check
```

### Perform a yum update
If the following variable is set to `yes`, the role will run a `yum update` before performing configuration changes. Default is `no`. \
*Note*: The outcome of a `yum update` depends on the managed node's configuration for sticky OS minor version, see the description of the release option in `man subscription-manager`. For SAP HANA installations, setting a certain minor version with `subscription-manager release --set=X.Y` is a strict requirement.
```yaml
sap_hana_preconfigure_update
```

###  HANA kernel parameters
[SAP Note 238241](https://launchpad.support.sap.com/#/notes/238241) defines kernel parameters that all Linux systems need to set.
The default parameter recomendations are dependent on the OS release. Hence the OS dependant default setting is defined in
./vars/{{ansible_os_release}}.yml. If you need to add or change parameters for your system, copy these parameters from the vars file
into the variable sap_hana_preconfigure_kernel_parameters and add or change your settings, as in the following example:

```yaml
sap_hana_preconfigure_kernel_parameters:
  - { name: net.core.somaxconn, value: 4096 }
  - { name: net.ipv4.tcp_max_syn_backlog, value: 8192 }
  - { name: net.ipv4.tcp_timestamps, value: 1 }
  - { name: net.ipv4.tcp_slow_start_after_idle, value: 0 }
```

###  HANA kernel parameters for IBM POWER servers
[SAP Note 2055470](https://launchpad.support.sap.com/#/notes/2055470) contains links to IBM documents for SAP HANA on POWER.
Among these is a document which contains certain recommended Linux kernel settings for SAP HANA on POWER:
Network_Configuration_for_HANA_Workloads_on_IBM_Power_Servers_V7.1.pdf.
This document is linked from SAP note 2055470 via "SAP HANA on IBM Power Systems and IBM System Storage - Guides", then via
"SAP on Linux and IBM Storage Guides (incl. HANA)", and then via
"SAP on Power Linux Network and Fibre Channel Guides".
The default parameter recommendations are defined in ./vars/{{ansible_os_release}}.yml. If you need to add or change parameters
for your system, copy these parameters from the vars file into the variable sap_hana_preconfigure_kernel_parameters_ppc64le and
add or change your settings, similar to the previous example.

###  HANA kernel parameters for NetApp NFS
[SAP Note 3024346](https://launchpad.support.sap.com/#/notes/3024346) defines kernel parameter settings for NetApp NFS.
In case you want the role to set or check these parameters, set the following variable to `yes`. Default is `no`.

```yaml
sap_hana_preconfigure_use_netapp_settings_nfs
```

###  HANA kernel parameters for NetApp NFSv3
[SAP Note 3024346](https://launchpad.support.sap.com/#/notes/3024346) also contains an additional parameter setting for NetApp when using NFSv3.
In case you want the role to set or check this parameter, set the following variable to `yes`. Default is `no`.

```yaml
sap_hana_preconfigure_use_netapp_settings_nfsv3
```

### Add the repository for IBM service and productivity tools for POWER (ppc64le only)
In case you do *not* want to automatically add the repository for the IBM service and productivity tools, set the following variable to `no`. Default is `yes`, meaning that the role will download and install the package specified in variable sap_hana_preconfigure_ibm_power_repo_url (see below) and also run the command /opt/ibm/lop/configure to accept the license.
```yaml
sap_hana_preconfigure_add_ibm_power_repo
```

### URL for IBM service and productivity tools for POWER (ppc64le only)
The following variable is set to the location of package ibm-power-repo-lastest.noarch.rpm or a package with similar contents, as defined by variable __sap_hana_preconfigure_ibm_power_repo_url in vars/RedHat_7.yml and vars/RedHat_8.yml.
You can replace it by your own URL by setting this variable to a different URL.
```yaml
sap_hana_preconfigure_ibm_power_repo_url
```

### Reboot the system if required
If the following variable is set to `yes`, the role will reboot the managed node if required. The default is `no`, in which case the role will only report that a reboot is required.
```yaml
sap_hana_preconfigure_reboot_ok
```

### How to behave if a reboot is required
In case `sap_hana_preconfigure_reboot_ok` (see above) is set to `no`, we should make sure that a reboot requirement does not remain unnoticed.
The following variable will cause the role to fail if a reboot is required, if undefined or set to `yes`, which is also the default.
By setting the variable to `no`, the role will not fail if a reboot is required but just print a warning message.
```yaml
sap_hana_preconfigure_fail_if_reboot_required
```

### Use tuned profile sap-hana
By default, the role will activate tuned profile `sap-hana` for configuring kernel parameters (where possible). If you do not want
to use the tuned profile sap-hana, set the following variable to `no`. In this case, the role will also modify GRUB_CMDLINE_LINUX,
no matter how variable `sap_hana_preconfigure_modify_grub_cmdline_linux` (see below) is set.
Note: If this variable is set to `yes`, the role may still modify GRUB_CMDLINE_LINUX in /etc/default/grub, by setting variable
`sap_hana_preconfigure_modify_grub_cmdline_linux` to `yes`. This provides more flexibility for setting certain kernel parameters.
```yaml
sap_hana_preconfigure_use_tuned
```

### Specify your own tuned profile
Use the following variable to set a tuned profile string other than the default `sap-hana`. The tuned profile must reside in directory
`/etc/tuned/my_own_profile`, as file named `tuned.conf` (example for a tuned profile named `my_own_profile`).
```yaml
sap_hana_preconfigure_tuned_profile
```

### Modify grub2 line GRUB_CMDLINE_LINUX
If you want to modify the grub2 line GRUB_CMDLINE_LINUX in /etc/default/grub, set the following variable to `yes`. The default is `no`. Setting this variable to `yes` probably only makes sense if `sap_hana_preconfigure_run_grub2_mkconfig` (see below) is also set to `yes`.
Note: If variable sap_hana_preconfigure_use_tuned (see above) is set to `no`, GRUB_CMDLINE_LINUX will modified in any case, no matter how variable `sap_hana_preconfigure_modify_grub_cmdline_linux` is set. This is to guarantee that either the tuned settings or the static settings will be applied. If variable sap_hana_preconfigure_use_tuned (see above) is set to `yes`, `sap_hana_preconfigure_modify_grub_cmdline_linux` can still be set to `yes` for modifying GRUB_CMDLINE_LINUX, providing more flexibility for setting certain kernel parameters.
```yaml
sap_hana_preconfigure_modify_grub_cmdline_linux
```

### Run grub2-mkconfig
If you do not want to run grub2-mkconfig to regenerate the grub2 config file after a change to /etc/default/grub (see the desciption of the two previous parameters), set the following variable to `no`. The default is `yes`.
```yaml
sap_hana_preconfigure_run_grub2_mkconfig
```

### HANA Major and minor version
These variables are used in all sap-hana roles so that they are only prefixed with `sap-hana`. If you use `sap-hana-mediacheck` role, these variables are read in automatically. The variable is used in the checks for [SAP Note 2235581](https://launchpad.support.sap.com/#/notes/2235581).

```yaml
sap_hana_version: "2"
sap_hana_sps: "0"
```

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
