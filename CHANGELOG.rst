===================================
community.sap_install Release Notes
===================================

.. contents:: Topics


v1.3.2
======

Release Summary
---------------

| Release Date: 2023-09-29
sap_general_preconfigure: Update to latest SAP documentation for RHEL 9 package libxcrypt-compat
sap_general_preconfigure: Bug fix for directory creation and SELinux Labels
sap_ha_pacemaker_cluster: Bug fix for AWS EC2 Virtual Servers
sap_ha_pacemaker_cluster: Bug fix for Google Cloud Compute Engine VM netmask lock on Virtual IP
sap_ha_pacemaker_cluster: Feature add for improved SAP NetWeaver HA compatibility
sap_ha_pacemaker_cluster: Feature add for ENSA1 compatibility
sap_ha_pacemaker_cluster: Feature add for SAP HA Interface Cluster Connector after cluster init
sap_ha_pacemaker_cluster: Feature add for IBM PowerVM hypervisor
sap_ha_pacemaker_cluster: Feature add for multiple network interfaces with Virtual IP
sap_hana_install: Bug fix for SELinux disable when SLES4SAP
sap_install_media_detect: Feature add for NFS compatibility
sap_install_media_detect: Feature add for idempotency
sap_install_media_detect: Feature add for new file detection after code restructure
sap_install_media_detect: Bug fix for setting SAP Maintenance Planner Stack XML path
sap_storage_setup: Feature add for Multipathing detection
sap_storage_setup: Bug fix for NFS throttle from customer test on MS Azure
sap_storage_setup: Bug fix for packages on SLES and Google Cloud
sap_swpm: Bug fix for RDBMS var name
sap_swpm: Bug fix for SAP HANA Client hdbuserstore connection
sap_swpm: Bug fix for SAP Maintenance Planner Stack XML path

v1.3.1
======

Release Summary
---------------

| Release Date: 2023-08-14
| sap_ha_pacemaker_cluster: Improved AWS constructs based on feedback
| sap_ha_pacemaker_cluster: Improved no STONITH resource definition handling
| sap_hana_install: Bug fix for arg spec on deprecated vars
| sap_hostagent: Bug fix for media handling
| sap_install_media_detect: Improved handling based on feedback
| sap_storage_setup: Bug fix for existing storage devices
| sap_swpm: Make full log output optional and replace with sapcontrol log final status
| collection: Bug fix for sample Ansible Playbooks

v1.3.0
======

Release Summary
---------------

| Release Date: 2023-07-21
| sap_general_preconfigure: Updates for new IBM Power packages with RHEL
| sap_hana_preconfigure: Updates for new IBM Power packages with RHEL
| sap_hana_install: Default Log Mode to normal and not Overwrite
| sap_ha_pacemaker_cluster: Detection of and compatibility for additional Infrastructure Platforms
| sap_ha_pacemaker_cluster: SAP NetWeaver compatibility added
| sap_install_media_detect: Restructure and add execution controls
| sap_storage_setup: Overhaul/Rewrite with breaking changes
| sap_storage_setup: SAP NetWeaver and NFS compatibility added
| sap_swpm: Minor alterations from High Availability test scenarios
| collection: Sample Playbooks updated

v1.2.3
======

Release Summary
---------------

| Release Date: 2023-04-25
| sap_hana_preconfigure: Some modifications for HANA on RHEL 9
| sap_ha_pacemaker_cluster: Compatibility for custom stonith resource definitions containing more than one element
| sap_hana_preconfigure: Be more flexible with IBM service and productivity tools


v1.2.2
======

Release Summary
---------------

| Release Date: 2023-02-01
| Fix for sap_hana_preconfigure on SLES when tuned is not installed


v1.2.1
======

Release Summary
---------------

| Release Date: 2023-01-26
| A few minor fixes


v1.2.0
======

Release Summary
---------------

| Release Date: 2022-12-20
| Consolidate sap_ha_install_pacemaker, sap_ha_prepare_pacemaker, and sap_ha_set_hana into new sap_ha_pacemaker_cluster role
| Use the ha_cluster Linux System Role and its enhanced features in the new role sap_ha_pacemaker_cluster
| Improve SID and instance checking in role sap_hana_install
| Enable modifying SELinux file labels for SAP directories
| Upgrade SAP SWPM handling for compatibility with more scenarios when generating inifile.params
| Add Ansible Role for basic Oracle DB installations for SAP
| Various minor enhancements
| Various fixes


v1.1.0
======

Release Summary
---------------

| Release Date: 2022-06-30
| Add SAP HANA Two-Node Scale-Up Cluster Installation


v1.0.3
======

Release Summary
---------------

| Release Date: 2022-05-13
| Initial Release on Galaxy

