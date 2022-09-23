# sap_ha_install_hana_hsr Ansible Role

Ansible role for SAP HANA System Replication Setup on 2 nodes with the same OS and SAP HANA release.

## Overview

The **sap_ha_install_hana_hsr** role is part of this system role sequence:

| Sequence | System Role              | Description                                                  |
| :------: | :----------------------- | :----------------------------------------------------------- |
|    1.    | sap_general_preconfigure | System Preparation for SAP                                   |
|    2.    | sap_hana_preconfigure    | System Preparation for SAP HANA                              |
|    3.    | sap_hana_install         | Installation of SAP HANA Database                            |
|    4.    | sap_ha_install_hana_hsr  | Configuration of SAP HANA System Replication                 |
|    5.    | sap_ha_prepare_pacemaker | Authentication and Preparation of Nodes for Cluster Creation |
|    6.    | sap_ha_install_pacemaker | Initialization of the Pacemaker Cluster                      |
|    7.    | sap_ha_set_hana          | Configuration of SAP HANA Resources for SAP Solutions        |

The **sap_ha_install_hana_hsr** roles configures a HANA system replication relationship which is used by the pacemaker cluster to automate SAP HANA System Replication (HSR). Prerequisite is the SAP HANA installation on the nodes.

## Tasks included

| Task                   | Description                                                                         |
| ---------------------- | ----------------------------------------------------------------------------------- |
| update_etchosts.yml    | all nodes of the cluster will be entered into the /etc/hosts, if not already exists |
| configure_firewall.yml | this will configure the firewall für HANA system replication (opional)              |
| hdbuserstore.yml       | create a user in the hdbuserstore                                                   |
| log_mode.yml           | check/set database logmode                                                          |
| pki_files.yml          | copy pki file from primary to secondary database                                    |
| run_backup.yml         | perform backup on the primary note as pre required step for HANA system replication |
| configure_hsr.yml      | enable HANA system replication on primary node and register secondary database node |

## Common Variables/Parameters Used

| Name                             | Description                     | Value            |
| -------------------------------- | ------------------------------- | ---------------- |
| sap_domain                       | Domain Name                     | e.g. example.com |
| sap_hana_sid                     | SAP ID                          | e.g. RH1         |
| sap_hana_instance_number         | Instance Number                 | e.g. 00          |
| sap_hana_install_master_password | DB System Password              |
| sap_hana_cluster_nodes           | Parameter list of cluster nodes |
| sap_hana_hacluster_password      | Pacemaker hacluster Password    |

## Role specific Variables

| Name                              | Description      | Value                |
| --------------------------------- | ---------------- | -------------------- |
| sap_ha_install_hana_hsr_rep_mode  | replication mode | default is sync      |
| sap_ha_install_hana_hsr_oper_mode | operation mode   | default is logreplay |

In most cases you need to specify these variables only, if you want to use different values than the default values.

## Example Parameter File

```yaml
sap_hana_sid: "DB1"
sap_hana_instance_number: "00"
sap_hana_install_master_password: "my_hana-password"

### Cluster Definition
sap_ha_install_pacemaker_cluster_name: cluster1
sap_hana_hacluster_password: "my_hacluster-password"

sap_domain: example.com

sap_hana_cluster_nodes:
  - node_name: node1
    node_ip: 192.168.1.11
    node_role: primary
    hana_site: DC01

  - node_name: node2
    node_ip: 192.168.1.12
    node_role: secondary
    hana_site: DC02
```

### Execution Design

Having the parameters specified as above, it can be executed with one command:

```text
ansible-playbook example_playbook_with_parameters.ymnl
```

If you need to execute the role using an external handled, you can also limit the playbook for specific a **host** adding parameter defined in e **parameter_file**.

```text
ansible-playbook -l node1 example_playbook.yml -e @parameter_file.yml
```

A good way to start is executing the playbook with the option _--list_tasks_. You can than start a playbook with the option _--start-at-task_ at a specific point. _--list_task_ will not start any task.

For more information please check

```text
ansible-playbook --help
```

## License

Apache license 2.0
