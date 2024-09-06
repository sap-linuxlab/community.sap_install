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
-   High Availability Installation

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
    - Incomplete parameters will result in failure
    - Wrong parameters will result in failure

Create an input file which contains all relevant installation information.
Sample input files are stored in the [inputs](/playbooks/vars) folder of this Ansible collection. Use the samples as guide for your desired installation.

### Default Parameters

Please check the default parameters file for more information on other parameters that can be used as an input:
- [**sap_swpm** default parameters](defaults/main.yml)

### Migrating playbooks from previous versions of sap_swpm

The following role parameter is no longer used because there are no role `modes` any more:

#### sap_swpm_ansible_role_mode

The following two role parameters have been renamed. If the new variables are not defined, the old ones are converted to the new ones.

#### sap_swpm_inifile_list -> sap_swpm_inifile_sections_list

**Previous name**: sap_swpm_inifile_list\
**New name**: sap_swpm_inifile_sections_list\
**Reason**: This variable contains sections of the sapinst input file, `inifile.params`.
The new variable name is reflecting this purpose.

#### sap_swpm_inifile_custom_values_dictionary -> sap_swpm_inifile_parameters_dict

**Previous name**: sap_swpm_inifile_custom_values_dictionary\
**New name**: sap_swpm_inifile_parameters_dict\
**Reason**: This variable contains parameter names and values of the
sapinst input file, `inifile.params`. The new variable name is reflecting this purpose.

#### Migration from the `*_templates` modes of the previous version of `sap_swpm`

The role `sap_swpm` does no longer use the dictionary `sap_swpm_templates_install_dictionary`.
This dictionary was used in the previous role modes `default_templates` and `advanced_templates`.

Because of this change, required low level members of `sap_swpm_templates_install_dictionary` have to be
redefined to top level variables. Creating top level variables from low level members
of a dict can be done:

- in a separate task using `ansible.builtin.set_fact` before calling `sap_swpm`, or

- in the task calling `sap_swpm` with a `vars`: section of the task calling `sap_swpm`.

Example:

```
- name: Execute the role sap_swpm
  ansible.builtin.include_role:
    name: community.sap_install.sap_swpm
  vars:
    sap_swpm_templates_product_input: "sap_s4hana_2023_distributed_nwas_ascs_ha"

    sap_swpm_product_catalog_id: "{{ sap_swpm_templates_install_dictionary[sap_swpm_templates_product_input]['sap_swpm_product_catalog_id'] }}"
    sap_swpm_inifile_sections_list: "{{ sap_swpm_templates_install_dictionary[sap_swpm_templates_product_input]['sap_swpm_inifile_list'] }}"
```

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
    - sap_swpm
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

- Update `/etc/hosts` (optional - `false` by default)

- Apply firewall rules for SAP HANA (optional - `false` by default)

- At this stage, the role is searching for a sapinst inifile on the managed node, or it will create one:

  - If a file `inifile.params` is located on the managed node in the directory specified in `sap_swpm_inifile_directory`,
    the role will not create a new one but rather download this file to the control node.

  - If such a file does *not* exist, the role will create an SAP SWPM `inifile.params` file by one of the following methods:

    Method 1: Predefined sections of the file `inifile_params.j2` will be used to create the file `inifile.params`.
              The variable `sap_swpm_inifile_sections_list` contains a list of sections which will part of the file `inifile.params`.
              All other sections will be ignored. The inifile parameters themselves will be set according to other role parameters.
              Example: The inifile parameter `archives.downloadBasket` will be set to the content of the role parameter
              `sap_swpm_software_path`.

    Method 2: The file `inifile.params` will be configured from the content of the dictionary `sap_swpm_inifile_parameters_dict`.
              This dictionary is defined like in the following example:

```
sap_swpm_inifile_parameters_dict:
  archives.downloadBasket: /software/download_basket
  NW_getFQDN.FQDN: poc.cloud
```

   It is also possible to use method 1 for creating the inifile and then replace or set additional variables using method 2:
   Just define both of the related parameters, `sap_swpm_inifile_sections_list` and `sap_swpm_inifile_parameters_dict`.

- The file `inifile.params` is then transferred to a temporary directory on the managed node, to be used by the sapinst process.

### SAP SWPM

- Execute SWPM. This and the remaining steps can be skipped by setting the default of the parameter `sap_swpm_run_sapinst` to `false`.

### Post-Install

- Set expiry of Unix created users to 'never'

- Apply firewall rules for SAP NW (optional - false by default)

## Tags

With the following tags, the role can be called to perform certain activities only:
- tag `sap_swpm_generate_inifile`: Only create the sapinst inifile, without running most of the preinstall steps.
  This can be useful for checking if the inifile is created as desired.
- tag `sap_swpm_sapinst_commandline`: Only show the sapinst command line.
- tag `sap_swpm_pre_install`: Perform all preinstallation steps, then exit.
- tag `sap_swpm_setup_firewall`: Only perform the firewall preinstallation settings (but only if variable `sap_swpm_setup_firewall` is set to `true`).
- tag `sap_swpm_update_etchosts`: Only update file `/etc/hosts` (but only if variable `sap_swpm_update_etchosts` is set to `true`).

## License

Apache license 2.0

## Author Information

IBM Lab for SAP Solutions, Red Hat for SAP Community of Practice, Jason Masipiquena, Sean Freeman, Bernd Finger, Markus Koch
