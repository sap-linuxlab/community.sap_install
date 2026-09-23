<!-- BEGIN Title -->
# sap_hostagent Ansible Role
<!-- END Title -->

## Description
<!-- BEGIN Description -->
The Ansible Role `sap_hostagent` is used install SAP Host Agent.

SAP Host Agent is an agent that can accomplish several life-cycle management tasks, such as operating system monitoring, database monitoring, system instance control and provisioning.

This role installs SAP Host Agent with following source methods:

- **SAR file**
  - Source: SAP Software Center under product `SAP HOST AGENT`.

- **SAP bundle**
  - Source: SAP Software Center under products like `SAP HANA PLATFORM EDITION`.
  - These archives contain the `HOSTAGENT.TGZ` file used for installation.

- **RPM package** (Red Hat only)
  - Source: SAP Software Center under product `SAP HOST AGENT`.
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
1. Validate variables and paths to files. 
2. Detect existing installation.
3. Create temporary directory.
4. Execute installation based on chosen method.
5. Configure SSL if `sap_hostagent_config_ssl` was set.
6. Cleanup temporary directory
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
        sap_hostagent_sar_remote: true
        sap_hostagent_sar_remote_path: "/software/SAPHOSTAGENT"
        sap_hostagent_sar_file_name: "SAPHOSTAGENT44_44-20009394.SAR"
        sap_hostagent_sapcar_remote_path: "/software/SAPHOSTAGENT"
        sap_hostagent_sapcar_file_name: "SAPCAR_1311-80000935.EXE"
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
```
<!-- END Execution Example -->

<!-- BEGIN Role Tags -->
<!-- END Role Tags -->

<!-- BEGIN Further Information -->
## Further Information
### Using non-root user
It is recommended to execute this role with `root` user by using `become: true` on playbook level.<br>
Using `non-root` user with appropriate `sudo` privileges is also enabled, but not recommended.<br>
Additional package `acl` will be installed during installation to allow `sudo` from `non-root` to `sapadm` user.
<!-- END Further Information -->

## License
<!-- BEGIN License -->
Apache 2.0
<!-- END License -->

## Maintainers
<!-- BEGIN Maintainers -->
- [Markus Koch](https://github.com/rhmk)
- [Bernd Finger](https://github.com/berndfinger)
- [Marcel Mamula](https://github.com/marcelmamula)
<!-- END Maintainers -->

## Role Variables
<!-- BEGIN Role Variables -->
### Deprecated Variables
Temp directory variables were deprecated in favour of directory created by `ansible.builtin.tempfile` Ansible Module.

- `sap_hostagent_agent_tmp_directory`
- `sap_hostagent_clean_tmp_directory`


### sap_hostagent_installation_type
- _Type:_ `string`
- _Default:_ `rpm`

Select type of installation source for SAPHOSTAGENT.</br>
Available options: `sar`, `bundle`, `rpm`</br>
**NOTE: Option `sar-remote` was deprecated in favor of `sap_hostagent_sar_remote: true`.**

### sap_hostagent_overwrite
- _Type:_ `bool`
- _Default:_ `false`

Select if existing SAP Host Agent installation should be overwritten.<br>
Set to `true` to overwrite existing SAP Host Agent installation.<br>
Set to `false` to skip installation tasks if existing installation is detected.<br>
**NOTE: Using this option for 'sar' and 'bundle' will allow upgrade and downgrade of SAP Host Agent.**


### Input Parameters for SAR
Following input parameters are used by both Local SAR and Remote SAR.

#### sap_hostagent_sar_file_name
- _Type:_ `string`

File name of the SAR file.

#### sap_hostagent_sapcar_file_name
- _Type:_ `string`

File name of the SAPCAR executable.

#### sap_hostagent_sar_remote
- _Type:_ `bool`
- _Default:_ `false`

Select the method to provide SAR file and SAPCAR executable.<br>
Set to `true` if the files are located on the Managed Node.<br>
Set to `false` if the files are located on the Control Node.


### Input Parameters for Local SAR

#### sap_hostagent_sar_local_path
- _Type:_ `string`

Path to directory where SAR file is located on Control Node.</br>

#### sap_hostagent_sapcar_local_path
- _Type:_ `string`

Path to directory where SAPCAR executable is located on Control Node</br>


### Input Parameters for Remote SAR

#### sap_hostagent_sar_remote_path
- _Type:_ `string`

Path to directory where SAR file is located on Managed Node.</br>

#### sap_hostagent_sapcar_remote_path
- _Type:_ `string`

Path to directory where SAPCAR executable is located on Managed Node.</br>


### Input Parameters for RPM (Red Hat specific)

#### sap_hostagent_rpm_file_name
- _Type:_ `string`

File name of the RPM file.

#### sap_hostagent_rpm_remote
- _Type:_ `bool`
- _Default:_ `false`

Select the method to provide RPM file.<br>
Set to `true` if the RPM file is located on the Managed Node.<br>
Set to `false` if the RPM file is located on the Control Node.

#### sap_hostagent_rpm_local_path
- _Type:_ `string`

Path to directory where RPM file is located on Control Node.

#### sap_hostagent_rpm_remote_path
- _Type:_ `string`

Path to directory where RPM file is located on Managed Node.


### Input Parameters for SAP Bundle

#### sap_hostagent_bundle_path
- _Type:_ `string`

Path to directory where `HOSTAGENT.TGZ` file is located on Managed Node.


### Input Parameters for SSL setup

#### sap_hostagent_config_ssl
- _Type:_ `bool`
- _Default:_ `false`

Select if SSL should be configured for the SAP Host Agent after installation.</br>
Configuration includes PSE and CSR files creation.<br>
**NOTE: Signed CA certificate is not supported.**

#### sap_hostagent_ssl_passwd
- _Type:_ `string`

Password for the generated CSR file.

#### sap_hostagent_ssl_org
- _Type:_ `string`

Organization details for the generated CSR file.

#### sap_hostagent_ssl_country
- _Type:_ `string`

Country information for the generated CSR file.
<!-- END Role Variables -->