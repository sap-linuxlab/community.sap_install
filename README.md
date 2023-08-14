# community.sap_install Ansible Collection

![Ansible Lint](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint.yml/badge.svg?branch=main)

This Ansible Collection executes various SAP Software installations and configuration tasks for running SAP software on Linux operating systems; with handlers for SAP HANA database lifecycle manager (HDBLCM) and SAP Software Provisioning Manager (SWPM) for programmatic deployment of any SAP solution scenario.

This can be combined with other Ansible Collections to provide end-to-end automation, from download of SAP software installation media through to technical configuration and burstable SAP NetWeaver application servers (start/stop).

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

| Name                                                                                                                                           | Summary                                                                |
| :--- | :--- |
| [sap_anydb_install_oracle](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_anydb_install_oracle)                     | install Oracle DB 19.x for SAP                                         |
| [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure)      	         | configure general OS settings for SAP software                         |
| [sap_ha_install_hana_hsr](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_install_hana_hsr)        	         | install SAP HANA System Replication                                    |
| [sap_ha_pacemaker_cluster](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_pacemaker_cluster)                     | install and configure pacemaker and SAP resources                      |
| [sap_hana_install](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_install)                      	         | install SAP HANA via HDBLCM                                            |
| [sap_hana_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_preconfigure)            	         | configure settings for SAP HANA database server                        |
| [sap_hostagent](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hostagent)                                           | install SAP Host Agent                                                 |
| [sap_hypervisor_node_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hypervisor_node_preconfigure)     | configure a hypervisor running VMs for SAP HANA                        |
| [sap_install_media_detect](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_install_media_detect)                     | detect and extract SAP Software installation media                     |
| [sap_netweaver_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_netweaver_preconfigure)  	         | configure settings for SAP NetWeaver application server                |
| [sap_storage_setup](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_storage_setup)                                   | configure storage for SAP HANA, with LVM partitions and XFS filesystem |
| [sap_swpm](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_swpm)                                                     | install SAP Software via SWPM                                          |
| [sap_vm_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_vm_preconfigure)                               | configure settings for a guest (VM) running on RHV/KVM for SAP HANA    |

**_Notes_**:

In general the "preconfigure" and "prepare" roles are prerequisites for the corresponding installation roles.
The logic has been separated to support a flexible execution of the different steps.

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
| [sap_hypervisor_node_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hypervisor_node_preconfigure) | N/A |
| [sap_install_media_detect](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_install_media_detect) | N/A |
| [sap_netweaver_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_netweaver_preconfigure) | [![Ansible Lint for sap_netweaver_preconfigure](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_netweaver_preconfigure.yml/badge.svg)](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_netweaver_preconfigure.yml) |
| [sap_storage_setup](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_storage_setup) | N/A |
| [sap_swpm](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_swpm) | [![Ansible Lint for sap_swpm](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_swpm.yml/badge.svg)](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_swpm.yml) |
| [sap_vm_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_vm_preconfigure) | N/A |

**_Notes:_**

- Ansible Playbook localhost executions may have limitations on SAP Software installations
- Ansible Roles for HA/DR are all designed for execution with Terraform

## Execution examples

There are various methods to execute the Ansible Collection, dependant on the use case. For more information, see [Execution examples with code samples](./docs/getting_started) and the summary below:

| Execution Scenario | Use Case | Target |
| ---- | ---- | ---- |
| Ansible Playbook <br/>-> source Ansible Collection <br/>-> execute Ansible Task <br/>--> run Ansible Role <br/>---> run Ansible Module for Shell (built-in)<br/>---> ... | Complex executions with various interlinked activities;<br/> run in parallel or sequentially | Localhost or Remote |

## Testing, Requirements and Dependencies

### Testing

Various SAP Software solutions have been extensively tested:

- SAP HANA
  - Scale-Up
  - Scale-Out
  - High Availability
- SAP NetWeaver AS (ABAP or JAVA) and additional addons (e.g. GRC, ADS)
- SAP S/4HANA AnyPremise (1809, 1909, 2020, 2021, 2022)
  - Sandbox (One Host) installation
  - Standard (Dual Host) installation
  - Distributed installation
  - High Availability installation
  - System Copy (Homogeneous with SAP HANA Backup / Recovery) installation
  - Maintenance Planner installation
  - System Rename
- SAP BW/4HANA
- SAP Business Suite on HANA (SoH, i.e. SAP ECC on HANA)
- SAP Business Suite (i.e. SAP ECC with SAP AnyDB - SAP ASE, SAP MaxDB, IBM Db2, Oracle DB)
- SAP Solution Manager 7.2
- SAP Web Dispatcher

### Target host - Operating System requirements

Designed for Linux operating systems, e.g. RHEL (7.x and 8.x) and SLES (15.x).

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
- Ansible Core 2.11.5 and above _(included with optional installation of Ansible Community Edition 4.0 and above)_
- OS: macOS with Homebrew, RHEL, SLES, and containers in Task Runners (e.g. Azure DevOps)

## License

- [Apache 2.0](./LICENSE)

## Contributors

Contributors to the Ansible Roles within this Ansible Collection, are shown within [/docs/contributors](./docs/CONTRIBUTORS.md).
