<!-- BEGIN Title -->
# sap_netweaver_preconfigure Ansible Role
<!-- END Title -->

## Description
<!-- BEGIN Description -->
Ansible Role `sap_netweaver_preconfigure` is used to ensure that Managed nodes are configured to host SAP Netweaver systems according to SAP Notes after [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure) role was executed.

This role performs installation of required packages for running SAP Netweaver systems and configuration of Operating system parameters.
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

Role can be executed independently or as part of [ansible.playbooks_for_sap](https://github.com/sap-linuxlab/ansible.playbooks_for_sap) playbooks.
<!-- END Execution -->

<!-- BEGIN Execution Recommended -->
### Recommended
It is recommended to execute this role together with other roles in this collection, in the following order:</br>
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

**Note: (Red Hat) Due to SAP notes 2002167, 2772999, and 3108316, the role will switch to tuned profile sap-netweaver no matter if another tuned profile (e.g. virtual-guest) had been active before or not.**
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
<!-- END Further Information -->

## License
<!-- BEGIN License -->
Apache 2.0
<!-- END License -->

## Maintainers
<!-- BEGIN Maintainers -->
- [Bernd Finger](https://github.com/berndfinger)
<!-- END Maintainers -->

## Role Input Parameters
All input parameters used by role are described in [INPUT_PARAMETERS.md](https://github.com/sap-linuxlab/community.sap_install/blob/main/roles/sap_netweaver_preconfigure/INPUT_PARAMETERS.md)
