# Documentation of community.sap_install Ansible Collection

## Introduction

The `sap_install` Ansible Collection provides a variety of automated tasks for the configuration and installation of SAP Software.

Each Ansible Role contained within this Ansible Collection, performs a distinct set of tasks and are designed to be run independently or cohesively - depending on the outcome desired by an end-user.


## Functionality

This Ansible Collection executes various SAP Software installations for different SAP solution scenarios. The code structure and logic has been separated to support a flexible execution of different steps for various scenarios.

Any Ansible Roles labelled "preconfigure" and "prepare" are prerequisites, executed before the corresponding installation Ansible Roles (such as `sap_hana_install` or `sap_swpm`).

At a high-level, the key installation functionality of this Ansible Collection includes:

1. **OS Preparation activities for SAP HANA Database Server, SAP AnyDB Database Server or SAP NetWeaver Application Server**

2. **SAP HANA installations via SAP HANA database lifecycle manager (HDBLCM)**
   - Configure Firewall rules and Hosts file for SAP HANA database server instance/s
   - Install SAP Host Agent
   - Install SAP HANA database server, with any SAP HANA Component (e.g. Live Cache Apps, Application Function Library etc.)
   - Apply license to SAP HANA

3. **SAP HANA High Availability tasks**
   - Install SAP HANA System Replication
   - Install Linux Pacemaker, configure Pacemaker Fencing Agents for a given Infrastructure Platform
   - Configure Linux Pacemaker Resource Agents for SAP HANA

4. **Every SAP Software installation via SAP Software Provisioning Manager (SWPM)**
    - Execute SAP SWPM Unattended installation
        - Using on-the-fly generated inifile.params from Ansible Variables
        - Using a list of inifile parameters in an Ansible Dictionary
        - Re-using an existing inifile.params

5. **SAP NetWeaver High Availability tasks**
   - Install Linux Pacemaker, configure Pacemaker Fencing Agents for a given Infrastructure Platform
   - Configure Linux Pacemaker Resource Agents for SAP NetWeaver ASCS/ERS


## Execution

An Ansible Playbook is the file created and executed by an end-user, which imports from Ansible Collections to perform various activities on the target hosts.

The Ansible Playbook can call either an Ansible Role, or directly call the individual Ansible Modules:

- **Ansible Roles** (runs multiple Ansible Modules)
- **Ansible Modules** (and adjoining Python/Bash Functions)

It is strongly recommended to execute these Ansible Roles in accordance to best practice Ansible usage, where an Ansible Playbook is executed from a host and Ansible will login to a target host to perform the activities.

> If an Ansible Playbook is executed from the target host itself (similar to logging in and running a shell script), this is known as an Ansible Playbook 'localhost execution' and is not recommended as it has limitations on SAP Software installations (particularly installations across multiple hosts).

At a high-level, complex executions with various interlinked activities are run in parallel or sequentially using the following execution structure:

```
Ansible Playbook
-> source Ansible Collection
-> execute Ansible Task
---> run Ansible Role
-----> run Ansible Module (e.g. built-in Ansible Module for Shell)
```

### Execution examples

There are various methods to execute the Ansible Collection, dependent on the use case.

