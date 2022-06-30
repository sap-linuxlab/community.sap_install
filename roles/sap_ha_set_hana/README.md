# sap_ha_set_hana Ansible Role

Ansible role for SAP HANA High Availability Setup

## Overview

The **sap_ha_set_hana** role is part of this sequence:

| Sequence | System Role              | Description                                                  |
| :------: | :----------------------- | :----------------------------------------------------------- |
|    1.    | sap_general_preconfigure | System Preparation for SAP                                   |
|    2.    | sap_hana_preconfigure    | System Preparation for SAP HANA                              |
|    3.    | sap_hana_install         | Installation of SAP HANA Database                            |
|    4.    | sap_ha_install_hana_hsr  | Configuration of SAP HANA System Replication                 |
|    5.    | sap_ha_prepare_pacemaker | Authentication and Preparation of Nodes for Cluster Creation |
|    6.    | sap_ha_install_pacemaker | Initialization of the Pacemaker Cluster                      |
|    7.    | sap_ha_set_hana          | Configuration of SAP HANA Resources for SAP Solutions        |

The **sap_ha_set_hana** is the last role to complete the configuration of te cluster ressources for
SAP HANA.

## Tasks includes

| Task                   | Description                 |
| ---------------------- | --------------------------- |
| cluster_sudoer.yml     | configure sudoer for SRHOOK |
| cluster_resources.yml  | create SAPHANA ressources   |
| cluster_srhook.yml     | configure myHooks SAPHanaSR |
| cluster_constraint.yml | configure constraints       |

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

| Name                 | Description                                            | Value         |
| -------------------- | ------------------------------------------------------ | ------------- |
| sap_ha_set_hana_vip1 | Virtual IP address of primary HANA database            | sap_hana_vip1 |
| sap_ha_set_hana_vip2 | Virtual IP address of secondary HANA database(planned) | sap_hana_vip2 |

## Example Parameter File

```
sap_hana_sid: 'DB1'
sap_hana_instance_number: '00'
sap_hana_install_master_password: 'my_hana-pass

### Cluster Definition
sap_ha_install_pacemaker_cluster_name: cluster1
sap_hana_hacluster_password: 'my_hacluster-pass
sap_pacemaker_stonith_devices:

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

sap_hana_vip1: 192.168.1.13
```

### Execution Design

Having the parameters specified as above, it can be executed with one command:

```
ansible-playbook example_playbook_with_parameters.ymnl
```

If you need to execute the role using an external handled, you can also limit the playbook for
specific a **host** adding parameter defined in e **parameter_file**.

```
ansible-playbook -l node1 example_playbook.yml -e @parameter_file.yml
```

A good way to start is executing the playbook with the option _--list_tasks_. You can than start a
playbook with the option _--start-at-task_ at a specific point. _--list_task_ will not start any
task.

For more information please check

```
ansible-playbook --help
```

## License

Apache license 2.0

## Author Information

IBM Lab for SAP Solutions, Red Hat for SAP Community of Practice, Jason Masipiquena, Sherard Guico,
Markus Moster
