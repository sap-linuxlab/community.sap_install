<!-- BEGIN Title -->
# sap_ha_pacemaker_cluster Ansible Role
<!-- END Title -->
![Ansible Lint for sap_ha_pacemaker_cluster](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_ha_pacemaker_cluster.yml/badge.svg)

## Description
<!-- BEGIN Description -->
Ansible Role `sap_ha_pacemaker_cluster` is used to install and configure Linux Pacemaker High Availability clusters for SAP HANA and SAP Netweaver systems on various infrastructure platforms.
<!-- END Description -->

<!-- BEGIN Dependencies -->
## Dependencies
- `fedora.linux_system_roles`
    - Roles:
        - `ha_cluster`

Install required collections by `ansible-galaxy install -vv -r meta/collection-requirements.yml`.
<!-- END Dependencies -->

<!-- BEGIN Prerequisites -->
## Prerequisites
Infrastructure:
- It is required to create them manually or using [sap_vm_provision](https://github.com/sap-linuxlab/community.sap_infrastructure/tree/main/roles/sap_vm_provision) role, because this role does not create any Cloud platform resources that are required by Resource Agents.

Managed nodes:
- Supported SAP system is installed. See [Recommended](#recommended) section.
- SAP HANA System Replication is configured for SAP HANA HA cluster. See [Recommended](#recommended) section.
- Operating system has access to all required packages
- All required ports are open (details below)

| SAP HANA System Replication process | Port |
| --- | --- |
| hdbnameserver<br/><sub> used for log and data shipping from a primary site to a secondary site.<br/>System DB port number plus 10,000</sub> | 4`<sap_hana_instance_number>`01 |
| hdbnameserver<br/><sub> unencrypted metadata communication between sites.<br/>System DB port number plus 10,000</sub> | 4`<sap_hana_instance_number>`02 |
| hdbnameserver<br/><sub> used for encrypted metadata communication between sites.<br/>System DB port number plus 10,000</sub> | 4`<sap_hana_instance_number>`06 |
| hdbindexserver<br/><sub> used for first MDC Tenant database schema</sub> | 4`<sap_hana_instance_number>`03 |
| hdbxsengine<br/><sub> used for SAP HANA XSC/XSA</sub> | 4`<sap_hana_instance_number>`07|
| hdbscriptserver<br/><sub> used for log and data shipping from a primary site to a secondary site.<br/>Tenant port number plus 10,000</sub> | 4`<sap_hana_instance_number>`40-97 |
| hdbxsengine<br/><sub> used for log and data shipping from a primary site to a secondary site.<br/>Tenant port number plus 10,000</sub> | 4`<sap_hana_instance_number>`40-97 |

| Linux Pacemaker process | Port |
| --- | --- |
| pcsd<br/><sub> cluster nodes requirement for node-to-node communication</sub> | 2224 (TCP)|
| pacemaker<br/><sub> cluster nodes requirement for Pacemaker Remote service daemon</sub> | 3121 (TCP) |
| corosync<br/><sub> cluster nodes requirement for node-to-node communication</sub> | 5404-5412 (UDP) |
<!-- END Prerequisites -->

## Execution
<!-- BEGIN Execution -->
**:warning: This ansible role will destroy and then recreate Linux Pacemaker cluster in process.**</br>
:warning: Do not execute this Ansible Role against existing Linux Pacemaker clusters unless you know what you are doing and you prepare inputs according to existing cluster.

Role can be executed independently or as part of [ansible.playbooks_for_sap](https://github.com/sap-linuxlab/ansible.playbooks_for_sap) playbooks.

### Supported Platforms
| Platform | Status | Notes |
| -------- | --------- | --------- |
| Physical server | :heavy_check_mark: | Need to specify valid fence agent |
| AWS EC2 Virtual Servers | :heavy_check_mark: | |
| Google Cloud Compute Engine Virtual Machine | :heavy_check_mark: | |
| Microsoft Azure Virtual Machines | :heavy_check_mark: | |
| IBM Cloud Virtual Server | :heavy_check_mark: | |
| IBM Power Virtual Server from IBM Cloud | :heavy_check_mark: | |
| IBM PowerVC hypervisor Virtual Machine | :heavy_check_mark: | |
| OVirt VM | :heavy_check_mark: | |

### Supported scenarios

| Platform | Variant | Status |
| -------- | --------- | --------- |
| SAP HANA scale-up (performance-optimized) 2 nodes | SAPHanaSR Classic | :heavy_check_mark: |
| SAP HANA scale-up (performance-optimized) 2 nodes | SAPHanaSR-angi | :heavy_check_mark: |
| SAP NetWeaver (ABAP) ASCS and ERS 2 nodes | Classic | :heavy_check_mark: |
| SAP NetWeaver (ABAP) ASCS and ERS 2 nodes | Simple Mount | :heavy_check_mark: |
<!-- END Execution -->

<!-- BEGIN Execution Recommended -->
### Recommended
It is recommended to execute this role together with other roles in this collection, in the following order:</br>
#### SAP HANA cluster
1. [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure)
2. [sap_hana_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_preconfigure)
3. [sap_install_media_detect](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_install_media_detect)
4. [sap_hana_install](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_install)
5. [sap_ha_install_hana_hsr](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_install_hana_hsr)
6. *`sap_ha_pacemaker_cluster`*

#### SAP Netweaver cluster
1. [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure)
2. [sap_netweaver_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_netweaver_preconfigure) 
3. [sap_install_media_detect](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_install_media_detect)
4. [sap_swpm](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_swpm)
5. *`sap_ha_pacemaker_cluster`*
<!-- END Execution Recommended -->

### Execution Flow
<!-- BEGIN Execution Flow -->
1. Assert that required inputs were provided.
2. Detect target infrastructure platform and prepare recommended inputs unless they were provided.
3. Prepare variables with all cluster parameters and resources.
4. Execute role `ha_cluster` from Ansible Collection `fedora.linux_system_roles` with prepared inputs.
5. Execute SAP product specific post tasks and verify cluster is running.
<!-- END Execution Flow -->

### Example
<!-- BEGIN Execution Example -->
```yaml
---
- name: Ansible Play for SAP HANA HA Scale-up cluster setup
  hosts: hana_primary, hana_secondary
  become: true
  tasks:
    - name: Execute Ansible Role sap_ha_pacemaker_cluster
      ansible.builtin.include_role:
        name: community.sap_install.sap_ha_pacemaker_cluster
      vars:
        sap_ha_pacemaker_cluster_cluster_name: clusterhdb
        sap_ha_pacemaker_cluster_hacluster_user_password: 'clusterpass'

        sap_ha_pacemaker_cluster_sap_type: saphana_scaleup
        sap_ha_pacemaker_cluster_host_type:
          - hana_scaleup_perf

        sap_ha_pacemaker_cluster_hana_sid: "H01"
        sap_ha_pacemaker_cluster_hana_instance_nr: "01"

        sap_ha_pacemaker_cluster_cluster_nodes:
          - node_name: h01hana0
            node_ip: "10.10.10.10"
            node_role: primary
            hana_site: DC01

          - node_name: h01hana1
            node_ip: "10.10.10.11"
            node_role: secondary
            hana_site: DC02
        sap_ha_pacemaker_cluster_replication_type: none
        sap_ha_pacemaker_cluster_vip_resource_group_name: viphdb
```
<!-- END Execution Example -->

<!-- BEGIN Role Tags -->
<!-- END Role Tags -->

<!-- BEGIN Further Information -->
## Further Information
Cluster can be further customized with inputs available from underlying role [ha_cluster](https://github.com/linux-system-roles/ha_cluster/blob/main/README.md), which will take precedence over `sap_ha_pacemaker_cluster` inputs.
<!-- END Further Information -->

## License
<!-- BEGIN License -->
Apache 2.0
<!-- END License -->

## Maintainers
<!-- BEGIN Maintainers -->
- [Janine Fuchs](https://github.com/ja9fuchs)
- [Marcel Mamula](https://github.com/marcelmamula)
<!-- END Maintainers -->

## Role Input Parameters
All input parameters used by role are described in [INPUT_PARAMETERS.md](https://github.com/sap-linuxlab/community.sap_install/blob/main/roles/sap_ha_pacemaker_cluster/INPUT_PARAMETERS.md)
