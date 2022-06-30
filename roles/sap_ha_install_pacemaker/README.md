# sap_ha_install_pacemaker Ansible Role

Ansible role for SAP Pacemaker Setup. This role needs **sap_ha_prepare_pacemaker** to be able to run. It creates a 2 node pacemaker cluster.

## Overview

The **sap_ha_install_pacemaker** role is part of this sequence:

| Sequence | System Role              | Description                                                  |
| :------: | :----------------------- | :----------------------------------------------------------- |
|    1.    | sap_general_preconfigure | System Preparation for SAP                                   |
|    2.    | sap_hana_preconfigure    | System Preparation for SAP HANA                              |
|    3.    | sap_hana_install         | Installation of SAP HANA Database                            |
|    4.    | sap_ha_install_hana_hsr  | Configuration of SAP HANA System Replication                 |
|    5.    | sap_ha_prepare_pacemaker | Authentication and Preparation of Nodes for Cluster Creation |
|    6.    | sap_ha_install_pacemaker | Initialization of the Pacemaker Cluster                      |
|    7.    | sap_ha_set_hana          | Configuration of SAP HANA Resources for SAP Solutions        |

The **sap_ha_install_pacemaker** creates a pacemaker cluster.
The necessary preparation is done in the role **sap_ha_prepare_pacemaker**.

## Tasks includes

| Task               | Description                         |
| ------------------ | ----------------------------------- |
| cluster_setup.yml  | create a cluster without ressources |
| stonith_config.yml | configure a stonith device          |

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

| Name                                     | Description                                            | Value                         |
| ---------------------------------------- | ------------------------------------------------------ | ----------------------------- |
| sap_ha_install_pacemaker_vip1            | VirtualIP address to the master database node          | sap_hana_vip1                 |
| sap_ha_install_pacemaker_vip2            | VirtualIP address to the slave database node (planned) | sap_hana_vip2                 |
| sap_ha_install_pacemaker_stonith_devices | parameter to configure stonith device                  | sap_pacemaker_stonith_devices |
| sap_ha_install_hana_hsr_rep_mode         | replication mode                                       | default is sync               |
| sap_ha_install_hana_hsr_oper_mode        | operation mode                                         | default is logreplay          |
| sap_pacemaker_stonith_devices            | description of the stonith device                      |

The stonith device needs to be - Please also check [SAP HANA scale-up Reference Architecture](https://cloud.google.com/solutions/sap/docs/sap-hana-ha-config-rhel)

```
sap_pacemaker_stonith_devices:    - Please also check [SAP HANA scale-up Reference Architecture](https://cloud.google.com/solutions/sap/docs/sap-hana-ha-config-rhel)

  - name: "fence_kdump1"
    agent: "fence_kdump"
    credential: "nodename='hana1'"
    parameters: "pcmk_host_list='hana1,hana2' pcmk_reboot_action='off'"
  - name: "fence_kdump2"
    agent: "fence_kdump"    - Please also check [SAP HANA scale-up Reference Architecture](https://cloud.google.com/solutions/sap/docs/sap-hana-ha-config-rhel)

    credential: "nodename='hana2'"
    parameters: "pcmk_host_list='hana1,hana2' pcmk_reboot_action='off'"

```

## Example Parameter File - Please also check [SAP HANA scale-up Reference Architecture](https://cloud.google.com/solutions/sap/docs/sap-hana-ha-config-rhel)

```
sap_hana_sid: 'DB1'
sap_hana_instance_number: '00'
sap_hana_install_master_password: 'my_hana-password'

### Cluster Definition
sap_ha_install_pacemaker_cluster_name: cluster1
sap_hana_hacluster_password: 'my_hacluster-password'
sap_pacemaker_stonith_devices:

sap_domain: example.com

sap_hana_cluster_nodes:
  - node_name: node1
    node_ip: 192.168.1.11
    node_role: primary
    hana_site: DC01

  - node_name: node2
    node_ip: 192.168.1.12    - Please also check [SAP HANA scale-up Reference Architecture](https://cloud.google.com/solutions/sap/docs/sap-hana-ha-config-rhel)

    node_role: secondary
    hana_site: DC02

sap_pacemaker_stonith_devices:
  - name: "fence_name_for_rhevm"
    agent: "fence_rhevm"
    credential: "disable_http_filter=1 ipaddr=lu0529.wdf.sap.corp login='rhevuser@internal' password=G3h31m pcmk_host_map='hana01:hana01;hana02:hana02' power_wait=3 ssl=1 ssl_insecure=1"

```

### Execution Design

Having the parameters specified as above, it can be executed with one command:

```
ansible-playbook example_playbook_with_parameters.yml
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

IBM Lab for SAP Solutions, Red Hat for SAP Community of Practice, Jason Masipiquena, Sherard Guico, Markus Moster
