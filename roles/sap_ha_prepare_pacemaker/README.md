# sap_ha_prepare_pacemaker Ansible Role

The role **sap_ha_prepare_pacemaker** is necessary because tasks needs to be finished on all nodes before the the cluster can be configured.

The following tasks are part of this role and excluded from the role **sap_ha_install_pacemaker**:
  - Software Installation
  - Host authentication

## Overview

The **sap_ha_prepare_pacemaker** role is part of this sequence:

| Sequence | System Role              | Description                                                  |
| :------: | :----------------------- | :----------------------------------------------------------- |
|    1.    | sap_general_preconfigure | System Preparation for SAP                                   |
|    2.    | sap_hana_preconfigure    | System Preparation for SAP HANA                              |
|    3.    | sap_hana_install         | Installation of SAP HANA Database                            |
|    4.    | sap_ha_install_hana_hsr  | Configuration of SAP HANA System Replication                 |
|    5.    | sap_ha_prepare_pacemaker | Authentication and Preparation of Nodes for Cluster Creation |
|    6.    | sap_ha_install_pacemaker | Initialization of the Pacemaker Cluster                      |
|    7.    | sap_ha_set_hana          | Configuration of SAP HANA Resources for SAP Solutions        |

The **sap_ha_install_pacemaker** prepares all nodes of a cluster to be able to install pacemaker.q

## Tasks includes

| Task                   | Description                                       |
| ---------------------- | ------------------------------------------------- |
| software_setup.yml     | enable repos and install cluster packages         |
| preconfig.yml          | set hacluster password                            |
| configure_firewall.yml | add high-availability ports to the firewalld      |
| cluster_prepare.yml    | enable cluster services and set pcs auth password |

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

| Name                                        | Description        | Value                       |
| ------------------------------------------- | ------------------ | --------------------------- |
| sap_ha_prepare_pacemaker_hacluster_password | hacluster password | sap_hana_hacluster_password |

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
