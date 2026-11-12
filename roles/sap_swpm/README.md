<!-- BEGIN Title -->
# sap_swpm Ansible Role
<!-- END Title -->
![Ansible Lint for sap_swpm](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_swpm.yml/badge.svg)

## Description
<!-- BEGIN Description -->
The Ansible role `sap_swpm` installs various SAP Systems installable by SAP Software Provisioning Manager (SWPM).
<!-- END Description -->

<!-- BEGIN Dependencies -->
<!-- END Dependencies -->

## Prerequisites
<!-- BEGIN Prerequisites -->
Managed nodes:

- Directory with SAP Installation media is present and `sap_swpm_software_path` updated. Download can be completed using [community.sap_launchpad](https://github.com/sap-linuxlab/community.sap_launchpad).
- Ensure that servers are configured for SAP Systems. See [Recommended](#recommended) section.
- Ensure that volumes and filesystems are configured correctly. See [Recommended](#recommended) section.

### Prepare SAP installation media
Place a valid SAPCAR executable file in a directory specified by variable `sap_swpm_sapcar_path` (e.g. /software/sapcar). Example: `SAPCAR_1300-70007716.EXE`

Place a valid SWPM SAR file in a directory specified by variable `sap_swpm_path` (e.g. /software/sap_swpm). Example: `SWPM20SP23_0-80003424

Place the following files in a directory specified by variable `sap_swpm_software_path` (e.g. /software/sap_swpm_download_basket):

  - For a new installation
      - Download the appropriate software from SAP Software Download Center, Maintenance Planner, etc.
  - For a restore or new installation
      - SAP IGS                   - `igs*.sar`
      - SAP IGS HELPER            - `igshelper*sar`
      - SAP Host Agent            - `SAPHOSTAGENT*SAR`
      - SAP Kernel DB             - `SAPEXEDB_*SAR`
      - SAP Kernel DB Independent - `SAPEXE_*SAR`
      - SAP HANA Client           - `IMDB_CLIENT*SAR`

Alternatively, you can place all the files mentioned above into a single directory and use the role [sap_install_media_detect](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_install_media_detect) to identify the required files<br>
and set the role variables automatically so that the role `sap_swpm` has access to all the files needed for a successful installation of SAP System.
<!-- END Prerequisites -->

## Execution
<!-- BEGIN Execution -->
### SWPM Variable Precedence
This section applies to SWPM Specific variables only, which describe the SAP System and its installation (see [Mandatory SWPM Specific Variables](#mandatory-swpm-specific-variables) and the SWPM variable sections that follow).<br>
For these variables the role resolves values itself, independently of Ansible variable precedence. The first source that provides a value wins.

> **NOTE: Role Specific variables are not part of this precedence.**<br>
> Variables that control how the role runs on the managed host (e.g. `sap_swpm_run_sapinst`, `sap_swpm_force`, `sap_swpm_db_load_force`, `sap_swpm_configure_firewall`, `sap_swpm_update_etchosts`, `sap_swpm_set_file_permissions`, file permission and ownership variables)
> are always read directly from role variables, using standard Ansible variable precedence.<br>
> They must be defined as role variables (extravars, vars, inventory or play). A value set for them in an existing inifile, `sap_swpm_role_parameters_dict` or `sap_swpm_templates_install_dictionary` has no effect.

#### Existing inifile is found
1. Parsed from the inifile if found with a value: product ID, software path, SID, FQDN. They take precedence over all other sources.
2. The `sap_swpm_role_parameters_dict` and role variables fill the remaining values needed by the pre tasks, in this order.
3. Fallback to `sap_swpm_software_path` for `sap_swpm_sapcar_path` and `sap_swpm_path`, if undefined or empty.
4. The `sap_swpm_templates_install_dictionary` is skipped.
5. The `sap_swpm_inifile_sections_list` and `sap_swpm_inifile_parameters_dict` are skipped, because inifile generation is skipped.

#### Existing inifile is not found
1. The `sap_swpm_role_parameters_dict`, if defined: It overrides role variables and their defaults, including Booleans. Only keys starting with `sap_swpm_` are used.
2. Role variables: Booleans are always used, other values only if not empty.
3. The `sap_swpm_templates_install_dictionary` fills values not set by previous sources.
4. Fallback to `sap_swpm_software_path` for `sap_swpm_sapcar_path` and `sap_swpm_path`, if undefined or empty.
5. Fallback for selected variables depending on sections in `sap_swpm_inifile_sections_list`, if undefined or empty.
> After the inifile is generated, `sap_swpm_inifile_parameters_dict` updates its parameters.

### SAP System Detection
The role detects existing SAP System and Instances to ensure its execution does not damage existing installation.<br>
Detection follows set of rules, unless it is skipped with `sap_swpm_skip_detection: true` or overriden with `sap_swpm_force: true`.<br>

Following checks are executed during detection workflow:
1. Existence of `saphostctrl` and if its output contains SID and Instance Numbers.
2. Existence of `sapcontrol` and if its output contains SID and Instance Numbers.
3. Existence of files in known SAP directories.
4. Existence of `/usr/sap/sapservices` and if it contains SID and Instance Numbers.
5. Existence of SAP System profiles for SID and Instance Numbers.

Outcome of detection is based on these checks and what they indicate:
- **Installation executed**: Nothing found by any check.
- **Installation skipped**: Checks found existing SAP System with same SID and Instance Numbers.
- **Failure**: The `saphostctrl` and `sapcontrol` did not detect SAP System, but files, sapservices or profiles indicate something exists. This could indicate invalid installation, so the role execution is stopped with failure.

> NOTE: Existing `sapadm` and `sidadm` users with group `sapsys` are also checked, but their existence is resulting in warning only if their IDs do not align with IDs defined in role variables.

> NOTE: Products with special rules, like Database Load, do not produce failure during SAP detection, but instead they are handled during variable validation.<br>
> **See [Database Load Safety](#database-load-safety) for more information**.
<!-- END Execution -->

<!-- BEGIN Execution Recommended -->
### Recommended
It is recommended to execute this role together with other roles in this collection, in the following order:

1. [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure)
2. [sap_netweaver_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_netweaver_preconfigure)
3. [sap_install_media_detect](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_install_media_detect)
4. *`sap_swpm`*

**NOTE:** For most scenarios, a database like SAP HANA must be available. Use the role [sap_hana_install](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_install) for installing the SAP HANA database.
<!-- END Execution Recommended -->

### Execution Flow
<!-- BEGIN Execution Flow -->
#### Validation
- Variables are loaded and validated in order described in [SWPM Variable Precedence](#swpm-variable-precedence).

#### Pre-Tasks
- New inifile is generated based on sections in `sap_swpm_inifile_sections_list` using jinja2 template `inifile_params.j2`, if existing inifile was not found.
  - After the inifile is generated, `sap_swpm_inifile_parameters_dict` updates its parameters.

- Existing SAP System and Instances are detected and the role proceeds based on [SAP System Detection](#sap-system-detection) rules.

- Determine installation type based on SAP Product Catalog ID defined in the `sap_swpm_product_catalog_id`.<br>
  Additional task are executed for High Avalability and System Restore products.

- Find `SAPCAR` files in the `sap_swpm_sapcar_path` and `SWPM` files in the `sap_swpm_path`.

- Find other SAR files (e.g. `SAPEXE`, `SAPEXEDB`, `igsexe`, `igshelper`) in the `sap_swpm_software_path`, if the `sap_swpm_generic` is set to `false` (Default: `false`).

- (Optional) Update `/etc/hosts` if `sap_swpm_update_etchosts` is set to `true` (Default: `false`).

- (Optional) Do not disable password expiry if `sap_swpm_set_sidadm_noexpire` is set to `false` (Default: `true`).

- (Optional) Apply firewall rules for SAP Instances if `sap_swpm_configure_firewall` is set to `true` (Default: `false`).

#### SAP SWPM

- Execute SWPM with shown command that can be used to watch status and progress.

> NOTE: This and the remaining steps can be skipped by setting the default of the parameter `sap_swpm_run_sapinst` to `false`.

#### Post-Install

- Set expiry of Linux created users to `never`, if the `sap_swpm_set_sidadm_noexpire` is set to `true` (Default: `true`).

- Update SAP HANA connection details in `hdbuserstore`, if present. 

- Restart `saphostexec` process if the `sap_swpm_install_saphostagent` is set to `true` (Default: `true`).

- (Optional) Handle the execution of SUM if SWPM started it. See [Up-To-Date Installation](#up-to-date-installation-udi) for more information.
<!-- END Execution Flow -->

### Example
<!-- BEGIN Execution Example -->

#### Installation of SAP ABAP ASCS instance in distributed system
- The [sap_install_media_detect](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_install_media_detect) role is used to prepare installation media and to set required variables for `sap_swpm` role.
- Example is based on `sap_s4hana_distributed_ha` scenario from [ansible.playbooks_for_sap](https://github.com/sap-linuxlab/ansible.playbooks_for_sap).

```yaml
---
- name: Ansible Play for ASCS installation
  hosts: nwas_ascs
  become: true
  any_errors_fatal: true
  max_fail_percentage: 0
  tasks:

    - name: Execute Ansible Role sap_install_media_detect
      ansible.builtin.include_role:
        name: community.sap_install.sap_install_media_detect
      vars:
        sap_install_media_detect_swpm: true
        sap_install_media_detect_hostagent: true
        sap_install_media_detect_igs: true
        sap_install_media_detect_kernel: true
        sap_install_media_detect_webdisp: false
        sap_install_media_detect_source_directory: /software

    - name: Execute Ansible Role sap_swpm
      ansible.builtin.include_role:
        name: community.sap_install.sap_swpm
      vars:
        sap_swpm_sid: AE1
        sap_swpm_virtual_hostname: ae1ascs
        sap_swpm_ascs_instance_nr: "01"
        sap_swpm_master_password: "Password@1"  # Do not use, this is example only!
        sap_swpm_ddic_000_password: "Password@1"  # Do not use, this is example only!
        sap_swpm_sapadm_uid: "3000"
        sap_swpm_sapsys_gid: "3001"
        sap_swpm_sidadm_uid: "3001"
        sap_swpm_product_catalog_id: NW_ABAP_ASCS:NW750.HDB.ABAPHA
        sap_swpm_inifile_sections_list:
          - swpm_installation_media
          - swpm_installation_media_swpm1
          - credentials
          - credentials_hana
          - db_config_hana
          - db_connection_nw_hana
          - nw_config_other
          - nw_config_central_services_abap
          - nw_config_ports
          - nw_config_host_agent
          - sap_os_linux_user
```

> NOTE: See repository level `playbooks` directory for more examples.

<!-- END Execution Example -->

<!-- BEGIN Role Tags -->
### Role Tags

> **Following tasks are always executed, regardless of any tags:**<br>
> - **Validation** - Validation of role variables is always executed to ensure that all subsequent tasks are executed on valid values.<br>
> - **Cleanup** - Cleanup tasks are executed every time temporary directory and files are created during role execution.<br>
> - Preservation (conditional) - Generated sapinst inifile is preserved in the `sap_swpm_software_path` directory if failure occured during execution, or tag `sap_swpm_generate_inifile` was used or the variable `sap_swpm_run_sapinst` is set to `false`.

With the following tags, the role can be called to perform certain activities only:

- `sap_swpm_generate_inifile`: Generates sapinst inifile regardless of whether existing inifile is present, without running any other tasks.<br>
  The file is saved in the `sap_swpm_software_path` directory with SAP System specific prefix (e.g. `inifile_AE1_NW_ABAP_OneHost.params`).<br>
  This can be used to check if the inifile is created as desired.
- `sap_swpm_sapinst_commandline`: Prepares the sapinst command that would be executed and outputs it.<br>
  **NOTE: Command show path to sapinst inifile, but it is not generated when only this tag is used!**
- `sap_swpm_pre_install`: Performs all pre tasks and exits before execution of sapinst command.
- `sap_swpm_configure_firewall`: Performs the firewall configuration tasks when the variable `sap_swpm_configure_firewall` is set to `true`.
- `sap_swpm_update_etchosts`: Performs update of `/etc/hosts` file when the variable `sap_swpm_update_etchosts` and `sap_swpm_run_sapinst` are set to `true`.
<!-- END Role Tags -->

<!-- BEGIN Further Information -->
## Further Information
<!-- BEGIN UDI -->
### Up-To-Date Installation (UDI)
The Software Update Manager can run on any host with an Application Server instance (e.g. NWAS ABAP PAS/AAS, NWAS JAVA CI/AAS) with correct permissions to access `/usr/sap/` and `/sapmnt/` directories.

When using the Software Provisioning Manager (SWPM) with a Maintenance Planner Stack XML file to perform an "up-to-date installation" (UDI) - it will start the Software Update Manager (SUM) automatically at the end of the installation process.<br>
This UDI feature applies only to SAP ABAP Platform / SAP NetWeaver, and must be performed from the Primary Application Server instance (i.e. NWAS ABAP PAS, or a OneHost installation).

Furthermore, during SWPM variable selection the enabling of Transport Management System (TMS) is required, see SAP Note 2522253 - SWPM can not call SUM automatically when doing the up-to-date installation.
<!-- END UDI -->

### Database Load Safety
SAP Product Catalog ID defined in the `sap_swpm_product_catalog_id` is parsed for known pattern and indicators for special cases.<br>
Database Load is detected if either `NW_ABAP_DB` or `NW_Java_DB` is contained in start of the string.

This results in immediate failure of execution, unless the `sap_swpm_db_load_force` is set to `true`.

**This is considered as explicit acknowledgement of all risks involved with targeting existing installation!**

**Running SWPM against an existing database WILL DROP and recreate the schema user, causing DATA LOSS on existing systems!**

> NOTE: The `sap_swpm_force` does not override this safety check.
<!-- END Further Information -->

## License
<!-- BEGIN License -->
Apache 2.0
<!-- END License -->

## Maintainers
<!-- BEGIN Maintainers -->
- [Bernd Finger](https://github.com/berndfinger)
- [Sean Freeman](https://github.com/seanfreeman)
- [Marcel Mamula](https://github.com/marcelmamula)
<!-- END Maintainers -->

## Role Variables
<!-- BEGIN Role Variables -->
> **NOTE: Deprecated Variables:**
> - `sap_swpm_ansible_role_mode` was removed in release `1.5.0` in favor of `sap_swpm_inifile_sections_list`.
> - The following variables are deprecated and the role displays a warning when they are used.<br>
>   The deprecated variable is used only if its replacement is not set.
>
> | Deprecated variable | Replacement |
> | --- | --- |
> | `sap_swpm_swpm_path` | `sap_swpm_path` |
> | `sap_swpm_swpm_sar_file_name` | `sap_swpm_file_name` |
> | `sap_swpm_swpm_remote_access_user` | `sap_swpm_remote_access_user` |
> | `sap_swpm_swpm_observer_mode` | `sap_swpm_observer_mode` (deprecated variable is used only if set to `true`) |
> | `sap_swpm_inifile_list` | `sap_swpm_inifile_sections_list` |
> | `sap_swpm_inifile_custom_values_dictionary` | `sap_swpm_inifile_parameters_dict` |
> | `sap_swpm_inifile_dictionary` | `sap_swpm_role_parameters_dict` |
>
> Deprecated variable names are not mapped when used as keys inside `sap_swpm_role_parameters_dict`.

<!-- BEGIN Mandatory Role Specific Variables -->
### Mandatory Role Specific Variables

#### sap_swpm_run_sapinst
- _Type:_ `bool`
- _Default:_ `true`

The variable that controls whether the sapinst command will be executed.<br>
Set to `false` to skip execution of sapinst.

#### sap_swpm_update_etchosts
- _Type:_ `bool`
- _Default:_ `false`

The variable that controls whether the role will update the `/etc/hosts` file.<br>
Set to `true` to update `/etc/hosts`, 'false' to skip.

#### sap_swpm_set_sidadm_noexpire
- _Type:_ `bool`
- _Default:_ `true`

The variable that controls whether the role will set the `sidadm` and `sapadm` user's passwords to never expire.<br>
Set to `false` to skip setting password to never expire.

#### sap_swpm_set_file_permissions
- _Type:_ `bool`
- _Default:_ `true`

The variable that controls whether the role will set file permissions and ownership for the SAP files in respective paths.<br>
Set to `false` to skip setting file permissions and ownership.<br>
See 'File Permissions and Ownership Variables' section for more information and configuration.<br>

#### sap_swpm_configure_firewall
- _Type:_ `bool`
- _Default:_ `false`

Set this variable to `true` to configure the required firewall ports for SAP Netweaver instances.<br>
What this configuration includes:<br>

- Installation of the `firewalld` package and starting the service.
- If `sap_swpm_firewall_ports` is undefined: A Firewalld service definition is created with recommended ports.<br>
  Note: `NN` refers to the SAP Instance Number defined in respective variables.<br>

Application instances: PAS, AAS, WD

| Ports | Protocol | Reason |
| --- | --- | --- |
| 1128-1129 | TCP | SAP Host Agent ports for status and metrics communication. |
| 32NN | TCP | SAP Dispatcher (32NN) communication |
| 33NN | TCP | SAP Gateway (33NN) communication |
| 47NN | TCP | SAP Dispatcher (47NN) SNC secured for CPIC and RFC communication. |
| 48NN | TCP | SAP Gateway (48NN) SNC secured for CPIC and RFC communication. |
| 80NN | TCP | SAP Internet Communication Manager (ICM) HTTP port (80NN). Used for non-secure web client access. |
| 443NN | TCP | SAP Internet Communication Manager (ICM) HTTPS port (443NN). Used for secure web client access. |
| 5NN13 | TCP | SAP Start Service (sapstartsrv) communication. Used for service control and status checks. |
| 5NN14 | TCP | SAP Start Service (sapstartsrv) communication. Used for service control and status checks. |
| 5NN16 | TCP | SAP Start Service (sapstartsrv) communication. Used for service control and status checks. |
| 620NN<br>621NN | TCP | JAVA ports (62NNN), commonly used for communication within the AS-Java stack, e.g., P4/P4S protocols. |

Central Services instances: ASCS, SCS, ERS

| Ports | Protocol | Reason |
| --- | --- | --- |
| 1128-1129 | TCP | SAP Host Agent ports for status and metrics communication. |
| 36NN | TCP | SAP Message Server port (36NN). Used for internal communication between application servers. |
| 39NN | TCP | SAP SAP Enqueue Server port (39NN). |
| 81NN | TCP | SAP Message Server HTTP port (81NN), configured via the `ms/http_port_<n>` profile parameter. |
| 5NN13 | TCP | SAP Start Service (sapstartsrv) communication. Used for service control and status checks. |
| 5NN14 | TCP | SAP Start Service (sapstartsrv) communication. Used for service control and status checks. |
| 5NN16 | TCP | SAP Start Service (sapstartsrv) communication. Used for service control and status checks. |

> If `sap_swpm_firewall_ports` is defined: The specified ports are opened directly and no service definition is created.<br>

**Important:** This does not include configuration of database services or ports, as they are not directly installed with this role.
For example, firewall configuration for SAP HANA can be managed separately in the `sap_hana_install` role.<br>

Managing configured Firewall:

- Setting this variable to `false` does not remove any existing firewall configuration.<br>
- For ongoing firewall management, consider using the `community.sap_operations.sap_firewall` role or the `firewall` Linux System Role.<br>

#### sap_swpm_inifile_directory
- _Type:_ `string`
- _Default:_ `/software/sap_swpm/inifiles`

The path to directory where existing sapinst inifile `inifile.params` is stored.<br>
Empty or invalid path will be ignored and the role will generate new inifile.<br>
The existing inifile is the first source of SWPM specific variables, so this variable must be known before any other source is read.
It cannot be set in `sap_swpm_role_parameters_dict` or `sap_swpm_templates_install_dictionary`.
<!-- END Mandatory Role Specific Variables -->


<!-- BEGIN Mandatory SWPM Specific Variables -->
### Mandatory SWPM Specific Variables
> All SWPM specific variables can be defined directly using existing inifile, `sap_swpm_templates_install_dictionary`, extravars, vars, inventory or directly in the playbook

#### sap_swpm_product_catalog_id
- _Type:_ `string`

SAP Product Catalog ID describing type of SAP System to install.<br>
Value must be a valid SAP Product Catalog ID, compatible with used SWPM version.<br>
Example: `NW_ABAP_OneHost:S4HANA2020.CORE.HDB.ABAP` represents S/4HANA 2020 OneHost system.

#### sap_swpm_software_path
- _Type:_ `string`
- _Default:_ `/software/sapfiles`

The primary path to directory where role will look for all files.<br>
It has to contain all required files (e.g. `igs*sar`, `igshelper*sar`, `SAPEXEDB_*SAR`, `SAPEXE_*SAR`, `IMDB_CLIENT*SAR`, `SAPHOSTAGENT*SAR`, etc.)

#### sap_swpm_sapcar_path
- _Type:_ `string`

The path to directory with `SAPCAR*EXE` file.<br>
If left empty, the role will fall back to using `sap_swpm_software_path`.

#### sap_swpm_sapcar_file_name
- _Type:_ `string`

**(Optional)** The name of the `SAPCAR*EXE` file located in the `sap_swpm_sapcar_path` directory.<br>
The role will automatically determine the `SAPCAR*EXE` file name if not specified.

#### sap_swpm_path
- _Type:_ `string`

The path to directory with `SWPM*.SAR` file.<br>
If left empty, the role will fall back to using `sap_swpm_software_path`.

#### sap_swpm_file_name
- _Type:_ `string`

**(Optional)** The name of the `SWPM*.SAR` file located in the `sap_swpm_path` directory.<br>
The role will automatically determine the `SWPM*.SAR` file name if not specified.

#### sap_swpm_software_extract_directory
- _Type:_ `string`

**(Optional)** The path to directory with extracted `SWPM` files.<br>
If left empty or commented out, the role will use `./extracted` as a subdirectory of `sap_swpm_path`.

#### sap_swpm_sid
- _Type:_ `string`

The SAP System ID (SID) for the SAP system to be installed.<br>
Value must be a valid SAP System ID (SID) consisting of 3 alphanumeric characters.<br>
See `SAP Note 1979280` for more information about accepted and restricted values.

#### sap_swpm_install_saphostagent
- _Type:_ `bool`
- _Default:_ `true`

Set to 'false' to disable the installation of the SAP Host Agent.<br>
**NOTE**: It is not recommended to disable the installation of the SAP Host Agent.

#### sap_swpm_fqdn
- _Type:_ `string`

The fully qualified domain name (FQDN) of the SAP system host.

#### sap_swpm_set_fqdn
- _Type:_ `bool`
- _Default:_ `true`

 Set to `false` if SWPM should not set the FQDN automatically.

#### sap_swpm_inifile_sections_list
- _Type:_ `list` of type `string`
- _Default:_ `[]`


The list of inifile sections to be processed by the role.<br>
Each selected section has required variables that need to be defined.<br>
For more details on what sapinst inifile parameters section updated see jinja2 template `templates/inifile_params.j2`.<br>

Available values:<br>

```yaml
sap_swpm_inifile_sections_list:
  - swpm_installation_media
  - swpm_installation_media_swpm2_hana
  - swpm_installation_media_swpm1
  - swpm_installation_media_swpm1_exportfiles
  - swpm_installation_media_swpm1_ibmdb2
  - swpm_installation_media_swpm1_oracledb_121
  - swpm_installation_media_swpm1_oracledb_122
  - swpm_installation_media_swpm1_oracledb_19
  - swpm_installation_media_swpm1_sapase
  - swpm_installation_media_swpm1_sapmaxdb
  - maintenance_plan_stack_tms_config
  - maintenance_plan_stack_tms_transports
  - maintenance_plan_stack_spam_config
  - maintenance_plan_stack_sum_config
  - maintenance_plan_stack_sum_10_batch_mode
  - credentials
  - credentials_hana
  - credentials_anydb_ibmdb2
  - credentials_anydb_oracledb
  - credentials_anydb_sapase
  - credentials_anydb_sapmaxdb
  - credentials_nwas_ssfs
  - credentials_hdbuserstore
  - db_config_hana
  - db_config_anydb_all
  - db_config_anydb_ibmdb2
  - db_config_anydb_oracledb
  - db_config_anydb_oracledb_121
  - db_config_anydb_oracledb_122
  - db_config_anydb_oracledb_19
  - db_config_anydb_sapase
  - db_config_anydb_sapmaxdb
  - db_connection_nw_hana
  - db_connection_nw_anydb_ibmdb2
  - db_connection_nw_anydb_oracledb
  - db_connection_nw_anydb_sapase
  - db_restore_hana
  - nw_config_anydb
  - nw_config_other
  - nw_config_central_services_abap
  - nw_config_central_services_java
  - nw_config_primary_application_server_instance
  - nw_config_additional_application_server_instance
  - nw_config_ers
  - nw_config_ports
  - nw_config_java_ume
  - nw_config_java_feature_template_ids
  - nw_config_java_icm_credentials
  - nw_config_webdisp_generic
  - nw_config_webdisp_gateway
  - nw_config_host_agent
  - nw_config_post_load_abap_reports
  - nw_config_livecache
  - nw_config_sld
  - nw_config_abap_language_packages
  - sap_os_linux_user
```

#### sap_swpm_master_password
- _Type:_ `string`

The master password used for all users during SWPM installation, unless overridden by specific user passwords.

<!-- END Mandatory SWPM Specific Variables -->


<!-- BEGIN SWPM 1 and SWPM 2 Variables -->
### SWPM 1 and SWPM 2 Variables

#### sap_swpm_software_use_media
- _Type:_ `bool`
- _Default:_ `false`

Set to `true` if SWPM2 should use CD Media when section `swpm_installation_media_swpm2_hana` is used.

- `SWPM1` (for older SAP products) requires CD Media and this parameter is ignored.
- `SWPM2` (for modern SAP products such as S/4 B/4) primarily uses SAR files, but this parameter allows use of CD Media if set to `true`.

#### sap_swpm_cd_export_pt1_path
- _Type:_ `string`

The path to the directory with Export Part 1 CD Media.<br>
Used in sections: `swpm_installation_media_swpm1_exportfiles`.

#### sap_swpm_cd_export_pt2_path
- _Type:_ `string`

The path to the directory with Export Part 2 CD Media.<br>
Used in sections: `swpm_installation_media_swpm1_exportfiles`.

#### sap_swpm_cd_language_path
- _Type:_ `string`

The path to the directory with Language Export CD Media.<br>
Used in sections: `swpm_installation_media_swpm1`.

#### sap_swpm_cd_java_path
- _Type:_ `string`

The path to the directory with JAVA Export CD Media.<br>
Used in sections: `swpm_installation_media_swpm1`.

#### sap_swpm_cd_export_path
- _Type:_ `string`

The path to the directory with Export CD Media.<br>
Used in sections: `swpm_installation_media`, `swpm_installation_media_swpm1_exportfiles`.

#### sap_swpm_export_files_path
- _Type:_ `string`

The path to the directory with AnyDB Export CD Media.<br>
Used in sections: `syscopy_export_anydb`.

#### sap_swpm_export_target_db_type
- _Type:_ `string`

The type of AnyDB Export CD Media.<br>
Used in sections: `syscopy_export_anydb`.


#### sap_swpm_cd_rdbms_path
- _Type:_ `string`

The path to the directory with RDBMS CD Media.<br>
Used in sections: `swpm_installation_media_swpm1`.

#### sap_swpm_cd_ibmdb2_path
- _Type:_ `string`

The path to the directory with IBM DB2 CD Media.<br>
Used in sections: `swpm_installation_media_swpm1_ibmdb2`.

#### sap_swpm_cd_ibmdb2_client_path
- _Type:_ `string`

The path to the directory with IBM DB2 Client CD Media.<br>
Used in sections: `swpm_installation_media_swpm1_ibmdb2`.

#### sap_swpm_ibmdb2_unpack_path
- _Type:_ `string`

The path where IBM DB2 CD Media is unpacked.<br>
Empty value defaults to `/db2/db2{{ sap_swpm_db_sid | lower }}/db2_software`.

#### sap_swpm_cd_sapase_path
- _Type:_ `string`

The path to the directory with SAP ASE CD Media.<br>
Used in sections: `swpm_installation_media_swpm1_sapase`.

#### sap_swpm_cd_sapase_client_path
- _Type:_ `string`

The path to the directory with SAP ASE Client CD Media.<br>
Used in sections: `swpm_installation_media_swpm1_sapase`.

#### sap_swpm_cd_sapmaxdb_path
- _Type:_ `string`

The path to the directory with MaxDB CD Media.<br>
Used in sections: `swpm_installation_media_swpm1_sapmaxdb`.

#### sap_swpm_cd_oracle_path
- _Type:_ `string`

The path to the directory with Oracle DB CD Media.<br>
Used in sections: `swpm_installation_media_swpm1_oracledb_121`, `swpm_installation_media_swpm1_oracledb_122`, `swpm_installation_media_swpm1_oracledb_19`.

#### sap_swpm_cd_oracle_client_path
- _Type:_ `string`

The path to the directory with Oracle DB Client CD Media.<br>
Used in sections: `swpm_installation_media_swpm1_oracledb_121`, `swpm_installation_media_swpm1_oracledb_122`, `swpm_installation_media_swpm1_oracledb_19`.
<!-- END SWPM 1 and SWPM 2 Variables -->


<!-- BEGIN NetWeaver Variables -->
### NetWeaver Variables

#### sap_swpm_ascs_instance_nr
- _Type:_ `string`

The instance number of SAP Netweaver ABAP Central Services (ASCS).<br>
Used in sections: `nw_config_central_services_abap`, `nw_config_ports`.

#### sap_swpm_ers_instance_nr
- _Type:_ `string`

The instance number of SAP Netweaver Enqueue Replication Server (ERS).<br>
Used in sections: `nw_config_ers`.

#### sap_swpm_pas_instance_nr
- _Type:_ `string`

The instance number of SAP Netweaver Primary Application Server (PAS).<br>
Used in sections: `nw_config_primary_application_server_instance`.

#### sap_swpm_aas_instance_nr
- _Type:_ `string`

The instance number of SAP Netweaver Additional Application Server (AAS).<br>
Used in sections: `nw_config_additional_application_server_instance`.

#### sap_swpm_java_scs_instance_nr
- _Type:_ `string`

The instance number of SAP Netweaver JAVA Central Services (SCS).<br>
Used in sections: `nw_config_central_services_java`.


#### sap_swpm_ascs_instance_hostname
- _Type:_ `string`

The hostname of SAP Netweaver ABAP Central Services (ASCS).<br>
Used in sections: `nw_config_central_services_abap`.

#### sap_swpm_ers_instance_hostname
- _Type:_ `string`

The hostname of SAP Netweaver Enqueue Replication Server (ERS).<br>
Used in sections: `nw_config_ers`.

#### sap_swpm_pas_instance_hostname
- _Type:_ `string`

The hostname of SAP Netweaver Primary Application Server (PAS).<br>
Used in sections: `nw_config_primary_application_server_instance`, `nw_config_java_ume`.

#### sap_swpm_aas_instance_hostname
- _Type:_ `string`

The hostname of SAP Netweaver Additional Application Server (AAS).<br>
Used in sections: `nw_config_additional_application_server_instance`.

#### sap_swpm_java_scs_instance_hostname
- _Type:_ `string`

The hostname of SAP Netweaver JAVA Central Services (SCS).<br>
Used in sections: `nw_config_central_services_java`.

#### sap_swpm_ddic_000_password
- _Type:_ `string`

The password of existing `DDIC` user in client `000` for restoration from backup.
Used in sections: `credentials_syscopy`.

#### sap_swpm_virtual_hostname
- _Type:_ `string`

Resolvable virtual hostname used for installation in a High Availability (HA) setup.<br>
Hostname must be either resolvable by DNS or `/etc/hosts` and resolved IP has to be part of IPv4 addresses on managed host.<br>
Used in sapinst command argument `SAPINST_USE_HOSTNAME`, generally in ASCS/ERS cluster configurations.
<!-- END NetWeaver Variables -->


<!-- BEGIN NetWeaver JAVA Variables -->
### NetWeaver JAVA Variables

#### sap_swpm_java_import_method
- _Type:_ `string`

The name of JAVA import method, either 'jload' or 'extramile' (BatchDeployer).<br>
Default value is based on `sap_swpm_product_catalog_id` prefix:

 - `jload` for SAP S/4HANA, which has `S4H` in the Product ID.
 - `extramile` for SAP NWAS JAVA otherwise.

#### sap_swpm_java_template_id_selected_list
- _Type:_ `list` of type `string`

The list of selected JAVA template keys for installation from the predefined dictionary `sap_swpm_java_template_id_lookup_dictionary` defined in role defaults.<br>
Used sections: `nw_config_java_feature_template_ids`.
<!-- END NetWeaver JAVA Variables -->


<!-- BEGIN NetWeaver JAVA UME Variables -->
### NetWeaver JAVA UME Variables

#### sap_swpm_ume_client_nr
- _Type:_ `string`
- _Default:_ `000`

The SAP client number for JAVA UME used in section `nw_config_java_ume`.

#### sap_swpm_ume_type
- _Type:_ `string`

The type of JAVA UME used in section `nw_config_java_ume`.

#### sap_swpm_ume_instance_nr
- _Type:_ `string`

The instance number of JAVA UME used in section `nw_config_java_ume`.<br>
Defaults to `sap_swpm_pas_instance_nr` if no value is provided.

#### sap_swpm_ume_j2ee_admin_password
- _Type:_ `string`

The `admin` password for JAVA UME used in sections `nw_config_java_ume` and `nw_config_java_icm_credentials`.

#### sap_swpm_ume_sapjsf_password
- _Type:_ `string`

The `sapjsf` password for JAVA UME used in section `nw_config_java_ume`.
<!-- END NetWeaver JAVA UME Variables -->


<!-- BEGIN Database Variables -->
### Database Variables

#### sap_swpm_db_sid
- _Type:_ `string`

The SAP System ID (SID) of Database, used across all database types in SWPM 1 and SWPM 2.<br>
Value must be a valid SAP System ID (SID) consisting of 3 alphanumeric characters.<br>
See SAP Note `1979280` for more information about non-HANA databases.<br>
See `SAP HANA Cockpit Installation Guide` for more information about HANA databases.

#### sap_swpm_db_instance_nr
- _Type:_ `string`

The Instance Number of Database instance.<br>
Value must be a valid instance number consisting of 2 digits.<br>
Used in SAP HANA specific inifile sections and for HDB userstore update.

#### sap_swpm_db_ip
- _Type:_ `string`

The IP address of the Database host used for updating `/etc/hosts` for SAP HANA database.

#### sap_swpm_db_host
- _Type:_ `string`

The hostname of the Database host used for updating `/etc/hosts` for SAP HANA database and various inifile sections.

#### sap_swpm_db_system_password
- _Type:_ `string`

The password of `SYSTEM` user for various Database types.

#### sap_swpm_db_systemdb_password
- _Type:_ `string`

The password of `SYSTEMDB` user in SAP HANA database.

#### sap_swpm_db_sidadm_password
- _Type:_ `string`

The password of `sidadm` user in SAP HANA database used in sections `db_connection_nw_hana`, `db_restore_hana`.

#### sap_swpm_db_schema_abap
- _Type:_ `string`

The name of ABAP schema during installation or restore.<br>
Defaults to `SAPHANADB` used by SAP HANA database, but used also for Oracle DB (`SAPSR3`) and IBM Db2 (`ABAP` or `SAPABAP1`).

#### sap_swpm_db_schema_abap_password
- _Type:_ `string`

The password of ABAP schema during installation or restore.<br>
Used by sections: `db_connection_nw_hana`, `db_connection_nw_anydb_oracledb`.

#### sap_swpm_db_schema_java
- _Type:_ `string`

The name of JAVA schema during installation or restore.<br>
Used by sections: `db_connection_nw_hana`, `db_config_anydb_oracledb`.

#### sap_swpm_db_schema_java_password
- _Type:_ `string`

The password of JAVA schema during installation or restore.<br>
Used by sections: `db_connection_nw_hana`, `db_connection_nw_anydb_oracledb`.

#### sap_swpm_db_schema
- _Type:_ `string`

The schema name for SAP HANA database.<br>
Used by sections: `db_config_hana`

#### sap_swpm_db_schema_password
- _Type:_ `string`

The schema password for SAP HANA database and SAP MaxDB.<br>
Used by sections: `credentials_hana`, `credentials_anydb_sapmaxdb`
<!-- END Database Variables -->


<!-- BEGIN Database Backup and Restore Variables -->
### Database Backup and Restore Variables
All variables in this section are used by section `db_restore_hana`.

#### sap_swpm_backup_location
- _Type:_ `string`

The path to directory with SAP HANA database backup files.

#### sap_swpm_backup_prefix
- _Type:_ `string`

The prefix for the backup files.

#### sap_swpm_backup_system_password
- _Type:_ `string`

The password of SYSTEM user for the backup.
<!-- END Database Backup and Restore Variables -->


<!-- BEGIN Web Dispatcher Variables -->
### Web Dispatcher Variables

#### sap_swpm_wd_instance_nr
- _Type:_ `string`

The instance number of the SAP Web Dispatcher.<br>
Used by section `nw_config_webdisp_generic` and for Firewall configuration.

#### sap_swpm_wd_system_connectivity
- _Type:_ `bool`
- _Default:_ `false`

Set to `true` to set parameter `configureSystemConnectivity` to `true` in sapinst inifile.

#### sap_swpm_wd_activate_icf
- _Type:_ `bool`
- _Default:_ `false`

Set to `true` to set parameter `activateICF` to `true` in sapinst inifile.

#### sap_swpm_wd_backend_sid
- _Type:_ `string`

The backend SID set in parameter `backEndSID` sapinst inifile.

#### sap_swpm_wd_backend_ms_http_port
- _Type:_ `string`

The backend message server port set in parameter `msHTTPPort` sapinst inifile.

#### sap_swpm_wd_backend_ms_host
- _Type:_ `string`

The backend message server hostname set in parameter `msHost` sapinst inifile.

#### sap_swpm_wd_backend_rfc_host
- _Type:_ `string`

The backend server RFC hostname set in parameter `rfcHost` sapinst inifile.

#### sap_swpm_wd_backend_rfc_instance_nr
- _Type:_ `string`

The backend server RFC instnance number set in parameter `rfcInstance` sapinst inifile.

#### sap_swpm_wd_backend_rfc_client_nr
- _Type:_ `string`

The backend server RFC client number set in parameter `rfcClient` sapinst inifile.

#### sap_swpm_wd_backend_rfc_user
- _Type:_ `string`

The backend server RFC user name set in parameter `rfcUser` sapinst inifile.

#### sap_swpm_wd_backend_rfc_user_password
- _Type:_ `string`

The backend server RFC user password set in parameter `rfcPassword` sapinst inifile.

#### sap_swpm_wd_backend_scenario_size
- _Type:_ `string`

The scenario size set in parameter `scenarioSize` sapinst inifile.

#### sap_swpm_wd_virtual_host
- _Type:_ `string`

The virtual hostname set in parameter `wdVirtualHostname` sapinst inifile.
<!-- END Web Dispatcher Variables -->


<!-- BEGIN Operating System User Variables -->
### Operating System User Variables

#### sap_swpm_sapadm_password
- _Type:_ `string`

The password of `sapadm` operating system user used in sections `credentials` and `db_connection_nw_anydb_ibmdb2`.

#### sap_swpm_sap_sidadm_password
- _Type:_ `string`

The password of `sidadm` operating system user used across database credential sections.

#### sap_swpm_sapadm_uid
- _Type:_ `string`

The user IDs of `sapadm` operating system users defined as 3 or 4 digit string.

#### sap_swpm_sidadm_uid
- _Type:_ `string`

The user IDs of `sidadm` operating system users defined as 3 or 4 digit string.

#### sap_swpm_sapsys_gid
- _Type:_ `string`

The group IDs of `sapsys` operating system group defined as 3 or 4 digit string.<br>
Both `sidadm` and `sapadm` users should belong to this group, if they already exist.
<!-- END Operating System User Variables -->


<!-- BEGIN Firewall Configuration Variables -->
### Firewall Configuration Variables 

#### sap_swpm_firewall_ports
- _Type:_ `list` of type `string`

**(Optional)** The list of firewall ports.<br>
The specified ports are opened directly and no service definition is created.<br>

#### sap_swpm_firewall_zone
- _Type:_ `string`

**(Optional)** The name of firewall zone where service or ports will be configured.<br>
Default firewall zone, usually `public`, is used if this variable is undefined.
<!-- END Firewall Configuration Variables -->


<!-- BEGIN Maintenance Planner Variables -->
### Maintenance Planner Variables **(Experimental)**

#### sap_swpm_mp_stack_path
- _Type:_ `string`

The path to the MP stack directory used to set sapinst command argument `SAPINST_STACK_XML` together with `sap_swpm_mp_stack_file_name`.

#### sap_swpm_mp_stack_file_name
- _Type:_ `string`

The name of the MP stack file used to set sapinst command argument `SAPINST_STACK_XML` together with `sap_swpm_mp_stack_path`.
<!-- END Maintenance Planner Variables -->


<!-- BEGIN SUM Variables -->
### SUM Variables **(Experimental)**
See [Up-To-Date Installation](#up-to-date-installation-udi) for more information.

#### sap_swpm_sum_start
- _Type:_ `bool`
- _Default:_ `false`

Set to `true` if SWPM should start SUM after installation.<br>
The role will wait for SUM completion and move known steps forward automatically.

#### sap_swpm_sum_prepare
- _Type:_ `bool`
- _Default:_ `false`

Set to `true` if SWPM should prepare SUM.<br>
Used in sections: `maintenance_plan_stack_sum_config`.

#### sap_swpm_sum_batch_file
- _Type:_ `string`

The name of existing `BatchModeInputFile.xml` from previous NetWeaver JAVA installation (SWPM 1) created in `/std/param` subdirectory.<br>
Used in sections: `maintenance_plan_stack_sum_10_batch_mode`.

#### sap_swpm_spam_update
- _Type:_ `bool`
- _Default:_ `false`

Set to `true` if SWPM should handle SPAM update.<br>
Used in sections: `maintenance_plan_stack_spam_config`.

#### sap_swpm_spam_update_sar
- _Type:_ `string`

The path to the update archive.<br>
Used in sections: `maintenance_plan_stack_spam_config`.

#### sap_swpm_configure_tms
- _Type:_ `bool`
- _Default:_ `true`

Set to `false` if SWPM should not configure TMS.<br>
Used in sections: `maintenance_plan_stack_tms_config`.

#### sap_swpm_tmsadm_password
- _Type:_ `string`

The password for `tmsadm` user.<br>
Used in sections: `maintenance_plan_stack_tms_config`.

#### sap_swpm_tms_tr_files_path
- _Type:_ `string`

The path to the transport files for TMS configuration.<br>
Used in sections: `maintenance_plan_stack_tms_transports`.
<!-- END SUM Variables -->


<!-- BEGIN SWPM Observer Mode Variables -->
### SWPM Observer Mode Variables **(Experimental)**

#### sap_swpm_observer_mode
- _Type:_ `bool`
- _Default:_ `false`

Set to `true` to enable SWPM observer mode for debugging or troubleshooting.<br>
This allows user to watch the installation progress from a browser (on standard port 4237) interactively.<br>
> NOTE: This is not intended use and interaction can impact the automated installation, resulting in unexpected issues.

#### sap_swpm_remote_access_user
- _Type:_ `string`

The name of the remote access user for SWPM observer mode.<br>
Allows to specify a different remote access user (e.g. when root's password is unknown).<br>
Default SWPM behaviour is to use root, which might not be desirable for security reasons.<br>
The remote access user must exist on operating system level before SWPM is executed.
<!-- END SWPM Observer Mode Variables -->


<!-- BEGIN File Permissions and Ownership Variables -->
### File Permissions and Ownership Variables
The following 9 parameters define the default permission and ownership settings as per the documentation [Installation of SAP ABAP Systems on UNIX : SAP HANA 2.0 Database - Using Software Provisioning Manager 2.0 guide](https://help.sap.com/docs/SLTOOLSET/39c32e9783f6439e871410848f61544c/c1f95d30d0ba4335919bf6e6f44263b2.html?version=CURRENT_VERSION_SWPM20).<br>

> NOTE: The source mentions `755` as the minimum permission for the SPWM download directory and a umask setting of `022` for the user which downloads the SAP software.

#### sap_swpm_software_directory_mode
- _Type:_ `string`
- _Default:_ `0755`

The permission settings for the directories in the `sap_swpm_software_path`.

#### sap_swpm_software_directory_owner
- _Type:_ `string`
- _Default:_ `root`

The user ownership settings for the directories in the `sap_swpm_software_path`.

#### sap_swpm_software_directory_group
- _Type:_ `string`
- _Default:_ `root`

The group ownership settings for the directories in the `sap_swpm_software_path`.

#### sap_swpm_files_sapcar_mode
- _Type:_ `string`
- _Default:_ `0755`

The permission settings for the `SAPCAR` files in the directory `sap_swpm_sapcar_path`.

#### sap_swpm_files_sapcar_owner
- _Type:_ `string`
- _Default:_ `root`

The user ownership settings for the `SAPCAR` files in the directory `sap_swpm_sapcar_path`.

#### sap_swpm_files_sapcar_group
- _Type:_ `string`
- _Default:_ `root`

The group ownership settings for the `SAPCAR` files in the directory `sap_swpm_sapcar_path`.

#### sap_swpm_files_non_sapcar_mode
- _Type:_ `string`
- _Default:_ `0644`

The permission settings for the `SWPM*.SAR` files in the directory `sap_swpm_path` and `non-SAPCAR` files in the in the directory `sap_swpm_software_path`.

#### sap_swpm_files_non_sapcar_owner
- _Type:_ `string`
- _Default:_ `root`

The user ownership settings for the `SWPM*.SAR` files in the directory `sap_swpm_path` and `non-SAPCAR` files in the in the directory `sap_swpm_software_path`.

#### sap_swpm_files_non_sapcar_group
- _Type:_ `string`
- _Default:_ `root`

The group ownership settings for the `SWPM*.SAR` files in the directory `sap_swpm_path` and `non-SAPCAR` files in the in the directory `sap_swpm_software_path`.
<!-- END File Permissions and Ownership Variables -->


<!-- BEGIN Other Role Specific Variables -->
### Other Role Specific Variables

#### sap_swpm_generic
- _Type:_ `bool`
- _Default:_ `false`

Set to `true` if the role should process only `SWPM` and `SAPCAR` software files.<br>
Other files like `SAPEXE`, `SAPEXEDB`, `igsexe`, `igshelper` will not be validated by the role before SWPM execution.

#### sap_swpm_display_unattended_output
- _Type:_ `bool`
- _Default:_ `false`

Set to `true` to show output from SWPM execution (sapinst stdout) in debug task.

#### sap_swpm_force **USE WITH CAUTION**
- _Type:_ `bool`
- _Default:_ `false`

Override that forces execution of installation tasks if existing SAP instance is detected.<br>
> **WARNING**: This variable should be used with caution as running SWPM installation with active SAP instances can lead to corruption of existing SAP installation!

#### sap_swpm_skip_detection
- _Type:_ `bool`

**(Optional)** Skip all detection checks. Use ONLY for testing/development on clean systems!<br>

> **WARNING**: Skipping detection can lead to data loss if installation already exists!
> This will bypass all safety checks including saphostctrl, sapcontrol, and file existence checks

#### sap_swpm_db_load_force **USE WITH CAUTION**
- _Type:_ `bool`
- _Default:_ `false`

Explicit acknowledgement required for Database Load products (`NW_ABAP_DB`, `NW_Java_DB`, etc.).<br>
These products cannot be detected by this role on empty managed hosts, because no local instance files are created.<br>
Set to `true` only after confirming the target database is empty or intended to be overwritten.<br>
The variable `sap_swpm_force` does NOT cover this scenario and it only applies to detection of existing instances.

> **WARNING**: Running SWPM against an existing database WILL DROP and recreate the schema user, causing DATA LOSS on existing systems!
<!-- END Other Role Specific Variables -->


<!-- BEGIN Other SWPM Specific Variables -->
### Other SWPM Specific Variables

#### sap_swpm_env_vars
- _Type:_ `dict`

**(Optional)** The dictionary of environment variables to be temporarily injected when executing sapinst.<br>
This can be used to modify variables like `TMP` or `rsdb_ssfs_connect` which will be used by sapinst.<br>
See SAP Notes `3651688` and `2063079` for more information on TMP environment variable when executing SWPM..

Example:

```yaml
sap_swpm_env_vars:
  TMP: /var/tmp
```

#### sap_swpm_command_extra_args
- _Type:_ `string`

**(Optional)** The string of extra sapinst arguments to be added to the sapinst command line.

#### sap_swpm_templates_install_dictionary
- _Type:_ `dict`

**(Optional)**  The dictionary containing installation templates for the role.<br>
Primarily used to define different SAP product versions and their specific role variables.<br>
See repository level `playbooks` directory for more examples.

#### sap_swpm_templates_product_input
- _Type:_ `string`

The key name of the product entry in the dictionary `sap_swpm_templates_install_dictionary`.<br>
Required if `sap_swpm_templates_install_dictionary` is defined. It must be a non-empty string that exists as a key in the dictionary.

#### sap_swpm_role_parameters_dict
- _Type:_ `dict`

**(Optional)** The dictionary of SWPM Specific variables and their values, defined as a top level variable.<br>
It has higher precedence than role variables and their defaults, including Booleans, so it can be used to override them for specific scenarios.<br>
See [SWPM Variable Precedence](#swpm-variable-precedence) for more information.

- Only keys starting with `sap_swpm_` are used and empty values are ignored.
- Deprecated variable names are not mapped to their new names, use the new names.
- Role Specific variables have no effect when defined in this dictionary.

Example:

```yaml
sap_swpm_role_parameters_dict:
  sap_swpm_install_saphostagent: false
```

#### sap_swpm_inifile_parameters_dict
- _Type:_ `dict`

**(Optional)** The dictionary of inifile parameters to be updated after inifile is generated.<br>
Example:

```yaml
sap_swpm_inifile_parameters_dict:
  archives.downloadBasket: /software/download_basket
  NW_getFQDN.FQDN: poc.cloud
```

#### sap_swpm_parallel_jobs_nr
- _Type:_ `string`
- _Default:_ `23`

The number of parallel extraction jobs for SAP HANA database.

#### sap_swpm_diagnostics_agent_password
- _Type:_ `string`

**(Optional)** The password for the diagnostics agent.

#### sap_swpm_use_password_file
- _Type:_ `bool`
- _Default:_ `false`

Set to `true` if SWPM should use a password file for existing inifile template containing encrypted passwords

#### sap_swpm_password_file_path
- _Type:_ `string`

The path where file `instkey.pkey` is expected when `sap_swpm_use_password_file` is set to `true`.

#### sap_swpm_load_type
- _Type:_ `string`
- _Default:_ `SAP`

The type of load for the SWPM installation set in inifile parameter `loadType`.<br>
Used in sections: `nw_config_other`, `syscopy_export_anydb`, `syscopy_import_anydb_ibmdb2`

#### sap_swpm_ascs_install_gateway
- _Type:_ `bool`
- _Default:_ `true`

Set to `false` if Gateway should not be installed as part of ASCS.<br>
Used in sections: `nw_config_webdisp_gateway`.<br>
> **NOTE**: It is not recommend to disable installation of gateway during ASCS installation.

<!-- END Other SWPM Specific Variables -->
<!-- END Role Variables -->
