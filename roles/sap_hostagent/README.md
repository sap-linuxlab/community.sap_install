<!-- BEGIN Title -->
# sap_hostagent Ansible Role
<!-- END Title -->

## Description
<!-- BEGIN Description -->
Ansible Role `sap_hostagent` is used install SAP Host Agent.

SAP Host Agent is an agent that can accomplish several life-cycle management tasks, such as operating system monitoring, database monitoring, system instance control and provisioning.

This role installs SAP Host Agent with following source methods:
- SAP SAR file
- SAP Bundle
- RPM package (Red Hat only)
<!-- END Description -->

<!-- BEGIN Dependencies -->
<!-- END Dependencies -->

<!-- BEGIN Prerequisites -->
## Prerequisites
Managed nodes:
- Ensure that servers are configured for SAP Systems. See [Recommended](#recommended) section.
<!-- END Prerequisites -->

## Execution
<!-- BEGIN Execution -->
<!-- END Execution -->

<!-- BEGIN Execution Recommended -->
### Recommended
It is recommended to execute this role together with other roles in this collection, in the following order:</br>
1. [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure)
2. *`sap_hostagent`*
<!-- END Execution Recommended -->

### Execution Flow
<!-- BEGIN Execution Flow -->
1. Create temporary directory.
2. Execute deployment based on chosen method.
3. Configure SSL if `sap_hostagent_config_ssl` was set.
4. Cleanup temporary directory
<!-- END Execution Flow -->

### Example
<!-- BEGIN Execution Example -->
#### Example playbook for installing using SAR file located on control node
```yaml
---
- name: Ansible Play for SAP Host Agent installation - Local SAR
  hosts: all
  become: true
  tasks:
    - name: Execute Ansible Role sap_hostagent
      ansible.builtin.include_role:
        name: community.sap_install.sap_hostagent
      vars:  
        sap_hostagent_installation_type: "sar"
        sap_hostagent_sar_local_path: "/software/SAPHOSTAGENT"
        sap_hostagent_sar_file_name: "SAPHOSTAGENT44_44-20009394.SAR"
        sap_hostagent_sapcar_local_path: "/software/SAPHOSTAGENT"
        sap_hostagent_sapcar_file_name: "SAPCAR_1311-80000935.EXE"
        sap_hostagent_clean_tmp_directory: true
```
#### Example playbook for installing using SAR file located on managed node
```yaml
---
- name: Ansible Play for SAP Host Agent installation - Remote SAR
  hosts: all
  become: true
  tasks:
    - name: Execute Ansible Role sap_hostagent
      ansible.builtin.include_role:
        name: community.sap_install.sap_hostagent
      vars:  
        sap_hostagent_installation_type: "sar"
        sap_hostagent_sar_remote_path: "/software/SAPHOSTAGENT"
        sap_hostagent_sar_file_name: "SAPHOSTAGENT44_44-20009394.SAR"
        sap_hostagent_sapcar_remote_path: "/software/SAPHOSTAGENT"
        sap_hostagent_sapcar_file_name: "SAPCAR_1311-80000935.EXE"
        sap_hostagent_clean_tmp_directory: true
```
#### Example playbook for installing using SAP Bundle
```yaml
---
- name: Ansible Play for SAP Host Agent installation - SAP bundle
  hosts: all
  become: true
  tasks:
    - name: Execute Ansible Role sap_hostagent
      ansible.builtin.include_role:
        name: community.sap_install.sap_hostagent
      vars:  
        sap_hostagent_installation_type: "bundle"
        sap_hostagent_bundle_path: "/usr/local/src/HANA-BUNDLE/51053381"
        sap_hostagent_clean_tmp_directory: true
```
#### Example playbook for installing using RPM on Red Hat
```yaml
---
- name: Ansible Play for SAP Host Agent installation - SAP bundle
  hosts: all
  become: true
  tasks:
    - name: Execute Ansible Role sap_hostagent
      ansible.builtin.include_role:
        name: community.sap_install.sap_hostagent
      vars:  
        sap_hostagent_installation_type: "rpm"
        sap_hostagent_rpm_local_path: "/mylocaldir/SAPHOSTAGENT"
        sap_hostagent_rpm_file_name: "saphostagentrpm_44-20009394.rpm"
        sap_hostagent_clean_tmp_directory: true
```
<!-- END Execution Example -->

<!-- BEGIN Role Tags -->
<!-- END Role Tags -->

<!-- BEGIN Further Information -->
<!-- END Further Information -->

## License
<!-- BEGIN License -->
Apache 2.0
<!-- END License -->

## Maintainers
<!-- BEGIN Maintainers -->
- [Markus Koch](https://github.com/rhmk)
- [Bernd Finger](https://github.com/berndfinger)
<!-- END Maintainers -->

## Role Input Parameters
All input parameters used by role are described in [INPUT_PARAMETERS.md](https://github.com/sap-linuxlab/community.sap_install/blob/main/roles/sap_hostagent/INPUT_PARAMETERS.md)
