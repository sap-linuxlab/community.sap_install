# Example Config to create a 2 node SAP HANA cluster

This directory contains an example how to configure a two node SAP HANA pacemaker cluster.
If you want to set up multiple environments, you can use a common playbook with the roles and a dedicated parameterfile per environment.
The easiest way is to put everything into one directory and all roles and parameters into a single playbook.

## Single Playbook Example
You can put everything into a single playbook file **example_in_one_file.yml***_. This example is used in a RHEVM environment. The fencing section might not fit to your environment and needs some changes. The file can also be downloaded.
```
---
- name: "Example SAP Hana and HA Cluster deployment on a 2-node cluster"
  hosts: hana1, hana2
  become: true

  vars:
    sap_ha_prepare_pacemaker_rhsm_repos:
      - "rhel-{{ ansible_distribution_major_version }}-for-{{ ansible_architecture }}-highavailability-e4s-rpms"

    sap_domain: example.com

    ## general + hana preconfigure
    # suppress reboot handler execution
    sap_general_preconfigure_reboot_ok: no
    sap_general_preconfigure_fail_if_reboot_required: no
    sap_hana_preconfigure_reboot_ok: no
    sap_hana_preconfigure_fail_if_reboot_required: no

    sap_hana_update_etchosts: yes         # usable in HSR role

    sap_hana_sid: 'DB1'
    sap_hana_instance_number: '00'
    sap_hana_install_master_password: 'DB1pass2'

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
        credential: "disable_http_filter=1 ipaddr=lu0529.wdf.sap.corp login='rhevuser@internal' password=G3h31m pcmk_host_map='hana01:hana01;hana02:hana02' power_wait=3 ssl=1 ssl_insecure=1"

  roles:

  # SAP Hana preparation and installation
    - name: sap_general_preconfigure
      tags:
        - sap_general_preconfigure
        - preconfigure

    - name: sap_hana_preconfigure
      tags:
        - sap_hana_preconfigure
        - preconfigure

    - name: sap_hana_install
      tags:
        - sap_hana_install

  # SAP Hana System Replication setup between 2 nodes
    - name: sap_ha_install_hana_hsr
      tags:
        - sap_ha_install_hana_hsr
        - hsr

  # 2-node Pacemaker Cluster Configuration
    - name: sap_ha_prepare_pacemaker
      tags:
        - sap_ha_prepare_pacemaker
        - pcs_prepare

    - name: sap_ha_install_pacemaker
      tags:
        - sap_ha_install_pacemaker

  # SAP Hana Cluster Resources Configuration
    - name: sap_ha_set_hana
      tags:
        - sap_ha_set_hana
```
This playbook is called with
```
ansible-playbook example_in_one_file.yml
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

```

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

*   roles
*   variables
*   call

### Roles used in the 2 node HANA Cluster example

Sequence|System Role|Description
:---:|:---|:---
1.|sap_general_preconfigure|System Preparation for SAP
2.| sap_hana_preconfigure|System Preparation for SAP HANA
3.|sap_hana_install|Installation of SAP HANA Database
4.|sap_ha_install_hana_hsr|Configuration of SAP HANA System Replication
5.|sap_ha_prepare_pacemaker|Authentication and Preparation of Nodes for Cluster Creation
6.|sap_ha_install_pacemaker|Initialization of the Pacemaker Cluster
7.|sap_ha_set_hana|Configuration of SAP HANA Resources for SAP Solutions

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
ansible-play example_play.yml 
```
