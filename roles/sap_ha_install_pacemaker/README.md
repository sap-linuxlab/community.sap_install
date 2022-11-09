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

| Task                        | Description                                     |
| --------------------------- | ----------------------------------------------- |
| check_status.yml            | check cluster status                            |
| cluster_setup.yml           | create a cluster without ressources             |
| stonith_sbd_node_config.yml | configure nodes for stonith via SBD             |
| stonith_sbd_config.yml      | configure cluster for stonith via SBD           |
| stonith_config.yml          | configure stonith devices (resource agents)     |

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

| Name                                                | Description                                            | Value                              |
| --------------------------------------------------- | ------------------------------------------------------ | ---------------------------------- |
| sap_ha_install_pacemaker_vip1                       | VirtualIP address to the master database node          | sap_hana_vip1                      |
| sap_ha_install_pacemaker_vip2                       | VirtualIP address to the slave database node (planned) | sap_hana_vip2                      |
| sap_ha_install_pacemaker_stonith_devices            | parameter to configure stonith device                  | sap_pacemaker_stonith_devices      |
| sap_ha_install_hana_hsr_rep_mode                    | replication mode                                       | default is sync                    |
| sap_ha_install_hana_hsr_oper_mode                   | operation mode                                         | default is logreplay               |
| sap_pacemaker_stonith_devices                       | description of the stonith device (define one or more) |                                    |
| sap_pacemaker_stonith_sbd_devices                   | block devices to use for SBD                           |                                    |
| sap_pacemaker_stonith_sbd_watchdog_module           | watchdog module to load and used for SBD               | softdog                            |
| sap_pacemaker_stonith_sbd_watchdog_module_blocklist | watchdog module to block and not be used for SBD       |                                    |
| sap_pacemaker_stonith_sbd_timeout_watchdog          | watchdog timeout written to SBD devices                | 30                                 |
| sap_pacemaker_stonith_sbd_timeout_msgwait           | msgwait timeout written to SBD devices                 | 60                                 |
| sap_pacemaker_stonith_timeout                       | stonith-timeout in the CIB                             | 900 (should be set to 90 for SBD ) |

## Stonith Device (resource agent)

