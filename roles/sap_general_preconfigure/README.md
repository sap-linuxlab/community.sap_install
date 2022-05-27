# sap_general_preconfigure Ansible Role

This role installs required packages and performs configuration steps which are required for installing and running SAP NetWeaver or SAP HANA. Specific installation and configuration steps on top of these basic steps are performed with roles sap-netweaver-preconfigure and sap-hana-preconfigure. Future implementations may reduce the scope of this role, for example if certain installation or configuration steps are done in the more specific roles.

## Requirements

To use this role, your system needs to be installed according to:
- RHEL 7: SAP note 2002167, Red Hat Enterprise Linux 7.x: Installation and Upgrade, section "Installing Red Hat Enterprise Linux 7"
- RHEL 8: SAP note 2772999, Red Hat Enterprise Linux 8.x: Installation and Configuration, section "Installing Red Hat Enterprise Linux 8".

Note
----
Do not run this role against an SAP or other production system. The role will enforce a certain configuration on the managed node(s), which might not be intended.

## Role Variables

- set in `defaults/main.yml`:

### Execute only certain steps of SAP notes
If the following variable is set to `no`, only certain steps of SAP notes will be executed or checked as per setting of variable `sap_general_preconfigure_<sap_note_number>_<step>`. If this variable is undefined or set to `yes`, all installation and configuration steps of applicable SAP notes will be executed.
```yaml
sap_general_preconfigure_config_all
```

### Perform installation or configuration steps, or both
If you have set `sap_general_preconfigure_config_all` (see above) to `no`, you can limit the scope of the role to only execute the installation or the configuration steps. For this purpose, set one of the following variables, or both, to `yes`. The default for both is `no`.
```yaml
sap_general_preconfigure_installation
sap_general_preconfigure_configuration
```

### Define configuration steps of SAP notes
For defining one or more configuration steps of SAP notes to be executed or checked only, set variable `sap_general_preconfigure_config_all` to `no`, `sap_general_preconfigure_configuration` to `yes`, and one or more of the following variables to `yes`:
```yaml
sap_general_preconfigure_2002167_0[2...6], example: sap_general_preconfigure_2002167_03
sap_general_preconfigure_1391070
sap_general_preconfigure_0941735
sap_general_preconfigure_2772999_[02...10], example: sap_general_preconfigure_2772999_10
```

### Run the role in assert mode
If the following variable is set to `yes`, the role will only check if the configuration of the managed node(s) is according to the applicable SAP notes. Default is `no`.
```yaml
sap_general_preconfigure_assert
```

### Behavior of the role in assert mode
If the role is run in assert mode (see above) and the following variable is set to `yes`, assertion errors will not cause the role to fail. This can be useful for creating reports.
Default is `no`, meaning that the role will fail for any assertion error which is discovered. This variable has no meaning if the role is not run in assert mode.
```yaml
sap_general_preconfigure_assert_ignore_errors
```

### (RHEL only): Enable repos
If the following variable is set to `yes`, the role will enable all repos as per definitions below. Default is `no`.
```yaml
sap_general_preconfigure_enable_repos
```

### (RHEL only): Use SAP NetWeaver repo
If the following variable is set to `no`, the role will not enable the SAP NetWeaver(s) repo if variable
`sap_general_preconfigure_enable_repos` is set to `yes`. Default is `yes`.
```yaml
sap_general_preconfigure_use_netweaver_repos
```

### (RHEL only): Enable SAP HANA repo
If the following variable is set to `no`, the role will not enable the SAP HANA repo(s) if variable
`sap_general_preconfigure_enable_repos` is set to `yes`. Default is `yes`.
```yaml
sap_general_preconfigure_use_hana_repos
```

### (RHEL only): Enable HA repo
If the following variable is set to `no`, the role will not enable the high availability repo(s) if variable
`sap_general_preconfigure_enable_repos` is set to `yes`. Default is `yes`.
```yaml
sap_general_preconfigure_use_ha_repos
```

