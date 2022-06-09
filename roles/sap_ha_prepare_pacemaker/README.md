# sap_ha_prepare_pacemaker Ansible Role

The role **sap_ha_prepare_pacemaker** is necessary because tasks needs to be finished on all nodes before the the cluster can be configured.
These tasks

*   Software Installation
*   Host authentication

are part of this role and excluded from the role **sap_ha_install_pacemaker**

## Include tasks used in sap_ha_install_pacemaker
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
