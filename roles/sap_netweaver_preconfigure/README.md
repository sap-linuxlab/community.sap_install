<!-- BEGIN Title -->
# sap_netweaver_preconfigure Ansible Role
<!-- END Title -->

## Description
<!-- BEGIN Description -->
The Ansible role `sap_netweaver_preconfigure` installs additional required packages and performs additional OS configuration steps according to applicable SAP notes for installing and running SAP ABAP Application Platform (formerly known as SAP NetWeaver) after the role [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure) has been executed.
<!-- END Description -->

<!-- BEGIN Dependencies -->
<!-- END Dependencies -->

<!-- BEGIN Prerequisites -->
## Prerequisites
Managed nodes:

- Ensure that general operating system configuration for SAP is performed by [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure). See [Recommended](#recommended) section.
<!-- END Prerequisites -->

## Execution
<!-- BEGIN Execution -->
**:warning: Do not execute this Ansible Role against existing SAP systems unless you know what you are doing and you prepare inputs to avoid unintended changes caused by default inputs.**

**NOTE: It is recommended to execute `timesync` role from Ansible Collection `fedora.linux_system_roles` before or after executing this role.**
<!-- END Execution -->

<!-- BEGIN Execution Recommended -->
### Recommended
It is recommended to execute this role together with other roles in this collection, in the following order:

1. [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure)
2. *`sap_netweaver_preconfigure`*
<!-- END Execution Recommended -->

### Execution Flow
<!-- BEGIN Execution Flow -->
1. Assert that required inputs were provided.
2. Install required packages
3. Apply configurations
    - Execute configuration tasks based on SAP Notes
    - (SUSE) Execute saptune with solution `sap_netweaver_preconfigure_saptune_solution` (Default: `NETWEAVER`)

**NOTE:** (Red Hat) Due to SAP notes 2002167, 2772999, and 3108316, the role will switch to tuned profile sap-netweaver no matter if another tuned profile (e.g. virtual-guest) had been active before or not.
<!-- END Execution Flow -->

### Example
<!-- BEGIN Execution Example -->
Example of execution together with prerequisite role [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure)
```yaml
---
- name: Ansible Play for SAP Netweaver preconfigure
  hosts: nwas_ascs, nwas_ers
  become: true
  tasks:
    - name: Execute Ansible Role sap_general_preconfigure
      ansible.builtin.include_role:
        name: community.sap_install.sap_general_preconfigure

    - name: Execute Ansible Role sap_netweaver_preconfigure
      ansible.builtin.include_role:
        name: community.sap_install.sap_netweaver_preconfigure
```
<!-- END Execution Example -->

<!-- BEGIN Role Tags -->
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

### sap_netweaver_preconfigure_packages
- _Type:_ `list` with elements of type `str`
- _Default:_ (set by platform/environment specific variables)

The list of packages to be installed for SAP NETWEAVER.<br>
The default for this variable is set in the vars file which corresponds to the detected OS version.<br>

### sap_netweaver_preconfigure_patterns
- _Type:_ `list` with elements of type `str`
- _Default:_ (set by platform/environment specific variables)

(SUSE specific) The list of the zypper patterns to install.<br>
The default for this parameter is set in the vars file which corresponds to the detected OS version.<br>

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

(SUSE specific) Specifies the saptune version.

### sap_netweaver_preconfigure_saptune_solution
- _Type:_ `str`
- _Default:_ `NETWEAVER`

(SUSE specific) Specifies the saptune solution to apply.<br>
Available values: `NETWEAVER`, `NETWEAVER+HANA`, `S4HANA-APP+DB`, `S4HANA-APPSERVER`, `S4HANA-DBSERVER`

### sap_netweaver_preconfigure_saptune_solution_force
- _Type:_ `bool`
- _Default:_ `false`

(SUSE specific) Apply saptune solution regardless if it is already enabled and verified.<br>
<!-- END Role Variables -->
