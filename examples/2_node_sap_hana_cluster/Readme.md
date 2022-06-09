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

##
