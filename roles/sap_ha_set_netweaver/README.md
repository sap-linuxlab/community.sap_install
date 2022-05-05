# sap_ha_set_netweaver Ansible Role

Ansible role for SAP NW High Availability Setup

## Scope

- **RedHat Enterprise Linux**
    - Tested on RHEL 8.2

- **Azure** 
    - Tested
    - Followed the steps based on the guide published in
        - [Azure HA Guide](https://docs.microsoft.com/en-us/azure/virtual-machines/workloads/sap/high-availability-guide-rhel-netapp-files)

- **AWS**
    - Future plans

## Overview

### Execution Design

- This Ansible role is designed to be executed using an external handler such `Terraform` or a separate `bash` script
- Limitations of doing an SAP installation where scripts and Ansible playbooks have to be executed locally and not thru the usual `ansible command` -> `inventory of hosts` scenario

    Sample execution:

    ```
    ansible-playbook --connection=local --limit localhost -i "localhost," sap-hana-ha.yml -e "@input_file.yml"
    ```

- This role must be ran in 4 parts on both the `primary` / `node1` and the `secondary` / `node2`
    - **Part 1** - Prepare NW for Installation
    - **Part 2** - Post NW ASCS Installation
    - **Part 3** - Post NW ERS Installation
    - **Part 4** - Post NW PAS Installation

- Tasks marked with `[A]` are executed for both `primary` / `node1` and `secondary` / `node2`
- Tasks marked with `[1]` are only executed for `primary` / `node1`
- Tasks marked with `[2]` are only executed for `secondary` / `node2`

### Sample Execution Steps

- Run 1 - part 1 - primary:
    ```bash
    ansible-playbook --connection=local --limit localhost -i "localhost," sap-hana-ha.yml -e "@input_file1.yml"
    ```
    ```yaml
    # input_file1.yml contents
    sap_ha_set_netweaver_role: "primary"
    sap_ha_set_netweaver_part: "1"
    <other variables>
    ```

- Run 2 - part 1 - secondary:
    ```bash
    ansible-playbook --connection=local --limit localhost -i "localhost," sap-hana-ha.yml -e "@input_file2.yml"
    ```
    ```yaml
    # input_file2.yml contents
    sap_ha_set_netweaver_role: "secondary"
    sap_ha_set_netweaver_part: "1"
    <other variables>
    ```

- Run 3 - part 2 - primary:
    ```bash
    ansible-playbook --connection=local --limit localhost -i "localhost," sap-hana-ha.yml -e "@input_file3.yml"
    ```
    ```yaml
    # input_file3.yml contents
    sap_ha_set_netweaver_role: "primary"
    sap_ha_set_netweaver_part: "2"
    <other variables>
    ```

- Run 4 - part 2 - secondary:
    ```bash
    ansible-playbook --connection=local --limit localhost -i "localhost," sap-hana-ha.yml -e "@input_file4.yml"
    ```
    ```yaml
    # input_file4.yml contents
    sap_ha_set_netweaver_role: "secondary"
    sap_ha_set_netweaver_part: "2"
    <other variables>
    ```

- Run 5 - part 3 - primary:
    ```bash
    ansible-playbook --connection=local --limit localhost -i "localhost," sap-hana-ha.yml -e "@input_file4.yml"
    ```
    ```yaml
    # input_file5.yml contents
    sap_ha_set_netweaver_role: "primary"
    sap_ha_set_netweaver_part: "3"
    <other variables>
    ```

- Run 6 - part 3 - secondary:
    ```bash
    ansible-playbook --connection=local --limit localhost -i "localhost," sap-hana-ha.yml -e "@input_file4.yml"
    ```
    ```yaml
    # input_file6.yml contents
    sap_ha_set_netweaver_role: "secondary"
    sap_ha_set_netweaver_part: "3"
    <other variables>
    ```

- Run 7 - part 4 - primary:
    ```bash
    ansible-playbook --connection=local --limit localhost -i "localhost," sap-hana-ha.yml -e "@input_file4.yml"
    ```
    ```yaml
    # input_file7.yml contents
    sap_ha_set_netweaver_role: "primary"
    sap_ha_set_netweaver_part: "4"
    <other variables>
    ```

- Run 8 - part 4 - primary:
    ```bash
    ansible-playbook --connection=local --limit localhost -i "localhost," sap-hana-ha.yml -e "@input_file4.yml"
    ```
    ```yaml
    # input_file8.yml contents
    sap_ha_set_netweaver_role: "secondary"
    sap_ha_set_netweaver_part: "4"
    <other variables>
    ```

## Variables / Inputs

| **Variable**                                  | **Info**                                  | **Default** | **Required** |
| :---                                          | :---                                      | :---        | :---         |
| sap_ha_set_netweaver_type                                | Cloud type - `az` for Azure               | <none>      | yes          |
| sap_ha_set_netweaver_role                                | `primary` or `secondary`                  | <none>      | yes          |
| sap_ha_set_netweaver_part                                | `1` or `2`                                | <none>      | yes          |
| sap_ha_set_netweaver_sid                                 | <none>                                    | <none>      | yes          |
| sap_ha_set_netweaver_nfs_ip                              | <none>                                    | <none>      | yes          |
| sap_ha_set_netweaver_nfs_trans_ip                        | <none>                                    | <none>      | yes          |
| sap_ha_set_netweaver_fqdn                                | <none>                                    | <none>      | yes          |
| sap_ha_set_netweaver_node1_hostname                      | <none>                                    | <none>      | yes          |
| sap_ha_set_netweaver_node1_ip                            | <none>                                    | <none>      | yes          |
| sap_ha_set_netweaver_node2_hostname                      | <none>                                    | <none>      | yes          |
| sap_ha_set_netweaver_node2_ip                            | <none>                                    | <none>      | yes          |
| sap_ha_set_netweaver_load_balancer_db_hostname           | <none>                                    | <none>      | yes          |
| sap_ha_set_netweaver_load_balancer_db_ip                 | <none>                                    | <none>      | yes          |
| sap_ha_set_netweaver_load_balancer_db_nr                 | <none>                                    | <none>      | yes          |
| sap_ha_set_netweaver_load_balancer_db_schema             | <none>                                    | 'SAPABAP1'  | yes          |
| sap_ha_set_netweaver_load_balancer_db_schema_password:   | <none>                                    | <none>      | yes          |
| sap_ha_set_netweaver_load_balancer_ascs_hostname         | <none>                                    | <none>      | yes          |
| sap_ha_set_netweaver_load_balancer_ascs_ip               | <none>                                    | <none>      | yes          |
| sap_ha_set_netweaver_load_balancer_ers_hostname          | <none>                                    | <none>      | yes          |
| sap_ha_set_netweaver_load_balancer_ers_ip                | <none>                                    | <none>      | yes          |
| sap_ha_set_netweaver_ascs_instance_nr                    | <none>                                    | <none>      | yes          |
| sap_ha_set_netweaver_ascs_instance_hostname              | <none>                                    | <none>      | yes          |
| sap_ha_set_netweaver_ascs_instance_ip                    | <none>                                    | <none>      | yes          |
| sap_ha_set_netweaver_ers_instance_nr                     | <none>                                    | <none>      | yes          |
| sap_ha_set_netweaver_ers_instance_hostname               | <none>                                    | <none>      | yes          |
| sap_ha_set_netweaver_ers_instance_ip                     | <none>                                    | <none>      | yes          |
| sap_ha_set_netweaver_pas_instance_nr                     | <none>                                    | <none>      | yes          |
| sap_ha_set_netweaver_pas_instance_hostname               | <none>                                    | <none>      | yes          |
| sap_ha_set_netweaver_pas_instance_ip                     | <none>                                    | <none>      | yes          |
| sap_ha_set_netweaver_az_netapp_file_volumes              | <none>                                    | 'NFSv4.1'      | yes          |

## License

Apache license 2.0

## Author Information

IBM Lab for SAP Solutions, Red Hat for SAP Community of Practice, Jason Masipiquena, Sherard Guico, Markus Moster
