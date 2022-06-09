# sap_ha_prepare_pacemaker Ansible Roleo

The role Prepare Pacemaker is necessary because tasks needs to be finished on all nodes before the the cluster can be configured

Software Installation 
Host authentication

is part of this role and excluded from the role

sap_ha_install_pacemaker
  include_tasks: software_setup.yml
  include_tasks: preconfig.yml
  include_tasks: cluster_prepare.yml
item
platform
sap_hana_hacluster_password
sap_hana_instance_number
sap_hana_node1_hostname
sap_hana_node1_ip
sap_hana_node2_hostname
sap_hana_node2_ip
sap_hana_sid
sap_hana_system_role
sap_ha_prepare_pacemaker_hacluster_password
sap_ha_prepare_pacemaker_node1_hostname
sap_ha_prepare_pacemaker_node2_hostname
sap_ha_prepare_pacemaker_packages
sap_ha_prepare_pacemaker_rhsm_repos
vars['sap_ha_prepare_pacemaker_packages_'+sap_ha_prepare_pacemaker_type]
