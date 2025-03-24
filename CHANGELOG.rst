====================================
community.sap\_install Release Notes
====================================

.. contents:: Topics

v1.5.3
======

Release Summary
---------------

Various enhancements and bug fixes

Bugfixes
--------

- collection - Cleanup the changelog(s) (https://github.com/sap-linuxlab/community.sap_install/pull/980)
- collection - Use the correct ansible-galaxy option in README.md files (https://github.com/sap-linuxlab/community.sap_install/pull/978)
- collection - gh issue templates (https://github.com/sap-linuxlab/community.sap_install/pull/987)
- collection and sap_hostagent - ansible-lint fixes (https://github.com/sap-linuxlab/community.sap_install/pull/973)
- sap*preconfigure - Use correct RHEL versions in task names (https://github.com/sap-linuxlab/community.sap_install/pull/976)
- sap*preconfigure - sysctl checks fail when config file has comments (https://github.com/sap-linuxlab/community.sap_install/pull/996)
- sap_*_preconfigure/SLES - Enhance saptune handling and detection (https://github.com/sap-linuxlab/community.sap_install/pull/994)
- sap_*_preconfigure/Suse - Enhance saptune revert logic (https://github.com/sap-linuxlab/community.sap_install/pull/983)
- sap_*_preconfigure/Suse - Switch saptune from present to latest (https://github.com/sap-linuxlab/community.sap_install/pull/952)
- sap_general_preconfigure - Fix check mode for sysctl (https://github.com/sap-linuxlab/community.sap_install/pull/950)
- sap_general_preconfigure - Remove unused file configure-etc-hosts.yml (https://github.com/sap-linuxlab/community.sap_install/pull/991)
- sap_general_preconfigure - Update the package name of the IBM Power tools for RHEL 10 (https://github.com/sap-linuxlab/community.sap_install/pull/998)
- sap_general_preconfigure - fix var role prefix (https://github.com/sap-linuxlab/community.sap_install/pull/948)
- sap_general_preconfigure, sap_maintain_etc_hosts - Ignore comments (https://github.com/sap-linuxlab/community.sap_install/pull/981)
- sap_general_preconfigure/SLES - Add etc hosts setup to configure steps (https://github.com/sap-linuxlab/community.sap_install/pull/992)
- sap_ha_pacemaker_cluster - fix ASCS constraint (https://github.com/sap-linuxlab/community.sap_install/pull/959)
- sap_ha_pacemaker_cluster - fix ASCS/ERS systemd (https://github.com/sap-linuxlab/community.sap_install/pull/963)
- sap_ha_pacemaker_cluster - fix NWAS (https://github.com/sap-linuxlab/community.sap_install/pull/972)
- sap_ha_pacemaker_cluster - fix internal-error (https://github.com/sap-linuxlab/community.sap_install/pull/966)
- sap_ha_pacemaker_cluster - fix package detection on RHEL (https://github.com/sap-linuxlab/community.sap_install/pull/947)
- sap_ha_pacemaker_cluster - fix(check-mode) (https://github.com/sap-linuxlab/community.sap_install/pull/986)
- sap_ha_pacemaker_cluster - several bug fixes (https://github.com/sap-linuxlab/community.sap_install/pull/965)
- sap_ha_pacemaker_cluster - stonith location constraints (https://github.com/sap-linuxlab/community.sap_install/pull/954)
- sap_hana_install - Update fapolicyd conditionals (https://github.com/sap-linuxlab/community.sap_install/pull/989)
- sap_hana_preconfigure - Fix check mode for largesend.conf - ppc64le (https://github.com/sap-linuxlab/community.sap_install/pull/956)
- sap_hana_preconfigure - Update the package name of the RHEL 10 Power tools (https://github.com/sap-linuxlab/community.sap_install/pull/958)
- sap_hana_preconfigure - fix check mode in two tasks (https://github.com/sap-linuxlab/community.sap_install/pull/953)
- sap_hana_preconfigure/SLES - Add package libltdl7 to vars (https://github.com/sap-linuxlab/community.sap_install/pull/993)
- sap_swpm - Fix link in README.md (https://github.com/sap-linuxlab/community.sap_install/pull/970)
- sap_swpm - remove duplicate section credentials_anydb_ibmdb2 (https://github.com/sap-linuxlab/community.sap_install/pull/995)
- sap_swpm - removed duplicates from credentials_hana section (https://github.com/sap-linuxlab/community.sap_install/pull/982)

v1.5.2
======

Release Summary
---------------

Various enhancements and bug fixes

Bugfixes
--------

- sap_*_preconfigure - Add code for RHEL 10 support (https://github.com/sap-linuxlab/community.sap_install/pull/938)
- sap_*_preconfigure/Suse - Rework of preconfigure roles for Suse, add missing notes. (https://github.com/sap-linuxlab/community.sap_install/pull/930)
- sap_general_preconfigure - Fix check mode (https://github.com/sap-linuxlab/community.sap_install/pull/935)
- sap_general_preconfigure - No longer install locale packages in RHEL 7 (https://github.com/sap-linuxlab/community.sap_install/pull/937)
- sap_netweaver_preconfigure - fix argument_specs validation error (https://github.com/sap-linuxlab/community.sap_install/pull/940)

v1.5.1
======

Release Summary
---------------

Various enhancements and bug fixes

Bugfixes
--------

- sap_*_preconfigure, sap_ha_pacemaker_cluster - Reworked loading vars (https://github.com/sap-linuxlab/community.sap_install/pull/910)
- sap_general_preconfigure - Implement SAP note 2369910 (https://github.com/sap-linuxlab/community.sap_install/pull/914)
- sap_ha_pacemaker_cluster - ANGI on RHEL and small improvements (https://github.com/sap-linuxlab/community.sap_install/pull/911)
- sap_ha_pacemaker_cluster - enable Simple Mount on RHEL (https://github.com/sap-linuxlab/community.sap_install/pull/931)
- sap_ha_pacemaker_cluster/SUSE - Rework SAPHanaSR-angi pre-steps and add SLES 16 vars (https://github.com/sap-linuxlab/community.sap_install/pull/928)
- sap_install_media_detect - Fix wrong sap_export_solman_java detection (https://github.com/sap-linuxlab/community.sap_install/pull/913)
- sap_swpm - Fix error when installing SAP NW750 JAVA or SOLMAN72SR2 JAVA instances (https://github.com/sap-linuxlab/community.sap_install/pull/916)
- sap_swpm - Fix error when using tag sap_swpm_generate_inifile (https://github.com/sap-linuxlab/community.sap_install/pull/918)
- sap_swpm - Use master password only when necessary (https://github.com/sap-linuxlab/community.sap_install/pull/920)
- sap_swpm, sap_general_preconfigure - Add variables for sap_install FQCN collection name for calling roles (https://github.com/sap-linuxlab/community.sap_install/pull/925)

v1.5.0
======

Release Summary
---------------

Various minor changes

Minor Changes
-------------

- collection - Add collection dependency for community.general (https://github.com/sap-linuxlab/community.sap_install/pull/808)
- collection - Modify for yamllint requirements (https://github.com/sap-linuxlab/community.sap_install/pull/811)
- feat - collection - Add playbook for direct execution (https://github.com/sap-linuxlab/community.sap_install/pull/842)
- feat - collection - Readme overhaul for all roles in collection (https://github.com/sap-linuxlab/community.sap_install/pull/873)
- feat - sap_ha_pacemaker_cluster - Enhance corosync totem handling with new dictionaries (https://github.com/sap-linuxlab/community.sap_install/pull/834)
- feat - sap_ha_pacemaker_cluster - GCP VIP reworked, Health check names updated (https://github.com/sap-linuxlab/community.sap_install/pull/863)
- feat - sap_ha_pacemaker_cluster - JAVA HA scenarios and complete refactor of role (https://github.com/sap-linuxlab/community.sap_install/pull/882)
- feat - sap_ha_pacemaker_cluster - New azure fence agent package for SUSE (https://github.com/sap-linuxlab/community.sap_install/pull/837)
- feat - sap_ha_pacemaker_cluster - Stonith SBD enablement (https://github.com/sap-linuxlab/community.sap_install/pull/829)
- feat - sap_hana_install - Implement an SAP HANA installation check only feature (https://github.com/sap-linuxlab/community.sap_install/pull/849)
- feat - sap_storage_setup - Add exact size disk check on top of approximate check (https://github.com/sap-linuxlab/community.sap_install/pull/839)
- feat - sap_storage_setup - Add support for HANA Scaleout NFS filesystems (https://github.com/sap-linuxlab/community.sap_install/pull/800)
- feat - sap_swpm - New improved and simplified version (https://github.com/sap-linuxlab/community.sap_install/pull/840)
- feat - sap_swpm - Option to enable SWPM observer mode (https://github.com/sap-linuxlab/community.sap_install/pull/749)
- sap_general_preconfigure - Use FQCN for import_role (https://github.com/sap-linuxlab/community.sap_install/pull/827)
- sap_general_preconfigure - Use the package module in most cases (https://github.com/sap-linuxlab/community.sap_install/pull/758)
- sap_ha_install_anydb_ibmdb2 - Append ibmcloud_vs (https://github.com/sap-linuxlab/community.sap_install/pull/815)
- sap_ha_pacemaker_cluster - Add override to use Classic SAPHanaSR agents (https://github.com/sap-linuxlab/community.sap_install/pull/806)
- sap_ha_pacemaker_cluster - GCP haproxy handling and new platform VIP dictionary (https://github.com/sap-linuxlab/community.sap_install/pull/862)
- sap_ha_pacemaker_cluster - Packages on AWS for RHEL (https://github.com/sap-linuxlab/community.sap_install/pull/857)
- sap_ha_pacemaker_cluster - vip resources must be first in ASCS/ERS resource groups (https://github.com/sap-linuxlab/community.sap_install/pull/872)
- sap_hana_install - Set the install execution mode to "optimized" (https://github.com/sap-linuxlab/community.sap_install/pull/896)
- sap_hana_install - Use polling for hdblcm (https://github.com/sap-linuxlab/community.sap_install/pull/805)
- sap_hana_preconfigure - Add RHEL 8.10 and 9.4 requirements (https://github.com/sap-linuxlab/community.sap_install/pull/869)
- sap_hana_preconfigure - Add compat-sap-c++-13 (https://github.com/sap-linuxlab/community.sap_install/pull/895)
- sap_hana_preconfigure - Allow setting THP to any possible value (https://github.com/sap-linuxlab/community.sap_install/pull/886)
- sap_hana_preconfigure - Enable TSX also for RHEL 9 (https://github.com/sap-linuxlab/community.sap_install/pull/797)
- sap_hana_preconfigure - No longer set net.core.somaxconn in RHEL 9 (https://github.com/sap-linuxlab/community.sap_install/pull/887)
- sap_hana_preconfigure - Refactor remove default saptune version (https://github.com/sap-linuxlab/community.sap_install/pull/818)
- sap_hana_preconfigure - Set THP to madvise from RHEL 9.2 onwards (https://github.com/sap-linuxlab/community.sap_install/pull/880)
- sap_hana_preconfigure - Sync with SAP note 3024346 v.10 for RHEL/NetApp (https://github.com/sap-linuxlab/community.sap_install/pull/816)
- sap_hana_preconfigure - Update azure override readme (https://github.com/sap-linuxlab/community.sap_install/pull/820)
- sap_hana_preconfigure - Zypper lock handler for SUSE (https://github.com/sap-linuxlab/community.sap_install/pull/796)
- sap_install_media_detect - AWS IGW slow impacts gpg key (https://github.com/sap-linuxlab/community.sap_install/pull/772)
- sap_install_media_detect - Allow disabling RAR handling (https://github.com/sap-linuxlab/community.sap_install/pull/856)
- sap_install_media_detect - Append loop labels (https://github.com/sap-linuxlab/community.sap_install/pull/781)
- sap_install_media_detect - Search known subdirs on re-run (https://github.com/sap-linuxlab/community.sap_install/pull/773)
- sap_netweaver_preconfigure - Rename package libcpupower1 for SLES4SAP 15 SP6 (https://github.com/sap-linuxlab/community.sap_install/pull/876)
- sap_netweaver_preconfigure - Sync with applicable SAP notes for Adobe DS (https://github.com/sap-linuxlab/community.sap_install/pull/888)
- sap_storage_setup - Defaults and documentation (https://github.com/sap-linuxlab/community.sap_install/pull/825)
- sap_swpm - Add default value for sap_swpm_java_scs_instance_hostname (https://github.com/sap-linuxlab/community.sap_install/pull/801)
- sap_swpm - Reduce the amount of empty lines in inifile.params (https://github.com/sap-linuxlab/community.sap_install/pull/822)
- sap_swpm - Remove the pids module (https://github.com/sap-linuxlab/community.sap_install/pull/786)
- sap_swpm - hdbuserstore default connection should use sap_swpm_db_schema_abap_password (https://github.com/sap-linuxlab/community.sap_install/pull/748)
- sap_swpm - sap_swpm_db_schema_password must be set explicitly for AAS (https://github.com/sap-linuxlab/community.sap_install/pull/760)

Bugfixes
--------

- sap_*_preconfigure - Edge case handling for SUSE packages
- sap_*_preconfigure - Fixes for testing with molecule (https://github.com/sap-linuxlab/community.sap_install/pull/807)
- sap_general_preconfigure - Reboot fix in handler (https://github.com/sap-linuxlab/community.sap_install/pull/892)
- sap_ha_install_anydb_ibmdb2 - Linting and sles bug fixes (https://github.com/sap-linuxlab/community.sap_install/pull/803)
- sap_ha_install_hana_hsr - Fixes to work for multiple secondaries (https://github.com/sap-linuxlab/community.sap_install/pull/866)
- sap_ha_pacemaker_cluster - Add python3-pip and NFS fix for Azure (https://github.com/sap-linuxlab/community.sap_install/pull/754)
- sap_ha_pacemaker_cluster - Fix UUID discovery for IBM Cloud VS (https://github.com/sap-linuxlab/community.sap_install/pull/903)
- sap_ha_pacemaker_cluster - Fix haproxy and minor lint issues (https://github.com/sap-linuxlab/community.sap_install/pull/898)
- sap_ha_pacemaker_cluster - Fix pcs resource restart (https://github.com/sap-linuxlab/community.sap_install/pull/769)
- sap_swpm - Add error notes to dev doc (https://github.com/sap-linuxlab/community.sap_install/pull/795)
- sap_swpm - Fix error when observer user defined, but empty and observer mode is on (https://github.com/sap-linuxlab/community.sap_install/pull/850)
- sap_swpm - Fix issues with localhost delegation on certain control nodes (https://github.com/sap-linuxlab/community.sap_install/pull/891)

v1.4.1
======

Release Summary
---------------

Various enhancements and bug fixes

Minor Changes
-------------

- collection - add sample AAS installation var file
- collection - fix ansible-test sanity errors
- collection - for package_facts Ansible Module add python3-rpm requirement for SLES
- collection - use -i instead of -l test scripts
- feat - sap_ha_pacemaker_cluster - ASCS ERS Simple Mount
- feat - sap_ha_pacemaker_cluster - compatibility enhancement for SLES
- feat - sap_ha_pacemaker_cluster - graceful SAP HANA start after PCMK Cluster start
- feat - sap_ha_pacemaker_cluster - handling for future merged Resource Agent package (SAPHanaSR-angi)
- feat - sap_ha_pacemaker_cluster - improved handling of custom SAP HANA srHooks
- feat - sap_ha_pacemaker_cluster - upgrade to ha_cluster Ansible Role with SLES compatibility
- feat - sap_hana_install - add compatibility for fapolicyd
- feat - sap_swpm - append generate options for s4hana java
- sap_*_preconfigure - disable and stop sapconf when saptune run
- sap_anydb_install_oracle - fix temp directory removal
- sap_general_preconfigure - fix /etc/hosts check in assert mode
- sap_general_preconfigure - revert to awk for asserting /etc/hosts
- sap_general_preconfigure - use tags for limiting the role scope
- sap_general_preconfigure - use the package module in most cases
- sap_general_preconfigure - use the role sap_maintain_etc_hosts - RHEL systems
- sap_ha_pacemaker_cluster - add retry for Azure Files (NFS) to avoid locks
- sap_ha_pacemaker_cluster - fix pcs resource restart
- sap_ha_pacemaker_cluster - use expect Ansible Module and add python3-pip requirement
- sap_ha_pacemaker_cluster - variable changes for different os and platforms
- sap_hana_install - update documentation for parameter sap_hana_install_force
- sap_hana_preconfigure - catch SELinux disabled
- sap_hana_preconfigure - move handlers to the correct location
- sap_hana_preconfigure - update kernel parameters for SLES
- sap_install_media_detect - detection of SAP Kernel Part I only
- sap_install_media_detect - directory handling fix for SAP SWPM
- sap_install_media_detect - duplicate SAR file handling for SAP Kernel, IGS, WebDisp
- sap_maintain_etc_hosts - fix wrong assert messages
- sap_maintain_etc_hosts - remove use ansible.utils.ip
- sap_netweaver_preconfigure - sync with SAP note 3119751 v.13 for RHEL
- sap_storage_setup - fix for TB disks
- sap_swpm - align execution and monitoring timeouts to 24hrs (86400s)
- sap_swpm - directory handling fix for SAP SWPM
- sap_swpm - optionally skip setting file permissions

v1.4.0
======

Release Summary
---------------

Various minor changes

Minor Changes
-------------

- collection - Move sap_hypervisor_node_preconfigure Role to sap_infrastructure Collection
- collection - Move sap_vm_preconfigure Role to sap_infrastructure Collection
- sap_anydb_install_oracle - Feature add for Oracle DB install with patch

v1.3.5
======

Release Summary
---------------

Various enhancements and bug fixes

Bugfixes
--------

- sap_hypervisor_node_preconfigure - Bug fix for role name and path for included tasks

v1.3.4
======

Release Summary
---------------

Various enhancements and bug fixes

Bugfixes
--------

- collection - Bug Fix for Ansible CVE-2023-5764
- collection - Bug Fix for Ansible Core minimum version update to 2.12.0 for import compliance with Ansible Galaxy
- collection - Bug fix for ansible-lint of each Ansible Role within Ansible Collection
- collection - Feature add for CodeSpell in git repository
- sap_general_preconfigure - Feature add for additional RHEL for SAP 8.8 and 9.2 release compatibility
- sap_ha_pacemaker_cluster - Feature add for Virtual IP and Constraints logic with Cloud Hyperscaler vendors
- sap_hana_preconfigure - Feature add for additional RHEL for SAP 8.8 and 9.2 release compatibility
- sap_hana_preconfigure - Feature add for compatibility with SLES using sapconf and SLES for SAP using saptune
- sap_hana_preconfigure - Feature add to reduce restrictions on new OS versions which are not yet supported by SAP
- sap_hypervisor_node_preconfigure - Bug fix for preconfiguration code structure of KVM (Red Hat Enterprise Virtualization) hypervisor nodes
- sap_hypervisor_node_preconfigure - Feature add for preconfiguration of KubeVirt (OpenShift Virtualization) hypervisor nodes
- sap_install_media_detect - Bug Fix for existing files
- sap_maintain_etc_hosts - Feature add for maintaining the /etc/hosts file of an SAP software host
- sap_netweaver_preconfigure - Feature add for compatibility with SLES using sapconf and SLES for SAP using saptune
- sap_swpm - Bug fix for runtime missing dependency python3-pip and advanced execution mode skipped tasks during certain installations
- sap_swpm - Feature add for basic System Copy executions in default mode

v1.3.3
======

Release Summary
---------------

Various enhancements and bug fixes

Bugfixes
--------

- collection - Make the preconfigure and sap_hana_install roles compatible with CVE-2023-5764

v1.3.2
======

Release Summary
---------------

Various enhancements and bug fixes

Bugfixes
--------

- sap_general_preconfigure - Bug fix for directory creation and SELinux Labels
- sap_general_preconfigure - Update to latest SAP documentation for RHEL 9 package libxcrypt-compat
- sap_ha_pacemaker_cluster - Bug fix for AWS EC2 Virtual Servers
- sap_ha_pacemaker_cluster - Bug fix for Google Cloud Compute Engine VM netmask lock on Virtual IP
- sap_ha_pacemaker_cluster - Feature add for ENSA1 compatibility
- sap_ha_pacemaker_cluster - Feature add for IBM PowerVM hypervisor
- sap_ha_pacemaker_cluster - Feature add for SAP HA Interface Cluster Connector after cluster init
- sap_ha_pacemaker_cluster - Feature add for improved SAP NetWeaver HA compatibility
- sap_ha_pacemaker_cluster - Feature add for multiple network interfaces with Virtual IP
- sap_hana_install - Bug fix for SELinux disable when SLES4SAP
- sap_install_media_detect - Bug fix for setting SAP Maintenance Planner Stack XML path
- sap_install_media_detect - Feature add for NFS compatibility
- sap_install_media_detect - Feature add for idempotency
- sap_install_media_detect - Feature add for new file detection after code restructure
- sap_storage_setup - Bug fix for NFS throttle from customer test on MS Azure
- sap_storage_setup - Bug fix for packages on SLES and Google Cloud
- sap_storage_setup - Feature add for Multipathing detection
- sap_swpm - Bug fix for RDBMS var name
- sap_swpm - Bug fix for SAP HANA Client hdbuserstore connection
- sap_swpm - Bug fix for SAP Maintenance Planner Stack XML path

v1.3.1
======

Release Summary
---------------

Various enhancements and bug fixes

Bugfixes
--------

- collection - Bug fix for sample Ansible Playbooks
- sap_ha_pacemaker_cluster - Improved AWS constructs based on feedback
- sap_ha_pacemaker_cluster - Improved no STONITH resource definition handling
- sap_hana_install - Bug fix for arg spec on deprecated vars
- sap_hostagent - Bug fix for media handling
- sap_install_media_detect - Improved handling based on feedback
- sap_storage_setup - Bug fix for existing storage devices
- sap_swpm - Make full log output optional and replace with sapcontrol log final status

v1.3.0
======

Release Summary
---------------

Various minor changes

Minor Changes
-------------

- collection - Sample Playbooks updated
- sap_general_preconfigure - Updates for new IBM Power packages with RHEL
- sap_ha_pacemaker_cluster - Detection of and compatibility for additional Infrastructure Platforms
- sap_ha_pacemaker_cluster - SAP NetWeaver compatibility added
- sap_hana_install - Default Log Mode to normal and not Overwrite
- sap_hana_preconfigure - Updates for new IBM Power packages with RHEL
- sap_install_media_detect - Restructure and add execution controls
- sap_storage_setup - Overhaul/Rewrite with breaking changes
- sap_storage_setup - SAP NetWeaver and NFS compatibility added
- sap_swpm - Minor alterations from High Availability test scenarios

v1.2.3
======

Release Summary
---------------

Various enhancements

Bugfixes
--------

- sap_ha_pacemaker_cluster - Compatibility for custom stonith resource definitions containing more than one element
- sap_hana_preconfigure - Be more flexible with IBM service and productivity tools
- sap_hana_preconfigure - Some modifications for HANA on RHEL 9

v1.2.2
======

Release Summary
---------------

Fix for sap_hana_preconfigure

Bugfixes
--------

- Fix for sap_hana_preconfigure on SLES when tuned is not installed

v1.2.1
======

Release Summary
---------------

A few minor fixes

Bugfixes
--------

- Various fixes

v1.2.0
======

Release Summary
---------------

Various minor changes

Minor Changes
-------------

- Add Ansible Role for basic Oracle DB installations for SAP
- Consolidate sap_ha_install_pacemaker, sap_ha_prepare_pacemaker, and sap_ha_set_hana into new sap_ha_pacemaker_cluster role
- Enable modifying SELinux file labels for SAP directories
- Improve SID and instance checking in role sap_hana_install
- Upgrade SAP SWPM handling for compatibility with more scenarios when generating inifile.params
- Use the ha_cluster Linux System Role and its enhanced features in the new role sap_ha_pacemaker_cluster
- Various other minor enhancements

Bugfixes
--------

- Various fixes

v1.1.0
======

Release Summary
---------------

New role for SAP HANA Two-Node Scale-Up Cluster Installation

Minor Changes
-------------

- Add SAP HANA Two-Node Scale-Up Cluster Installation

v1.0.3
======

Release Summary
---------------

Initial Release on Galaxy
