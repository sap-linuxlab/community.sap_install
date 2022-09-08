# community.sap_install Ansible Collection ![Ansible Lint](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint.yml/badge.svg?branch=main)

This Ansible Collection executes various SAP Software installations and configuration tasks for running SAP software on Linux operating systems; with handlers for SAP HANA database lifecycle manager (HDBLCM) and SAP Software Provisioning Manager (SWPM) for programmatic deployment of any SAP solution scenario.

This can be combined with other Ansible Collections to provide end-to-end automation, from download of SAP software installation media through to technical configuration and burstable SAP NetWeaver application servers (start/stop).

## Available Scenarios and Infrastructure Platforms

**Operating Systems (target machines)**

- Red Hat Enterprise Linux for SAP Solutions[^rhel]
  - RHEL 8.2, 8.4 and later

| Scenario                              | Description                                                                                                                     | Infrastructure Platform&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;                                                                                                                                                                                                                        |
| :------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SAP HANA single node installation** | Installation of a SAP HANA Database Server to a single machine                                                                  | <ul><li>:heavy_check_mark: AWS EC2</li><li>:warning: GCP VM</li><li>:warning: IBM Cloud, Intel VS</li><li>:warning: IBM Cloud, Power VS</li><li>:warning: Microsoft Azure</li><li>:heavy_check_mark: IBM PowerVM LPAR</li><li>:heavy_check_mark: OVirt VM</li><li>:warning: VMware vSphere VM</li></ul> |
| **SAP HANA 2-node pacemaker cluster** | Installation of a SAP HANA Database Server with HANA System Replication (HSR) in a basic 2-node Pacemaker Cluster configuration | <ul><li>:warning: AWS EC2</li><li>:warning: GCP VM</li><li>:warning: IBM Cloud, Intel VS</li><li>:warning: IBM Cloud, Power VS</li><li>:warning: Microsoft Azure</li><li>:warning: IBM PowerVM LPAR</li><li>:heavy_check_mark: OVirt VM</li><li>:warning: VMware vSphere VM</li></ul> |

Key:

- :heavy_check_mark: Verified compatibility
- :warning: Unverified and untested, expected to be compatible
- :x: Not compatible

**Out of Scope**

- AWS Classic environment
- Azure Classic environment using Azure Service Manager (ASM)
- IBM Cloud Classic Infrastructure environment

## Functionality

This Ansible Collection executes various SAP Software installations for different SAP solution scenarios, including:

- **SAP HANA installations via SAP HANA database lifecycle manager (HDBLCM)**

  - Install SAP HANA database server, with any SAP HANA Component (e.g. Live Cache Apps, Application Function Library etc.)
  - Configure Firewall rules and Hosts file for SAP HANA database server instance/s
  - Apply license to SAP HANA
  - Configure storage layout for SAP HANA mount points (i.e. /hana/data, /hana/log, /hana/shared)
  - Install SAP Host Agent
  - Install Linux Pacemaker, configure Pacemaker Fencing Agents and Pacemaker Resource Agents
  - Install SAP HANA System Replication
  - Set HA/DR for SAP HANA System Replication

- **Every SAP Software installation via SAP Software Provisioning Manager (SWPM)**
  - Run software install tasks using easy Ansible Variable to generate SWPM Unattended installations _(sap_swpm Ansible Role default mode)_.
    - Optional use of templating definitions for repeated installations _(sap_swpm Ansible Role default templates mode)_.
  - Run software install tasks with Ansible Variables one-to-one matched to SWPM Unattended Inifile parameters to generate bespoke SWPM Unattended installations _(sap_swpm Ansible Role advanced mode)_.
    - Optional use of templating definitions for repeated installations _(sap_swpm Ansible Role advanced templates mode)_.
  - Run previously-defined installations with an existing SWPM Unattended inifile.params _(sap_swpm Ansible Role inifile_reuse mode)_
  - Install Linux Pacemaker, configure Pacemaker Fencing Agents and Pacemaker Resource Agents
  - Set HA/DR with distributed SAP System installations (i.e. ERS)

## Contents

An Ansible Playbook can call either an Ansible Role, or the individual Ansible Modules:

- **Ansible Roles** (runs multiple Ansible Modules)
- **Ansible Modules** (and adjoining Python/Bash Functions)

For further information regarding the development, code structure and execution workflow please read the [Development documentation](./docs/DEVELOPMENT.md).

Within this Ansible Collection, there are various Ansible Roles and no custom Ansible Modules.

### Ansible Roles

| Name &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;              | Summary                                                                |
| :----------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------- |
| [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure)     | configure general settings for SAP software                            |
| [sap_netweaver_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_netweaver_preconfigure) | configure settings for SAP NetWeaver application server                |
| [sap_hana_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_preconfigure)           | configure settings for SAP HANA database server                        |
| [sap_hana_install](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_install)                     | install SAP HANA via HDBLCM                                            |
| [sap_swpm](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_swpm)                                     | install SAP Software via SWPM                                          |
| [sap_ha_install_hana_hsr](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_install_hana_hsr)       | install SAP HANA System Replication                                    |
| [sap_ha_prepare_pacemaker](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_prepare_pacemaker)     | prepare for Linux Pacemaker installation                               |
| [sap_ha_install_pacemaker](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_install_pacemaker)     | install and configure Linux Pacemaker                                  |
| [sap_ha_set_hana](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_set_hana)                       | configure HA/DR for SAP HANA                                           |
| [sap_ha_set_netweaver](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_set_netweaver)             | configure HA/DR for SAP NetWeaver                                      |
| [sap_hostagent](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hostagent)                           | install SAP Host Agent                                                 |
| [sap_storage_setup](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_storage_setup)                               | configure storage for SAP HANA, with LVM partitions and XFS filesystem |
| [sap_install_media_detect](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_install_media_detect)     | detect and extract SAP Software installation media                     |

