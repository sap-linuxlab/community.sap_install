# sap_netweaver_preconfigure Ansible Role

This role installs additional required packages and performs additional configuration steps for installing and running SAP NetWeaver.
If you want to configure a RHEL system for the installation and later usage of SAP NetWeaver, you have to first run role sap_general_preconfigure
and then role sap_netweaver_preconfigure.

## Requirements

To use this role, your system needs to be configured with the basic requirements for SAP NetWeaver or SAP HANA. This is typically done by
running role sap_general_preconfigure (for RHEL managed nodes before RHEL 7.6, community maintained role sap-base-settings can be used).
It is also strongly recommended to run role linux-system-roles.timesync for all systems running SAP NetWeaver, to maintain an identical system time,
before or after running role sap_netweaver_preconfigure.

Note
----
As per SAP notes 2002167 and 2772999, the role will switch to tuned profile sap-netweaver no matter if another tuned profile
(e.g. virtual-guest) had been active before or not.

The role can check if enough swap space - as per the prerequisite checker in sapinst - has been configured on the managed node.
Please check the SAP NetWeaver installation guide for swap space requirements.

Do not run this role against an SAP NetWeaver or other production system. The role will enforce a certain configuration on the managed
node(s), which might not be intended.

## Role Variables

### Execute only certain steps of SAP notes
If the following variable is set to `no`, only the installation or configuration steps of SAP notes will be executed or checked. If this variable is undefined or set to `yes`, all installation and configuration steps of applicable SAP notes will be executed.
```yaml
sap_netweaver_preconfigure_config_all
```

### Perform installation or configuration steps, or both
If you have set `sap_netweaver_preconfigure_config_all` (see above) to `no`, you can limit the scope of the role to only execute the installation or the configuration steps. For this purpose, set one of the following variables, or both, to `yes`. The default for both is `no`.
```yaml
sap_netweaver_preconfigure_installation
sap_netweaver_preconfigure_configuration
```

### Install required packages for Adobe Document Services
If the following variable is set to `yes`, required packages for Adobe Document Services according to SAP note 2135057 (RHEL 7) or 2920407 (RHEL 8) will be installed. Default is `no`.
```yaml
sap_netweaver_preconfigure_use_adobe_doc_services
```

### Run the role in assert mode
If the following variable is set to `yes`, the role will only check if the configuration of the managed node(s) is according to the applicable SAP notes. Default is `no`.
```yaml
sap_netweaver_preconfigure_assert
```

### Behavior of the role in assert mode
If the role is run in assert mode (see above) and the following variable is set to `yes`, assertion errors will not cause the role to fail. This can be useful for creating reports.
Default is `no`, meaning that the role will fail for any assertion error which is discovered. This variable has no meaning if the role is not run in assert mode.
```yaml
sap_netweaver_preconfigure_assert_ignore_errors
```

### Swap space for SAP NetWeaver
When installing SAP NetWeaver, the prerequisite checker verifies if enough swap space is configured. By default, the role checks is there is at least 20480 MB of swap space available.
This variable can be used set to the swap space limit to any other value.
```yaml
sap_netweaver_preconfigure_min_swap_space_mb
```

### Fail if there is less than 20480 MB of swap space configured
If the following variable is set to `no`, the role will not fail if less than 20480 MB of swap space is configured. Default is `yes`.
```yaml
sap_netweaver_preconfigure_fail_if_not_enough_swap_space_configured
```

## Example Playbook

Simple playbook, named sap+netweaver.yml:
```yaml
---
- hosts: all
  roles:
    - role: sap_general_preconfigure
    - role: sap_netweaver_preconfigure
```

Simple playbook for an extended check (assert) run, named sap+netweaver-assert.yml:
```yaml
---
- hosts: all
  vars:
    sap_preconfigure_assert: yes
    sap_preconfigure_assert_ignore_errors: yes
    sap_netweaver_preconfigure_assert: yes
    sap_netweaver_preconfigure_assert_ignore_errors: yes
  roles:
    - role: sap_general_preconfigure
    - role: sap_netweaver_preconfigure
```

## Example Usage
Normal run, for configuring server host_1 for SAP NetWeaver:
```yaml
ansible-playbook sap+netweaver.yml -l host_1
```

Extended Check (assert) run, not aborting if an error has been found:
```yaml
ansible-playbook sap+netweaver-assert.yml -l host_1
```

Same as above, with a nice compact and colored output, this time for two hosts:
```yaml
ansible-playbook sap+netweaver-assert.yml -l host_1,host_2 |
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

Red Hat for SAP Community of Practice, Bernd Finger, Rainer Leber
