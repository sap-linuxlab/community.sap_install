# Example Config to create a 2 node SAP HANA cluster

This directory contains an example how to configure a 2
## Structure

*   role description
*   necessary parameter
*   common variables used
*   examples of usage

## Introduction

Starting with a 2 node HANA cluster. Additional configs will follow.

The installation is following the guidelines using the official documentation.

Besides the official documentation, before updating a config, it will be checked, if those updates are still necessary. In most cases, missing parts will also be recreated, if they are removed.

The automated install is more robust and much faster. The installation of a 2 node cluster should not take longer than 20 minutes.

Playbooks can be restarted and obsolete tasks will be skipped.

This is one improvement of the former collection. Additional, we have added common variables to keep the amount of variables low.

For example, sap_hana_sid or sap_hana_instance_number is used in 5 different roles. This example reduces the variables from 10 to 2.

## Example Setup
*   roles
*   variables
*   call

### Roles used in the 2 node HANA Cluster example
*   sap_general_preconfigure
*   sap_hana_preconfigure
*   sap_hana_install
*   sap_ha_install_hana_hsr
*   sap_ha_prepare_pacemaker
*   sap_ha_install_pacemaker
*   sap_ha_set_hana

## Setup Ansible
*   select management node
*   install hana package
*   choose a non root user for executing ansible
*   create ssh access to managed nodes
*   download github ***git clone https://github.com/sap-linuxlab/community.sap_install.git***
*   set access to roles using a link or config **ansible.cfg** on ansible management nodes
*   create your play directory form
**  Playbooks
**  group_vars directory
**  host_vars directory

## Example Files
*   hosts
**  inventory file
*   example_play.yml
**  example playbook to run the complete Installation
*   group_vars
**  group_vars directory including files
**  common settings to a group of managed nodes
*   host_vars
**  host_vars directory including files
**  contains files per host with host specific settings

### Example Settings for Example Files
* clustername **cluster1**
* node1 **hana01**
* node2 **hana02**
* etc.

### hosts
```
[cluster1]
hana01
hana02
```
### `host_vars/node1` example
```
# SAP Hana cluster definitions
sap_hana_system_role: primary
sap_hana_site_name: DC1
```

### `host_vars/node2` example
```
# SAP Hana cluster definitions
sap_hana_system_role: secondary
sap_hana_site_name: DC2

```
### `group_vars/cluster1.yml`
```
sap_domain: example.com

############ SAP node default values ############

# GENERAL PRECONFIGURE
sap_general_preconfigure_enable_repos: no
sap_general_preconfigure_use_netweaver_repos: no
sap_general_preconfigure_use_hana_repos: yes
sap_general_preconfigure_use_ha_repos: yes
sap_general_preconfigure_disable_all_other_repos: yes
sap_general_preconfigure_set_minor_release: yes
sap_general_preconfigure_min_package_check: yes
sap_general_preconfigure_update: yes
sap_general_preconfigure_reboot_ok: no
sap_general_preconfigure_fail_if_reboot_required: no
sap_general_preconfigure_selinux_state: disabled
sap_general_preconfigure_modify_etc_hosts: yes

# HANA PRECONFIGURE
sap_hana_preconfigure_config_all: yes
sap_hana_preconfigure_set_minor_release: yes
sap_hana_preconfigure_min_package_check: yes
sap_hana_preconfigure_reboot_ok: no
sap_hana_preconfigure_fail_if_reboot_required: no
sap_hana_preconfigure_use_netapp_settings_nfs: no
sap_hana_preconfigure_use_netapp_settings_nfsv3: no
sap_hana_preconfigure_use_tuned: yes
sap_hana_preconfigure_modify_grub_cmdline_linux: no
sap_hana_preconfigure_run_grub2_mkconfig: yes
# SAP HANA Default Values
sap_hana_sid: 'RH2'
sap_hana_instance_number: '02'
sap_hana_node1_ip: 192.168.1.11
sap_hana_node2_ip: 192.168.1.12
sap_hana_hacluster_password: 'redhat'
sap_hana_node1_hostname: hana01
sap_hana_node2_hostname: hana02
sap_hana_site1_name: DC01
sap_hana_site2_name: DC02
sap_ha_install_hana_hsr_fqdn: "example.com"
sap_ha_install_hana_hsr_rep_mode: sync
sap_ha_install_hana_hsr_oper_mode: logreplay
sap_ha_install_hana_hsr_hdbuserstore_system_backup_user: HDB_SYSTEMDB
sap_ha_install_hana_hsr_db_system_password: 'RedHat2022!'
sap_hana_install_master_password: RedHat202


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
sap_ha_install_pacemaker_stonith_credential: "ip=lu0123 username=user@internal passwd=S3cr3t"
sap_ha_install_pacemaker_stonith_parameters: 'pcmk_host_list="hana01;hana02" power_wait=3 ssl=1 ssl_insecure=1 disable_http_filter=1'
sap_ha_set_hana_vip1: 192.168.1.13

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
### Playbook `example_play.yml`
```
---
- hosts: cluster1
  debugger: on_failed
  collections:
    - community.sap_install
  become: true
  vars:
    sap_hana_sid: 'RH1'
# adding more variables here
  roles:
    - name: sap_general_preconfigure
      tags: sap_general_preconfigure, preconfigure
    - name: sap_hana_preconfigure
      tags: sap_hana_preconfigure, preconfigure
    - name: sap_hana_install
      tags: sap_hana_install, hana_install
    - name: sap_ha_install_hana_hsr
      tags: sap_ha_install_hana_hsr, hsr
    - name: sap_ha_prepare_pacemaker
      tags: sap_ha_prepare_pacemaker, pcs_prepare
    - name: sap_ha_install_pacemaker
      tags: sap_ha_install_pacemaker, pcs_install
    - name: sap_ha_set_hana
      tags: sap_ha_set_hana, hana_into_cluster
```

## Execution
You can execute this example with:
```
ansible-play example_play.yml --list_tasks
```
or you can run the playbook with:
```
ansible-play example_play.yml
```
