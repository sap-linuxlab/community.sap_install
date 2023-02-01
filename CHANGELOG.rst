===================================
community.sap_install Release Notes
===================================

.. contents:: Topics



v1.2.2
======

Release Summary
---------------

| Release Date: 2022-02-01
| Fix for sap_hana_preconfigure on SLES when tuned is not installed


v1.2.1
======

Release Summary
---------------

| Release Date: 2022-01-26
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

