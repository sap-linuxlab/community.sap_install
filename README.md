# community.sap_install Ansible Collection

![Ansible Lint](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint.yml/badge.svg?branch=main)

## Description

This Ansible Collection executes various SAP Software installations and configuration tasks for various SAP solutions and deployment scenarios on supported Linux operating systems.

Included roles cover range of tasks:

- Preparation of Operating system and SAP installation media before installation
- Installation of SAP Database, either SAP HANA or Oracle Database
- Installation of SAP Products, like SAP S4HANA, SAP BW4HANA, SAP Netweaver, SAP Solution Manager and others.
- Configuration of replication of SAP HANA and High Availability clusters for SAP HANA and SAP Netweaver


## Requirements

| Component | Control Node | Managed Node |
| --- | --- | --- |
| Operating System | Any OS | Red Hat Enterprise Linux for SAP Solutions 8.x, 9.x and 10.x<br>SUSE Linux Enterprise Server for SAP applications 15 SP5, 15 SP6, 15 SP7 and 16.0 |
| Python | 3.11 or higher | 3.9 or higher |
| Ansible-Core | 2.18 or higher | N/A |
| Ansible | 12 or higher | N/A |

> **Managed Node Registration**<br>
> Operating system needs to have access to required package repositories either directly or via subscription registration.

**Additional notes:**

- **Version Compatibility:** For a detailed mapping of supported Python versions and Ansible-Core lifecycles, refer to the official [Ansible-Core Support Matrix](https://docs.ansible.com/projects/ansible/latest/reference_appendices/release_and_maintenance.html#ansible-core-support-matrix).
- **Control Node Permissions:** Ensure the user executing the playbooks has the necessary SSH keys and sudo privileges configured for the target environment.

## Installation Instructions

### Installation
Install this collection with Ansible Galaxy command:
```console
ansible-galaxy collection install community.sap_install
```

Optionally you can include collection in requirements.yml file and include it together with other collections using: `ansible-galaxy collection install -r requirements.yml`
Requirements file need to be maintained in following format:
```yaml
collections:
  - name: community.sap_install
```

### Upgrade
Installed Ansible Collection will not be upgraded automatically when Ansible package is upgraded.

To upgrade the collection to the latest available version, run the following command:
```console
ansible-galaxy collection install community.sap_install --upgrade
```

You can also install a specific version of the collection, when you encounter issues with latest version. Please report these issues in affected Role repository if that happens.
Example of downgrading collection to version 1.4.0:
```
ansible-galaxy collection install community.sap_install:==1.4.0
```

See [Installing collections](https://docs.ansible.com/ansible/latest/collections_guide/collections_installing.html) for more details on installation methods.


## Use Cases

### Example Scenarios

- Preparation of Operating system for SAP installation
- Preparation of SAP installation media for SAP installation
- Installation of SAP HANA (including High Availability with replication) or Oracle Database
- Installation of SAP S4HANA or other SAP products
- Configuration of Pacemaker cluster for SAP HANA and SAP Netweaver

More deployment scenarios are available in [ansible.playbooks_for_sap](https://github.com/sap-linuxlab/ansible.playbooks_for_sap) repository.

### Ansible Roles
All included roles can be executed independently or as part of [ansible.playbooks_for_sap](https://github.com/sap-linuxlab/ansible.playbooks_for_sap) playbooks.

| Name | Summary |
| --- | --- |
| [sap_anydb_install_oracle](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_anydb_install_oracle) | Install Oracle DB 19.x for SAP |
| [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure) | Configure general OS settings for SAP software |
| [sap_ha_install_hana_hsr](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_install_hana_hsr) | Configure and enable SAP HANA System Replication |
| [sap_ha_pacemaker_cluster](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_pacemaker_cluster) | Configure Pacemaker cluster for SAP HANA and SAP Netweaver |
| [sap_hana_install](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_install) | Install SAP HANA via HDBLCM |
| [sap_hana_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_preconfigure) | Configure OS settings for SAP HANA database server |
| [sap_hostagent](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hostagent) | Install SAP Host Agent |
| [sap_install_media_detect](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_install_media_detect) | Detect and extract SAP Software installation media |
| [sap_maintain_etc_hosts](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_maintain_etc_hosts) | Maintain the /etc/hosts file of an SAP software host |
| [sap_netweaver_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_netweaver_preconfigure) | Configure OS settings for SAP NetWeaver application server |
| [sap_storage_setup](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_storage_setup) | Configure storage for SAP system (Folder structure, LVM, XFS, NFS) |
| [sap_swpm](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_swpm) | Install SAP Software via SWPM |


## Testing
This Ansible Collection was tested across different Operating Systems, SAP products and scenarios. You can find examples of some of them below.

Operating systems:

- Red Hat Enterprise Linux for SAP Solutions 8.x, 9.x and 10.x
- SUSE Linux Enterprise Server for SAP applications 15 SP5, 15 SP6, 15 SP7 and 16.0

Deployment scenarios:

- All scenarios included in [ansible.playbooks_for_sap](https://github.com/sap-linuxlab/ansible.playbooks_for_sap) repository

SAP Products:

- SAP S/4HANA AnyPremise (1809, 1909, 2020, 2021, 2022, 2023) with setup as Standard, Distributed, High Availability and optional Maintenance Planner or Restore System Copy
- SAP Business Suite (ECC) on HANA and SAP Business Suite (ECC) with SAP AnyDB - SAP ASE, SAP MaxDB, IBM Db2, Oracle DB
- SAP BW/4HANA (2021, 2023) with setup as Standard or Scale-Out
- SAP HANA 2.0 (SPS04+) with setup as Scale-Up, Scale-Out, High Availability
- Other SAP installation activities; such as System Rename, System Copy Export, SAP Solution Manager and SAP Web Dispatcher

> **Testing Disclaimer**<br>
> It is not possible to test every Operating System and SAP Product combination with every release.<br>
> Testing is regularly done for common scenarios: SAP HANA, SAP HANA HA, SAP S4HANA Distributed HA**


## Contributing
For information on how to contribute, please see our [contribution guidelines](https://sap-linuxlab.github.io/initiative_contributions/).


## Contributors
We welcome contributions to this collection. For a list of all contributors and information on how you can get involved, please see our [CONTRIBUTORS document](./CONTRIBUTORS.md).


## Support
You can report any issues using [Issues](https://github.com/sap-linuxlab/community.sap_install/issues) section.


## Release Notes and Roadmap
You can find the release notes of this collection in [Changelog file](https://github.com/sap-linuxlab/community.sap_install/blob/main/CHANGELOG.rst)


## Further Information

### Variable Precedence Rules
Please follow [Ansible Precedence guidelines](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable) on how to pass variables when using this collection.

### Getting Started
More information on how to execute Ansible playbooks is in [Getting started guide](https://github.com/sap-linuxlab/community.sap_install/blob/main/docs/getting_started/README.md).


## License
[Apache 2.0](https://github.com/sap-linuxlab/community.sap_install/blob/main/LICENSE) 
