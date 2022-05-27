# sap_ha_install_hana_hsr Ansible Role

Ansible role for SAP HANA System Replication Setup

## Scope

- **RedHat Enterprise Linux**
    - Tested on RHEL 8.2

- **Azure** 
    - Tested
    - Followed the steps based on the guide published in
        - [Azure HA Guide](https://docs.microsoft.com/en-us/azure/virtual-machines/workloads/sap/sap-hana-high-availability-rhel)

- **AWS**
    - Future plans

## Overview

### Execution Design

- This Ansible role is designed to be executed using an external handler such `Terraform` or a separate `bash` script
- Limitations of doing an SAP installation where scripts and Ansible playbooks have to be executed locally and not thru the usual `ansible command` -> `inventory of hosts` scenario

    Sample execution:

    ```bash
    ansible-playbook --connection=local --limit localhost -i "localhost," sap-hana-hsr.yml -e "@input_file.yml"
    ```

- This role must be ran on both the `primary` / `node1` and the `secondary` / `node2`
- Tasks marked with `[A]` are executed for both `primary` / `node1` and `secondary` / `node2`
- Tasks marked with `[1]` are only executed for `primary` / `node1`
- Tasks marked with `[2]` are only executed for `secondary` / `node2`

### Sample Execution Steps

- Run 1 - primary:
    ```bash
    ansible-playbook --connection=local --limit localhost -i "localhost," sap-hana-hsr.yml -e "@input_file1.yml"
    ```
    ```yaml
    # input_file1.yml contents
    sap_ha_install_hana_hsr_role: "primary"
    <other variables>
    ```

- Run 2 - secondary:
    ```bash
    ansible-playbook --connection=local --limit localhost -i "localhost," sap-hana-hsr.yml -e "@input_file2.yml"
    ```
    ```yaml
    # input_file2.yml contents
    sap_ha_install_hana_hsr_role: "secondary"
    <other variables>
    ```

## Variables / Inputs

| **Variable**                                             | **Info**                                  | **Default** | **Required** |
| :---                                                     | :---                                      | :---        | :---         |
| sap_ha_install_hana_hsr_role                             | `primary` or `secondary`                  | <none>      | yes          |
| sap_ha_install_hana_hsr_sid                              | SID of the SAP HANA system                | <none>      | yes          |
| sap_ha_install_hana_hsr_instance_number                  | Instance number of the SAP HANA system    | <none>      | yes          |
| sap_ha_install_hana_hsr_db_system_password               | SYSTEM password of the SAP HANA system    | <none>      | yes          |
| sap_ha_install_hana_hsr_alias                            | Alias name of the SAP HANA system         | <none>      | yes          |
| sap_ha_install_hana_hsr_primary_ip                       | IP address of the `primary` node          | <none>      | yes          |
| sap_ha_install_hana_hsr_primary_hostname                 | Hostname of the `primary` node            | <none>      | yes          |
| sap_ha_install_hana_hsr_secondary_ip                     | IP address of the `secondary` node        | <none>      | yes          |
| sap_ha_install_hana_hsr_secondary_hostname               | Hostname of the `secondary` node          | <none>      | yes          |
| sap_ha_install_hana_hsr_fqdn                             | Fully qualified domain name               | <none>      | yes          |
| sap_ha_install_hana_hsr_hdbuserstore_system_backup_user  | hdbuserstore username to be set           | <none>      | no           |
| sap_ha_install_hana_hsr_rep_mode                         | HSR replication mode                      | 'sync'      | no           |
| sap_ha_install_hana_hsr_oper_mode                        | HSR operation mode                        | 'logreplay' | no           |
| sap_ha_install_hana_hsr_type                             | Cloud type - not used right now           | <none>      | not used     |

## License

Apache license 2.0

## Author Information

IBM Lab for SAP Solutions, Red Hat for SAP Community of Practice, Jason Masipiquena, Sherard Guico, Markus Moster