### (RHEL only): Disable all other repos
Set the following variable to `no` to leave all currently enabled repos enabled. The default is `yes`, which means
that the subscription-manager command will disable all repos before enabling the desired ones.
```yaml
sap_general_preconfigure_disable_all_other_repos
```

### (RHEL only): Provide your own list of repos to enable
If you want to provide your own list of repos (e.g. on cloud systems), set the following variable accordingly.
Otherwise, the RHEL default repo names with the maximum support duration for the RHEL minor release are chosen automatically
(e.g. normal repos for RHEL 8.3, e4s repos for RHEL 8.4).
```yaml
sap_general_preconfigure_req_repos
```

### (RHEL only): Set the minor release lock
Set to `yes` if you want the role to set the RHEL minor release, which is a requirement for SAP HANA. Default is `no`.
Note: If you set the RHEL minor release lock, then it is strongly recommended to also set variable
`sap_general_preconfigure_repo_type` (see below) to `e4s`.
```yaml
sap_general_preconfigure_set_minor_release
```

### Minimum package check
The following variable will make sure packages are installed at minimum required versions as defined in files `vars/*.yml`. Default is `yes`.
```yaml
sap_general_preconfigure_min_package_check
```

### Perform a yum update
If the following variable is set to `yes`, the role will run a `yum update` before performing configuration changes. Default is `no`. \
*Note*: The outcome of a `yum update` depends on the managed node's configuration for sticky OS minor version, see the description of the release option in `man subscription-manager`. For SAP HANA installations, setting a certain minor version with `subscscription-manager release --set=X.Y` is a strict requirement.
```yaml
sap_general_preconfigure_update
```

### Reboot the system if required
If the following variable is set to `yes`, the role will reboot the managed node if required. The default is `no`, in which case the role will only report that a reboot is required.
```yaml
sap_general_preconfigure_reboot_ok
```

### How to behave if a reboot is required
In case `sap_general_preconfigure_reboot_ok` (see above) is set to `no`, we should make sure that a reboot requirement does not remain unnoticed.
The following variable will cause the role to fail if a reboot is required, if undefined or set to `yes`, which is also the default. 
By setting the variable to `no`, the role will not fail if a reboot is required but just print a warning message.
```yaml
sap_general_preconfigure_fail_if_reboot_required
```

### Define SELinux state
The following variable allows for defining the desired SELinux state. Default is `disabled`.
```yaml
sap_general_preconfigure_selinux_state
```

### Size of TMPFS in GB:
The following variable contains a formula for setting the size of TMPFS according to SAP note 941735. You can modify the formula or replace it by a static value if needed.
```yaml
sap_general_preconfigure_size_of_tmpfs_gb
```

### Locale
The following variable contains the locale to be check. This check is currently not implemented.
```yaml
sap_general_preconfigure_locale
```

### Modify /etc/hosts
If you not want the role to check and if necessary modify `/etc/hosts` according to SAP's requirements, set the following variable to `no`. Default is `yes`.
```yaml
sap_general_preconfigure_modify_etc_hosts
```

### Maximum length of the hostname
The role will fail if the hostname has more than 13 characters (defined in vars/main.yml), to catch such cases before attempting to install SAP software.
There might be cases where other limits are desired (e.g. just 8 characters). In this case, set the following variable according to your needs (e.g. '8').
See also SAP note 611361.
```yaml
sap_general_preconfigure_max_hostname_length
```

### hostname
If the role should not use the hostname as reported by Ansible (=`ansible_hostname`), set the following variable according to your needs:
```yaml
sap_hostname
```

### DNS domain name
If the role should not use the DNS domain name as reported by Ansible (=`ansible_domain`), set the following variable according to your needs:
```yaml
sap_domain
```

### IP address
If the role should not use the primary IP address as reported by Ansible (=`ansible_default_ipv4.address`), set the following variable according to your needs:
```yaml
sap_ip
```

### Linux group name of the database user
The following variable contains the name of the group which is used for the database(s), e.g. 'dba'.
```yaml
sap_general_preconfigure_db_group_name
```

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