**_Notes_**:

In general the "preconfigure" and "prepare" roles are prerequisites for the corresponding installation roles.
The logic has been separated to support a flexible execution of the different steps.

### Ansible Roles Lint Status

| Role Name                                                                                                                      | Ansible Lint Status                                                                                                                                                                                                                                                                                      |
| :----------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure)     | [![Ansible Lint for sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint%20sap_general_preconfigure.yml/badge.svg)](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint%20sap_general_preconfigure.yml)       |
| [sap_netweaver_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_netweaver_preconfigure) | [![Ansible Lint for sap_netweaver_preconfigure](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint%20sap_netweaver_preconfigure.yml/badge.svg)](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint%20sap_netweaver_preconfigure.yml) |
| [sap_hana_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_preconfigure)           | [![Ansible Lint for sap_hana_preconfigure](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint%20sap_hana_preconfigure.yml/badge.svg)](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint%20sap_hana_preconfigure.yml)                |
| [sap_hana_install](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_install)                     | [![Ansible Lint for sap_hana_install](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint%20sap_hana_install.yml/badge.svg)](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint%20sap_hana_install.yml)                               |

**_Notes:_**

- Ansible Playbook localhost executions may have limitations on SAP Software installations
- Ansible Roles for HA/DR are all designed for execution with Terraform

## Execution examples

There are various methods to execute the Ansible Collection, dependant on the use case. For more information, see [Execution examples with code samples](./docs/getting_started) and the summary below:

| Execution Scenario                                                                                                                                                       | Use Case                                                                                     | Target              |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------- | ------------------- |
| Ansible Playbook <br/>-> source Ansible Collection <br/>-> execute Ansible Task <br/>--> run Ansible Role <br/>---> run Ansible Module for Shell (built-in)<br/>---> ... | Complex executions with various interlinked activities;<br/> run in parallel or sequentially | Localhost or Remote |

## Requirements, Dependencies and Testing

### Operating System requirements

Designed for Linux operating systems, e.g. RHEL (7.x and 8.x) and SLES (15.x).

This Ansible Collection has not been tested and amended for SAP NetWeaver Application Server instantiations on IBM AIX or Windows Server.

Assumptions for executing the Ansible Roles from this Ansible Collection include:

- Registered OS
- OS Package repositories are available (from the relevant content delivery network of the OS vendor)

N.B. The Ansible Collection works with SLES from version 15 SP3 and upwards, for the following reasons:

- firewalld is used within the Ansible Collection. In SLES 15 SP3, firewalld became the replacement for nftables. See changelog [SLE-16300](https://www.suse.com/releasenotes/x86_64/SUSE-SLES/15-SP3/index.html#jsc-SLE-16300)
- SELinux is used within the Ansible Collection. While introduced earlier with community support, full support for SELinux was provided as of SLES 15 SP3. See changelog [SLE-17307](https://www.suse.com/releasenotes/x86_64/SUSE-SLES/15-SP3/index.html#jsc-SLE-17307)

### Python requirements

Python 3 from the execution/controller host.

### Testing on execution/controller host

**Tests with Ansible Core release versions:**

- Ansible Core 2.11.5 community edition

**Tests with Python release versions:**

- Python 3.9.7 (i.e. CPython distribution)

**Tests with Operating System release versions:**

- RHEL 8.4
- macOS 11.6 (Big Sur), with Homebrew used for Python 3.x via PyEnv

### Testing with SAP Software Provisioning Manager (SWPM)

SAP SWPM Catalog Products which have been tested:

- SAP S/4HANA AnyPremise 1809, 1909, 2020, 2021
  - One Host installation
  - Dual Host installation
  - Distributed installation
  - High Availability installation
  - System Copy (Homogeneous with SAP HANA Backup / Recovery) installation
  - System Rename
- SAP B/4HANA
- SAP Solution Manager 7.2
- SAP Business Suite (i.e. ECC)
- SAP NetWeaver applications (e.g. GRC)
- SAP Web Dispatcher

## References

- Azure:

  - [Azure Pacemaker Setup Guide](https://docs.microsoft.com/en-us/azure/virtual-machines/workloads/sap/high-availability-guide-rhel-pacemaker)

- AWS:

  - [Configuring SAP HANA Scale-Up System Replication with the RHEL HA Add-On on Amazon Web Services (AWS)](https://access.redhat.com/articles/3569621)

- Google Cloud:

  - [HA cluster configuration guide for SAP HANA on RHEL](https://cloud.google.com/solutions/sap/docs/sap-hana-ha-config-rhel)

- IBM Cloud:
  - [IBM Cloud for SAP portfolio - IBM Cloud Docs](https://cloud.ibm.com/docs/sap)

- RHEL:
    - [Overview of the Red Hat Enterprise Linux for SAP Solutions subscription](https://access.redhat.com/solutions/3082481)
    - [Automating SAP HANA Scale-Up System Replication using the RHEL HA Add-On](https://access.redhat.com/articles/3004101)

## License

- [Apache 2.0](./LICENSE)

## Contributors

Contributors to the Ansible Roles within this Ansible Collection, are shown within [/docs/contributors](./docs/CONTRIBUTORS.md).

[^rhel]: [Overview of the Red Hat Enterprise Linux for SAP Solutions subscription](https://access.redhat.com/solutions/3082481)
