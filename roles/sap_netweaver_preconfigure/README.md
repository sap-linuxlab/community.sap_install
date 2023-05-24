# sap_netweaver_preconfigure Ansible Role

This role installs additional required packages and performs additional configuration steps for installing and running SAP NetWeaver.
If you want to configure a RHEL system for the installation and later usage of SAP NetWeaver, you have to first run role `sap_general_preconfigure` and then role sap_netweaver_preconfigure.  
For SLES, running the `sap_general_preconfigure` role is not necessary.

## Requirements

To use this role, your system needs to be configured with the basic requirements for SAP NetWeaver or SAP HANA. This is typically done by
running role sap_general_preconfigure (for RHEL managed nodes before RHEL 7.6, community maintained role sap-base-settings can be used).
It is also strongly recommended to run role linux-system-roles.timesync for all systems running SAP NetWeaver, to maintain an identical
system time, before or after running role sap_netweaver_preconfigure.

Note 
----
On RHEL, as per SAP notes 2002167 and 2772999, the role will switch to tuned profile sap-netweaver no matter if another tuned profile
(e.g. virtual-guest) had been active before or not.

On SLES, this role will switch the saptune solution to the one specified by the configuration and will override any previously set solution.
The default solution is `NETWEAVER`.

The role can check if enough swap space - as per the prerequisite checker in sapinst - has been configured on the managed node.
Please check the SAP NetWeaver installation guide for swap space requirements.

Do not run this role against an SAP NetWeaver or other production system. The role will enforce a certain configuration on the managed
node(s), which might not be intended.

<!-- BEGIN: Role Input Parameters -->
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

<!-- END: Role Input Parameters -->

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