For more information, see [Getting started](./getting_started#readme) and edit the [sample Ansible Playbooks in `/playbooks`](../playbooks/).


## Requirements and Dependencies

### Target host - Operating System requirements

Designed for Linux operating systems, e.g. RHEL (7.x, 8.x, 9.x) and SLES (15 SPx).

This Ansible Collection has not been tested and amended for SAP NetWeaver Application Server instantiations on IBM AIX or Windows Server.

Assumptions for executing the Ansible Roles from this Ansible Collection include:

- Registered OS
- OS Package repositories are available (from the relevant content delivery network of the OS vendor)

N.B. The Ansible Collection works with SLES from version 15 SP3 and upwards, for the following reasons:

- firewalld is used within the Ansible Collection. In SLES 15 SP3, firewalld became the replacement for nftables. See changelog [SLE-16300](https://www.suse.com/releasenotes/x86_64/SUSE-SLES/15-SP3/index.html#jsc-SLE-16300)
- SELinux is used within the Ansible Collection. While introduced earlier with community support, full support for SELinux was provided as of SLES 15 SP3. See changelog [SLE-17307](https://www.suse.com/releasenotes/x86_64/SUSE-SLES/15-SP3/index.html#jsc-SLE-17307)

### Execution/Controller host - Operating System requirements

Execution of Ansible Playbooks using this Ansible Collection have been tested with:
- Python 3.9.7 and above (i.e. CPython distribution)
- Ansible Core 2.12.0 and above _(included with optional installation of Ansible Community Edition 5.0 and above)_
- OS: macOS with Homebrew, RHEL, SLES, and containers in Task Runners (e.g. Azure DevOps)

#### Ansible Core version

This Ansible Collection was designed for maximum backwards compatibility, with full compatibility starting from Ansible Core 2.12.0 and above.

**Note 1:** Ansible 2.9 was the last release before the Ansible project was split into Ansible Core and Ansible Community Edition, and was before Ansible Collections functionality was introduced. This Ansible Collection should execute when Ansible 2.9 is used, but it is not recommended and errors should be expected (and will not be resolved).

**Note 2:** Ansible Core versions prior to 2.14.12 , 2.15.8 , and 2.16.1 where `CVE-2023-5764` (templating inside `that` statement of `assert` Ansible Tasks) security fix was addressed, will work after `v1.3.4` of this Ansible Collection. Otherwise an error similar to the following will occur:

```yaml
fatal: [host01]: FAILED! =>
  msg: 'The conditional check ''13 <= 128'' failed. The error was: Conditional is marked as unsafe, and cannot be evaluated.'
```


## Testing

Various SAP Software solutions have been extensively tested.

Prior to each release, basic scenarios are executed to confirm functionality is working as expected; including SAP S/4HANA installation.

Important note: it is not possible for the project maintainers to test every SAP Software installation and solution scenario for each OS hosted on each Infrastructure Platform, if an error is identified please raise a [GitHub Issue](/../../issues/).


### Ansible Roles Lint Status

| Role Name | Ansible Lint Status |
| :--- | :--- |
| [sap_anydb_install_oracle](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_anydb_install_oracle) | N/A |
| [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure) | [![Ansible Lint for sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_general_preconfigure.yml/badge.svg)](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_general_preconfigure.yml) |
| [sap_ha_install_hana_hsr](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_install_hana_hsr) | [![Ansible Lint for sap_ha_install_hana_hsr](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_ha_install_hana_hsr.yml/badge.svg)](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_ha_install_hana_hsr.yml) |
| [sap_ha_pacemaker_cluster](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_pacemaker_cluster) | [![Ansible Lint for sap_ha_pacemaker_cluster](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_ha_pacemaker_cluster.yml/badge.svg)](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_ha_pacemaker_cluster.yml) |
| [sap_hana_install](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_install) | [![Ansible Lint for sap_hana_install](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_hana_install.yml/badge.svg)](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_hana_install.yml) |
| [sap_hana_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_preconfigure) | [![Ansible Lint for sap_hana_preconfigure](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_hana_preconfigure.yml/badge.svg)](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_hana_preconfigure.yml) |
| [sap_hostagent](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hostagent) | N/A |
| [sap_install_media_detect](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_install_media_detect) | N/A |
| [sap_maintain_etc_hosts](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_maintain_etc_hosts) | [![Ansible Lint for sap_maintain_etc_hosts](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_maintain_etc_hosts.yml/badge.svg)](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_maintain_etc_hosts.yml) |
| [sap_netweaver_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_netweaver_preconfigure) | [![Ansible Lint for sap_netweaver_preconfigure](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_netweaver_preconfigure.yml/badge.svg)](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_netweaver_preconfigure.yml) |
| [sap_storage_setup](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_storage_setup) | N/A |
| [sap_swpm](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_swpm) | [![Ansible Lint for sap_swpm](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_swpm.yml/badge.svg)](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_swpm.yml) |
