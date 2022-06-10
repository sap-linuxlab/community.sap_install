# sap_ha_prepare_pacemaker Ansible Role

The role **sap_ha_prepare_pacemaker** is necessary because tasks needs to be finished on all nodes before the the cluster can be configured.
These tasks

*   Software Installation
*   Host authentication

are part of this role and excluded from the role **sap_ha_install_pacemaker**

## Usage Example
The examples contains
playbook
```
hosts: cluster1
roles:
    - sap_general_preconfigure
    - sap_hana_preconfigure
    - sap_ha_install_hana_hsr
    - sap_ha_prepare_pacemaker
    - sap_ha_install_pacemaker
    - sap_ha_set_hana
```

inventory (i.e. `/etc/ansible/hosts`) example
```
[cluster1]
node1
node2
```

`host_vars/node1` example
```

```

`host_vars/node2` example
```

```

`group_vars/cluster1` example
```
# SAP HANA Default Values
sap_hana_sid: RH2
sap_hana_instance_number: '02'
sap_hana_install_master_password: RedHat202
sap_hana_node1_hostname: hana05
sap_hana_node2_hostname: hana06
sap_hana_node1_ip: 192.168.5.81
sap_hana_node2_ip: 192.168.5.82
sap_hana_hacluster_password: 'redhat'
sap_hana_site1_name: DC01
sap_hana_site2_name: DC02
sap_domain: example.com
sap_hana_systemdb_password: 'RedHat2022!'
 
### Specific variables per node
sap_general_preconfigure_max_hostname_length: 128
sap_general_preconfigure_update: no
sap_general_preconfigure_selinux_state: 'permissive'

# pacemaker vars
## Cluster Vars
sap_ha_install_pacemaker_cluster_name: cluster1
sap_ha_install_pacemaker_hacluster_password: redhat

### Stonith Vars
sap_ha_install_pacemaker_stonith_name: 'auto_rhevm_fence'
sap_ha_install_pacemaker_stonith_fence_agent: 'fence_rhevm'
sap_ha_install_pacemaker_stonith_credential: "ip=lu0529 username=amemon@internal passwd=redhat04"
sap_ha_install_pacemaker_stonith_parameters: 'pcmk_host_map="hana05:Auto_hana_01;hana06:Auto_hana_02" power_wait=3 ssl=1 ssl_insecure=1 disable_http_filter=1'
sap_ha_set_hana_vip1: 192.168.5.83

sap_ha_stonith_device:
  - name: "auto_rhevm_fence1"
    agent: "fence_rhevm"
    credential: "ip=lu0529 username=amemon@internal passwd=redhat04"
    parameters: "pcmk_host_map='hana05:Auto_hana_01;hana06:Auto_hana_02' power_wait=3 ssl=1 ssl_insecure=1 disable_http_filter=1"
  - name: "auto_rhevm_fence2"
    agent: "fence_rhevm"
    credential: "ip=lu0529 username=amemon@internal passwd=redhat04"
    parameters: 'pcmk_host_map="hana05:Auto_hana_01;hana06:Auto_hana_02" power_wait=3 ssl=1 ssl_insecure=1 disable_http_filter=1'

```

## Include tasks used in sap_ha_prepare_pacemaker
  Task Name|Description
  ---|---
  software_setup.yml|Install necessary software packages
  preconfig.yml|set password for hacluster user
  cluster_prepare.yml|set pcs auth for cluster nodes

## Recommended Variables

The following common variables are set once for multiple system roles. We recommend to use these common shared variables to simplify variable definitions.

Variable Name|Description
---|---
sap_hana_node1_hostname|name of first node
sap_hana_node2_hostname|name of second node
sap_hana_hacluster_password|password for `hacluster` user

##  Usage of this role
Simply add to your playbook file:

```
collections:
  - community.sap_install
sap_ha_prepare_pacemaker
```
If there is a **roles** subdirectory in the same location where the playbook is stored, containing the roles for the SAP HA HANA installation, you can simply use
```
sap_ha_prepare_pacemaker
```

## Role Variables

Variable Name|Description|Default Value
---|---|---
sap_ha_prepare_pacemaker_hacluster_password|hacluster password|sap_hana_hacluster_password
sap_ha_prepare_pacemaker_node1_hostname|name of first node|sap_hana_node1_hostname
sap_ha_prepare_pacemaker_node2_hostname|name of second node|sap_hana_node2_hostname
sap_ha_prepare_pacemaker_packages|list of packages to install|pcs, pacemaker, nfs-util, fence-agents-all, resource-agents-sap-hana
sap_ha_prepare_pacemaker_rhsm_repos|list of necessary repos|list of repos is part of the collection
