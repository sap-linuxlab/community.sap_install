# sap_swpm Ansible Role

Ansible role for SAP software installation using SWPM

## Requirements

The role requires additional collections which are specified in `meta/collection-requirements.yml`. Before using this role,
make sure that the required collections are installed, for example by using the following command:

`ansible-galaxy install -vv -r meta/collection-requirements.yml`

## Scope

This role has been tested and working for the following scenarios
-   One Host Installation
-   Dual Host Installation
-   Distributed Installation
-   System Restore
-   High Avalability Installation

This role has been tested and working for the following SAP products
-   SAP S/4HANA 1809, 1909, 2020, 2021
-   SAP BW/4HANA
-   SAP Solution Manager 7.2
-   SAP Netweaver Business Suite Applications (ECC, GRC, etc)
-   SAP Web Dispatcher

> The general rule is - if the installation uses SAP SWPM then this Ansible Role can be used.

### SAP Preconfigure

- Ensure the required volumes and filesystems are configured in the host. You can use the role `sap_storage_setup` to configure this. More info [here](/roles/sap_storage_setup)

- Please run the RHEL SAP System Role `sap_general_preconfigure` for initial host configuration; as necessary, also use `sap_netweaver_preconfigure` and `sap_hana_preconfigure`

- For further guidance on using SAP SWPM for different SAP Software installations, please see System Provisioning with Software Provisioning Manager (SWPM) - [User Guides for SAP SWPM 1.0](30839dda13b2485889466316ce5b39e9/c8ed609927fa4e45988200b153ac63d1.html?locale=en-US) and [User Guides for SAP SWPM 2.0](https://help.sap.com/docs/SOFTWARE_PROVISIONING_MANAGER/30839dda13b2485889466316ce5b39e9/6865029dacbe473fadd8eff339bfa568.html?locale=en-US)

### SAP Software Installation .SAR Files

1. SAPCAR executable

2. Software Provisioning Manager .SAR file
    - `SWPM*.SAR`

3. SAP Installation files
    - For New Installation
        - Download appropriate software from SAP Software Download Center, Maintenance Planner, etc
    - For Restore or New Installation
        - SAP IGS                   - `igs*.sar`
        - SAP IGS HELPER            - `igshelper*sar`
        - SAP Host Agent            - `SAPHOSTAGENT*SAR`
        - SAP Kernel DB             - `SAPEXEDB_*SAR`
        - SAP Kernel DB Independent - `SAPEXE_*SAR`
        - SAP HANA Client           - `IMDB_CLIENT*SAR`

4. SAP HANA Database MDC DB Tenant Backup (for restore)
    - stored on the local disk of the machine where the SAP HANA database server will reside

    NOTE: Specific media requirements will use format `SAPINST.CD.PACKAGE.<media_name> = <location>`, and the media names can be discovered by using this command on the SWPM directory `grep -rwh "<package mediaName" --include "packages.xml" /software/sap_swpm_extracted/ | sed 's/^ *//g' | sort | uniq`

## Variables and Parameters

### Input Parameters

The inputs are critical for running this role
    - Determines the installation type
    - Incomplete parameters will result to failure
    - Wrong parameters will result to failure

Create an input file which contains all relevant installation information.
Sample input files are stored in the [inputs](/playbooks/vars) folder of this Ansible collection. Use the samples as guide for your desired installation

### Default Parameters

### Default Parameters

Please check the default parameters file for more information on other parameters that can be used as an input:
- [**sap_swpm** default parameters](defaults/main.yml)

Sample Playbooks and sample parameters are shown in the Ansible Collection `/playbooks` directory.

The Ansible Collection `/playbooks` directory includes sample playbooks for using the `sap_swpm` Ansible Role in the following 'modes':
- Default
- Default Templates
- Advanced
- Advanced Templates
- Inifile Reuse

The Ansible Collection `/playbooks/vars` directory includes sample variable files for:
- `sap_swpm` 'Default mode' to generate inifile.params of...
  - SAP BW/4HANA OneHost
  - SAP S/4HANA Distributed - ASCS, DBCI, ERS, PAS
  - SAP S/4HANA OneHost
  - SAP S/4HANA System Copy OneHost
  - SAP Solution Manager (ABAP)
  - SAP Solution Manager (JAVA)
  - SAP Web Dispatcher
  - SAP System Rename
- `sap_swpm` 'Default Templates mode' to generate inifile.params of...
  - SAP S/4HANA OneHost
  - SAP S/4HANA System Copy OneHost
  - SAP System Rename
- `sap_swpm` 'Advanced mode' to generate inifile.params of...
  - SAP S/4HANA OneHost
- `sap_swpm` 'Advanced Templates mode' to generate inifile.params of...
  - SAP BW/4HANA OneHost
  - SAP S/4HANA Distributed - ASCS, DBCI, ERS, PAS
  - SAP S/4HANA OneHost
  - SAP S/4HANA System Copy OneHost
  - SAP Solution Manager (ABAP)
  - SAP Solution Manager (JAVA)
  - SAP Web Dispatcher
  - SAP System Rename
- `sap_swpm` 'Inifile Reuse mode' inifile.params file for...
  - SAP S/4HANA OneHost

NOTE: these are only sample files, they are meant to be edited by the user before execution and do not cover all scenarios possible (the Ansible Role can execute ant SAP SWPM installation)

## Execution

Sample Ansible Playbook Execution

- Local Host Installation
    - `ansible-playbook --connection=local --limit localhost -i "localhost," sap-swpm.yml -e "@inputs/S4H.install"`

- Target Host Installation
    - `ansible-playbook -i "<target-host>" sap-swpm.yml -e "@inputs/S4H.install"`

### Sample Playbook

```yaml
---
- hosts: all
  become: true
  roles:
    - { role: sap_swpm }
```

## Execution Flow

### Pre-Install

- Determine installation type
    - The product id specified determines the installation type
        - standard installation
        - system restore
        - generic product installation
        - high availability installation

- Get SAPCAR executable filename from `sap_swpm_sapcar_path`

- Get SWPM executable filename from `sap_swpm_swpm_path`

- Get all .SAR filenames  from `sap_swpm_software_path`

- Update `/etc/hosts` (optional - yes by default)

- Apply firewall rules for SAP HANA (optional - no by default)

- Process SAP SWPM `inifile.params` based on inputs

### SAP SWPM

- Execute SWPM

### Post-Install

- Set expiry of Unix created users to 'never'

- Apply firewall rules for SAP NW (optional - no by default)


## Execution Modes

Every SAP Software installation via SAP Software Provisioning Manager (SWPM) is possible, there are different Ansible Role execution modes available:

- Default (`sap_swpm_templates_product_input: default`), run software install tasks using easy Ansible Variable to generate SWPM Unattended installations
    - Default Templates (`sap_swpm_templates_product_input: default_templates`), optional use of templating definitions for repeated installations
- Advanced (`sap_swpm_templates_product_input: advanced`), run software install tasks with Ansible Variables one-to-one matched to SWPM Unattended Inifile parameters to generate bespoke SWPM Unattended installations
    - Advanced Templates (`sap_swpm_templates_product_input: advanced_templates`), optional use of templating definitions for repeated installations
- Inifile Reuse (`sap_swpm_templates_product_input: inifile_reuse`), run previously-defined installations with an existing SWPM Unattended inifile.params

### Default Templates mode variables

Example using all inifile list parameters with the Default Templates mode to install SAP ECC EhP8 on IBM Db2:

```
sap_swpm_ansible_role_mode: default_templates
sap_swpm_templates_product_input: default_templates

sap_swpm_templates_install_dictionary:

  template_name_ecc_ehp8_ibmdb2:

    sap_swpm_product_catalog_id: NW_ABAP_OneHost:BS2016.ERP608.DB6.PD
    sap_swpm_inifile_dictionary:
      sap_swpm_sid:
      ...
    sap_swpm_inifile_list:
    - swpm_installation_media
    - swpm_installation_media_swpm1
    - swpm_installation_media_swpm1_exportfiles
    - swpm_installation_media_swpm1_ibmdb2
    - sum_config
    - credentials
    - credentials_anydb_ibmdb2
    - db_config_anydb_all
    - db_config_anydb_ibmdb2
    - db_connection_nw_anydb_ibmdb2
    - nw_config_anydb
    - nw_config_other
    - nw_config_central_services_abap
    #  - nw_config_central_services_java
    - nw_config_primary_application_server_instance
    - nw_config_ports
    - nw_config_host_agent
    #  - nw_config_post_abap_reports
    - sap_os_linux_user
```

## Tags

With the following tags, the role can be called to perform certain activities only:
- tag `sap_swpm_generate_inifile`: Only create the sapinst inifile. This can be useful for checking if the inifile is created as desired.
- tag `sap_swpm_sapinst_commandline`: Only show the sapinst command line.
- tag `sap_swpm_pre_install`: Perform all preinstallation steps, then exit.
- tag `sap_swpm_setup_firewall`: Only perform the firewall preinstallation settings (but only if variable `sap_swpm_setup_firewall` is set to `true`).
- tag `sap_swpm_update_etchosts`: Only update file `/etc/hosts` (but only if variable `sap_swpm_update_etchosts` is set to `true`).

## License

Apache license 2.0

## Author Information

IBM Lab for SAP Solutions, Red Hat for SAP Community of Practice, Jason Masipiquena, Sean Freeman, Bernd Finger, Markus Koch
