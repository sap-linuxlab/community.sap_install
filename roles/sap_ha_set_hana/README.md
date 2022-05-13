# sap_ha_set_hana Ansible Role

Ansible role for SAP HANA High Availability Setup

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
    ansible-playbook --connection=local --limit localhost -i "localhost," sap-hana-ha.yml -e "@input_file.yml"
    ```

- This role must be ran in 2 parts on both the `primary` / `node1` and the `secondary` / `node2`
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
    sap_ha_set_hana_type: "az"
    sap_ha_set_hana_role: "primary"
    sap_ha_set_hana_part: "1"
    sap_ha_set_hana_sid: "HDB"
    sap_ha_set_hana_instance_number: "00"
    sap_ha_set_hana_load_balancer_ip: "10.1.1.1"
    sap_ha_set_hana_site1: "hana01"
    sap_ha_set_hana_site2: "hana02"
    ```

- Run 2 - part 1 - secondary:
    ```bash
    ansible-playbook --connection=local --limit localhost -i "localhost," sap-hana-ha.yml -e "@input_file2.yml"
    ```
    ```yaml
    # input_file2.yml contents
    sap_ha_set_hana_type: "az"
    sap_ha_set_hana_role: "secondary"
    sap_ha_set_hana_part: "1"
    sap_ha_set_hana_sid: "HDB"
    sap_ha_set_hana_instance_number: "00"
    sap_ha_set_hana_load_balancer_ip: "10.1.1.1"
    sap_ha_set_hana_site1: "hana01"
    sap_ha_set_hana_site2: "hana02"
    ```

- Run 3 - part 2 - primary:
    ```bash
    ansible-playbook --connection=local --limit localhost -i "localhost," sap-hana-ha.yml -e "@input_file3.yml"
    ```
    ```yaml
    # input_file3.yml contents
    sap_ha_set_hana_type: "az"
    sap_ha_set_hana_role: "primary"
    sap_ha_set_hana_part: "2"
    sap_ha_set_hana_sid: "HDB"
    sap_ha_set_hana_instance_number: "00"
    sap_ha_set_hana_load_balancer_ip: "10.1.1.1"
    sap_ha_set_hana_site1: "hana01"
    sap_ha_set_hana_site2: "hana02"
    ```

- Run 4 - part 2 - secondary:
    ```bash
    ansible-playbook --connection=local --limit localhost -i "localhost," sap-hana-ha.yml -e "@input_file4.yml"
    ```
    ```yaml
    # input_file4.yml contents
    sap_ha_set_hana_type: "az"
    sap_ha_set_hana_role: "secondary"
    sap_ha_set_hana_part: "2"
    sap_ha_set_hana_sid: "HDB"
    sap_ha_set_hana_instance_number: "00"
    sap_ha_set_hana_load_balancer_ip: "10.1.1.1"
    sap_ha_set_hana_site1: "hana01"
    sap_ha_set_hana_site2: "hana02"
    ```

## Variables / Inputs

| **Variable**                          | **Info**                                  | **Default** | **Required** |
| :---                                  | :---                                      | :---        | :---         |
| sap_ha_set_hana_type                  | Cloud type - `az` for Azure               | <none>      | yes          |
| sap_ha_set_hana_role                  | `primary` or `secondary`                  | <none>      | yes          |
| sap_ha_set_hana_part                  | `1` or `2`                                | <none>      | yes          |
| sap_ha_set_hana_sid                   | SID of the SAP HANA system                | <none>      | yes          |
| sap_ha_set_hana_instance_number       | Instance number of the SAP HANA system    | <none>      | yes          |
| sap_ha_set_hana_load_balancer_ip      | IP address of the load balancer           | <none>      | yes          |
| sap_ha_set_hana_site1                 | IP address of the load balancer           | <none>      | yes          |
| sap_ha_set_hana_site2                 | IP address of the load balancer           | <none>      | yes          |

## License

Apache license 2.0

## Author Information

IBM Lab for SAP Solutions, Red Hat for SAP Community of Practice, Jason Masipiquena, Sherard Guico, Markus Moster
