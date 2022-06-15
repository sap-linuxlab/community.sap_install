# sap_ha_install_hana_hsr Ansible Role

Ansible role for SAP HANA System Replication Setup

## Scope

- **RedHat Enterprise Linux**
    - Tested on RHEL 8.2 and later

- **Azure**
    - Tested
    - Followed the steps based on the guide published in
        - [Azure HA Guide](https://docs.microsoft.com/en-us/azure/virtual-machines/workloads/sap/sap-hana-high-availability-rhel)

- **AWS**
    - Future plans

## Overview

The **sap_ha_install_hana_hsr** role is part of this system role sequence:

Sequence|System Role|Description
:---:|:---|:---
1.|sap_general_preconfigure|System Preparation for SAP
2.| sap_hana_preconfigure|System Preparation for SAP HANA
3.|sap_hana_install|Installation of SAP HANA Database
4.|sap_ha_install_hana_hsr|Configuration of SAP HANA System Replication
5.|sap_ha_prepare_pacemaker|Authentication and Preparation of Nodes for Cluster Creation
6.|sap_ha_install_pacemaker|Initialization of the Pacemaker Cluster
7.|sap_ha_set_hana|Configuration of SAP HANA Resources for SAP Solutions

The **sap_ha_install_hana_hsr** roles configures a HANA system replication relationship which is used by the pacemaker cluster to automate SAP HANA system replication.

## Parameters Used
Parameters with role prefix in the name are only related to the role.

Name|Description|Value
---|---|---
sap_domain|Domain Name| f.e. example.com
sap_hana_sid|SAP ID| f.e. RH1
sap_hana_instance_number|Instance Number|f.e. 00
sap_hana_site1_name|name of the first site| f.e. DC1
sap_hana_site2_name|name of the second site| f.e. DC2
sap_hana_systemdb_password| DB System Password
sap_hana_system_role| Role of the node| primary or secondary
sap_hana_node1_hostname|hostname of the first node|f.e. hana01
sap_hana_node1_ip|IP address of the first node| f.e. 192.168.1.11
sap_hana_node2_hostname|hostname of the second node|f.e. hana02
sap_hana_node2_ip|IP address of the second node| f.e. 192.168.1.12
sap_ha_install_hana_hsr_rep_mode| replication mode| default is sync
sap_ha_install_hana_hsr_oper_mode| operation mode| default is logreplay

## Tasks includes

Task|Description
---|---
update_etchosts.yml|all nodes of the cluster will be entered into the /etc/hosts, if not already exists
configure_firewall.yml|this will configure the firewall für HANA system replication (opional)
hdbuserstore.yml|create a user in the hdbuserstore
log_mode.yml|check/set database logmode
pki_files.yml|copy pki file from primary to secondary database
run_backup.yml|perform backup on the primary note as pre required step for HANA system replication
configure_hsr.yml| enable HANA system replication on primary node and register secondary database node



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
- Tasks marked with `[2]` are only executed for `secsap_ha_install_hana_hsr_rep_mode: sync
sap_ha_install_hana_hsr_oper_mode: logreplayondary` / `node2`

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
| sap_ha_install_hana_hsr_secondary_hostname               | sap_ha_install_hana_hsr_rep_mode: sync
sap_ha_install_hana_hsr_oper_mode: logreplayHostname of the `secondary` node          | <none>      | yes          |
| sap_ha_install_hana_hsr_fqdn                             | Fully qualified domain name               | <none>      | yes          |
| sap_ha_install_hana_hsr_hdbuserstore_system_backup_user  | hdbuserstore username to be set           | <none>      | no           |
| sap_ha_install_hana_hsr_rep_mode                         | HSR replication mode                      | 'sync'      | no           |
| sap_ha_install_hana_hsr_oper_mode                        | HSR operation mode                        | 'logreplay' | no           |
| sap_ha_install_hana_hsr_type                             | Cloud type - not used right now           | <none>      | not used     |

## License

Apache license 2.0
sap_ha_install_hana_hsr_rep_mode: sync
sap_ha_install_hana_hsr_oper_mode: logreplay
sap_ha_install_hana_hsr_rep_mode: sync
sap_ha_install_hana_hsr_oper_mode: logreplay
sap_ha_install_hana_hsr_rep_mode: sync
sap_ha_install_hana_hsr_oper_mode: logreplay
IBM Lab for SAP Solutions, Red Hat for SAP Community of Practice, Jason Masipiquena, Sherard Guico, Markus Moster
  include_tasks: update_etchosts.yml
  include_tasks: configure_firewall.yml
  include_tasks: hdbuserstore.yml
  include_tasks: log_mode.yml
  include_tasks: pki_files.yml
  include_tasks: run_backup.yml
  include_tasks: configure_hsr.yml
