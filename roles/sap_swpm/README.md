# sap_swpm Ansible Role

Ansible role for SAP software installation using SWPM

This role has been tested and working for the following scenarios
-   One Host Installation
-   Dual Host Installation
-   Distributed Installation
-   System Restore
-   High Avalability Installation

This role has been tested and working for the following SAP products
-   SAP S/4HANA 1809, 1909, 2020, 2021
-   SAP B/4HANA
-   SAP Solution Manager 7.2
-   SAP Netweaver Business Suite Applications (ECC, GRC, etc)
-   SAP Web Dispatcher

> The general rule is - if it runs in SWPM, this will work.

### SAP Preconfigure

- Make sure required volumes and filesystems are configured in the host. You can use the role `sap_storage` to configure this. More info [here](/roles/sap_storage)

- Please run the RHEL SAP System Role `sap_general_preconfigure` for initial host configuration

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

Please check the default parameters file for more information on other parameters that can be used as an input
- [**sap_swpm** default parameters](defaults/main.yml)

- Template S/4HANA2020 input for installation
    - [Template S/4HANA Install](/playbooks/vars/s4hana/template.S4H.install)
    - [Template S/4HANA Restore](/playbooks/vars/s4hana/template.S4H.restore)

- Sample S/4HANA2020 input for distributed / high availability installation (ASCS, ERS, DBCI, PAS)
    - [Sample S/4HANA distributed](/playbooks/vars/s4hana/s4hana-distributed)

- Sample Solman 7.2 input installation
    - ABAP [Solman 7.2](/playbooks/vars/solman/SHA.install)
    - Java [Solman 7.2](/playbooks/vars/solman/SHA.install)

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

Example using all inifile list parameters with the Default Templates mode:

```
sap_swpm_ansible_role_mode: default_templates
sap_swpm_templates_product_input: default_templates

sap_swpm_templates_install_dictionary:

  template_name:

    sap_swpm_product_catalog_id: NW_ABAP_OneHost:BS2016.ERP608.DB6.PD
    sap_swpm_inifile_dictionary:
      sap_swpm_sid:
      ...
    sap_swpm_inifile_list:
    - swpm_installation_media
    - swpm_installation_media_swpm2_hana
    - swpm_installation_media_swpm1
    - swpm_installation_media_swpm1_ibmdb2
    - sum_config
    - credentials
    - credentials_hana
    - credentials_anydb_ibmdb2
    - credentials_anydb_oracledb
    - credentials_anydb_sapase
    - credentials_anydb_sapmaxdb
    - db_config_hana
    - db_config_anydb_all
    - db_config_anydb_ibmdb2
    - db_config_anydb_oracledb
    - db_config_anydb_sapase
    - db_config_anydb_sapmaxdb
    - db_connection_nw_hana
    - db_connection_nw_anydb_ibmdb2
    - db_connection_nw_anydb_oracledb
    - db_restore_hana
    - nw_config_anydb
    - nw_config_other
    - nw_config_central_instance
    - nw_config_ers
    - nw_config_webdisp_gateway
    - nw_config_instance
    - nw_config_ports
    - nw_config_java_ume
    - nw_config_webdisp_generic
    - nw_config_host_agent
    - sap_os_nix_user
```

## License

Apache license 2.0

## Author Information

IBM Lab for SAP Solutions, Red Hat for SAP Community of Practice, Jason Masipiquena, Sean Freeman