A working stonith/fencing mechanism is mandatory when building pacemaker clusters. The stonith devices (resource agents) need to be described according to specific needs and environments:
  - environment agnostic (can be used everywhere)
    - fence_sbd / stonith:external/sbd
      - RHEL [Design Guidance for RHEL High Availability Clusters - sbd Considerations](https://access.redhat.com/articles/2941601) and [Exploring RHEL High Availability's Components - sbd and fence_sbd](https://access.redhat.com/articles/2943361)
      - SLES [Storage Protection and SBD](https://documentation.suse.com/sle-ha/12-SP4/html/SLE-HA-all/cha-ha-storage-protect.html)
    - fence_kdump (for diagnostics)
      - RHEL [How do I configure fence_kdump in a Red Hat Pacemaker cluster?](https://access.redhat.com/solutions/2876971)
      - SLES [Example STONITH resource configurations](https://documentation.suse.com/sle-ha/15-SP4/html/SLE-HA-all/cha-ha-fencing.html#sec-ha-fencing-config-examples)
  - AWS
    - fence_aws / stonith:external/ec2
      - RHEL [](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/deploying_red_hat_enterprise_linux_8_on_public_cloud_platforms/configuring-a-red-hat-high-availability-cluster-on-aws_deploying-a-virtual-machine-on-aws#aws-configuring-fencing_configuring-a-red-hat-high-availability-cluster-on-aws)
      - SLES [HA Cluster configuration on RHEL - Cluster resources - STONITH](https://docs.aws.amazon.com/sap/latest/sap-hana/sap-hana-on-aws-cluster-resources-1.html)
      - SLES [HA Cluster configuration on SLES - Cluster resources - STONITH](https://docs.aws.amazon.com/sap/latest/sap-hana/sap-hana-on-aws-stonith-device.html)
  - Azure
    - fence_azure_arm
      - RHEL [Setting up Pacemaker on Red Hat Enterprise Linux in Azure](https://learn.microsoft.com/en-us/azure/virtual-machines/workloads/sap/high-availability-guide-rhel-pacemaker)
      - SLES [Set up Pacemaker on SUSE Linux Enterprise Server in Azure](https://learn.microsoft.com/en-us/azure/virtual-machines/workloads/sap/high-availability-guide-suse-pacemaker)
  - GCP
    - fence_gce / gcpstonith
      - RHEL [SAP HANA scale-up Reference Architecture](https://cloud.google.com/solutions/sap/docs/sap-hana-ha-config-rhel)
      - SLES [SAP HANA scale-up Reference Architecture](https://cloud.google.com/solutions/sap/docs/sap-hana-ha-config-sles)
  - RHEV
    - fence_rhevm
      - RHEL [How do I configure a fence_rhevm stonith device in a Red Hat High Availability cluster?](https://access.redhat.com/solutions/3607691)
  - VMware
    - fence_vmware_rest
      - RHEL [How to configure a stonith device using agent fence_vmware_rest in a RHEL 7, 8 or 9 High Availability cluster with pacemaker?](https://access.redhat.com/solutions/3510461)

## Requirements, Dependencies and Testing

Tests are performed with other Ansible Roles in the sequence. Please refer to tests performed with final Ansible Roles:
- [sap_ha_set_hana Ansible Role - Requirements, Dependencies and Testing](../sap_ha_set_hana/README.md#requirements-dependencies-and-testing)
- [sap_ha_set_netweaver Ansible Role - Requirements, Dependencies and Testing](../sap_ha_set_netweaver/README.md#requirements-dependencies-and-testing)

## Example Parameter File

### general section

```
sap_hana_sid: 'DB1'
sap_hana_instance_number: '00'
sap_hana_install_master_password: 'my_hana-password'

### Cluster Definition
sap_ha_install_pacemaker_cluster_name: cluster1
sap_hana_hacluster_password: 'my_hacluster-password'

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

### stonith/fencing section

#### fencing via SBD

```
sap_ha_install_pacemaker_stonith_devices:
  - name: "fence_sbd"
    agent: "fence_sbd"
    parameters: >
      "devices={{ sap_pacemaker_stonith_sbd_devices | join(',') }}"
      "pcmk_delay_max=30"
sap_pacemaker_stonith_sbd_watchdog_module: 'softdog'
sap_pacemaker_stonith_sbd_watchdog_module_blocklist: 'iTCO_wdt'
sap_pacemaker_stonith_sbd_timeout_watchdog: '30'
sap_pacemaker_stonith_sbd_timeout_msgwait: '60'
sap_pacemaker_stonith_timeout: '90'
sap_pacemaker_stonith_sbd_devices:
  - "/dev/sde"
  - "/dev/sdf"
  - "/dev/sdg"
```

#### fencing on AWS

```
sap_ha_install_pacemaker_stonith_devices:
  - name: "fence_aws"
    agent: "fence_aws"
    parameters: >
      "region=<aws-region>"
      "access_key=<access-key>"
      "secret_key=<secret-access-key>"
      "pcmk_host_map=<primary-hostname>:<primary-instance-id>;<secondary-hostname>:<secondary-instance-id>"
      "pcmk_delay_max=45"
      "power_timeout=600 pcmk_reboot_timeout=600"
      "pcmk_reboot_retries=4"
```

#### fencing on Azure

```
sap_ha_install_pacemaker_stonith_devices:
  - name: "fence_azure_arm"
    agent: "fence_azure_arm"
    parameters: >
      "msi=true"
      "resourceGroup=<resourcegroup>"
      "subscriptionId=<subscriptionid>"
      "pcmk_host_map=<primary-hostname>:<primary-instance-id>;<secondary-hostname>:<secondary-instance-id>"
      "power_timeout=240 pcmk_reboot_timeout=900 pcmk_monitor_timeout=120 pcmk_monitor_retries=4 pcmk_action_limit=3 pcmk_delay_max=15"
      "op monitor interval=3600"
```

#### fencing on GCP

```
sap_ha_install_pacemaker_stonith_devices:
  - name: "fence_gce"
    agent: "fence_gce"
    parameters: >
      "project=<project>"
      "zone=<zone>"
```

#### fencing on RHEV

```
sap_ha_install_pacemaker_stonith_devices:
  - name: "fence_rhevm"
    agent: "fence_rhevm"
    parameters: >
      "ipaddr=<RHEV_Manager_IP/hostname>"
      "ssl_insecure=1 ssl=1"
      "login='<rhv_fencing_user@domain_name>'"
      "passwd=<password>"
      "pcmk_host_map='<pacemaker_node_name1>:<vm_name1>;<pacemaker_node_name2>:<vm_name2>'"
      "power_wait=3"
```

#### fencing on VMware

```
sap_ha_install_pacemaker_stonith_devices:
  - name: "fence_vmware_rest"
    agent: "fence_vmware_rest"
    parameters: >
      "pcmk_host_list=<vm_name1>,<vm_name2>"
      "ssl_insecure=1 ssl=1"
      "ipaddr={{ lookup('env', 'VMWARE_HOST')}}"
      "login={{lookup('env','VMWARE_USER')}}"
      "passwd={{lookup('env','VMWARE_PASSWORD')}}"
```

#### fencing with kdump (to gather additional logs)

```
sap_ha_install_pacemaker_stonith_devices:
  - name: "fence_kdump1"
    agent: "fence_kdump"
    credential: "nodename='hana1'"
    parameters: "pcmk_host_list='hana1,hana2' pcmk_reboot_action='off'"
  - name: "fence_kdump2"
    agent: "fence_kdump"
    credential: "nodename='hana2'"
    parameters: "pcmk_host_list='hana1,hana2' pcmk_reboot_action='off'"
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
