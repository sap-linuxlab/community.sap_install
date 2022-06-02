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

## Flow

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

## License

Apache license 2.0

## Author Information

IBM Lab for SAP Solutions, Red Hat for SAP Community of Practice, Jason Masipiquena, Sean Freeman
