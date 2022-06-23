# Example Config to create a 2 node SAP HANA cluster

This directory contains an example how to configure a two node SAP HANA pacemaker cluster.
If you want to set up multiple environments, you can use a common playbook with the roles and a dedicated parameter file per environment.
The easiest way is to put everything into one directory and all roles and parameters into a single playbook. The roles can be cloned. 
If the directory of the playbook doesn't contains a roles directory with the roles used in the playbook, the roles path needs to be adapted.

## Single Playbook Example
You can put everything into a single playbook file **simples_one_file_example.yml***_. This example is used in a RHEVM environment. The fencing section might not fit to your environment and needs some changes. The file can also be downloaded. We are using plaein text passwords in the example. You can use vaulted passwords. Please check the ansible documentation. 
```

---
# call playbook with # ansible-playbook example_in_one_file.yml
- name: "Example SAP Hana and HA Cluster deployment on a 2-node cluster"
  hosts: hana1, hana2
  become: true

  vars:
    sap_domain: example.com

    sap_hana_sid: 'DB1'
    sap_hana_instance_number: '00'
    sap_hana_install_master_password: 'DB1pass2example_in_one_file'

    ### Cluster Definition
    sap_ha_install_pacemaker_cluster_name: cluster1
    sap_hana_hacluster_password: 'my_hacluster'

    sap_hana_cluster_nodes:
      - node_name: hana1
        node_ip: 10.240.128.6
        node_role: primary
        hana_site: DC01

      - node_name: hana2
        node_ip: 10.240.128.7
        node_role: secondary
        hana_site: DC02

    sap_ha_set_hana_vip1: 10.240.128.9

    sap_pacemaker_stonith_devices:
      - name: "fence_name_for_rhevm"
        agent: "fence_rhevm"
        credential: "disable_http_filter=1 ipaddr=lu0123.wdf.sap.corp login='rhevuser@internal' password=G3h31m pcmk_host_map='hana01:hana01;hana02:hana02' power_wait=3 ssl=1 ssl_insecure=1"

  roles:

    - sap_general_preconfigure
    - sap_hana_preconfigure
    - sap_hana_install
    - sap_ha_install_hana_hsr
    - sap_ha_prepare_pacemaker
    - sap_ha_install_pacemaker
    - sap_ha_set_hana
```
This playbook can be executed with
```
ansible-playbook simple_one_file_example.yml
```
## Variables Specifying a Two Node Cluster
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
example_in_one_file
```
## Rolesexample_in_one_file
To use the roles to setup a two node HANA cluster environment you need a section in your ansible playbookexample_in_one_file
```
  roles:
example_in_one_file
    - sap_general_preconfigure
    - sap_hana_preconfigure
    - sap_hana_install
    - sap_ha_install_hana_hsr
    - sap_ha_prepare_pacemaker
    - sap_ha_install_pacemaker
    - sap_ha_set_hana
```
## Execution
You can execute this example with:
```
ansible-play example_play.yml --list_tasks
ansible-play example_play.yml 
ansible-play example_play.yml --start_at_task <Taskname>
```
For more information please check KBA
