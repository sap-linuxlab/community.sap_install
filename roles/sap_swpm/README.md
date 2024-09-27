<!-- BEGIN Title -->
# sap_swpm Ansible Role
<!-- END Title -->
![Ansible Lint for sap_swpm](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_swpm.yml/badge.svg)

## Description
<!-- BEGIN Description -->
The Ansible role `sap_swpm` installs the SAP ABAP Application Platform (formerly known as SAP NetWeaver) using the SAP Software Provisioning Manager (SWPM).
<!-- END Description -->

<!-- BEGIN Dependencies -->
## Dependencies
- `fedora.linux_system_roles`
    - Roles:
        - `selinux`

Install required collections by `ansible-galaxy install -vv -r meta/collection-requirements.yml`.
<!-- END Dependencies -->

## Prerequisites
<!-- BEGIN Prerequisites -->
Managed nodes:
- Directory with SAP Installation media is present and `sap_install_media_detect_source_directory` updated. Download can be completed using [community.sap_launchpad](https://github.com/sap-linuxlab/community).
- Ensure that servers are configured for SAP ABAP Application Platform. See [Recommended](#recommended) section.
- Ensure that volumes and filesystems are configured correctly. See [Recommended](#recommended) section.

### Prepare SAP ABAP Application Platform installation media
Place a valid SAPCAR executable file in a directory specified by variable `sap_swpm_sapcar_path`, e.g. /software/sapcar. Example:
    - SAPCAR_1300-70007716.EXE

Place the following files in a directory specified by variable `sap_swpm_swpm_path`, e.g. /software/sap_swpm:
    - SWPM20SP18_3-80003424.SAR

Place the following files in a directory specified by variable `sap_swpm_software_path`, e.g. /software/abap_application_platform:
    - For a new installation
        - Download the appropriate software from SAP Software Download Center, Maintenance Planner, etc
    - For a restore or new installation
        - SAP IGS                   - `igs*.sar`
        - SAP IGS HELPER            - `igshelper*sar`
        - SAP Host Agent            - `SAPHOSTAGENT*SAR`
        - SAP Kernel DB             - `SAPEXEDB_*SAR`
        - SAP Kernel DB Independent - `SAPEXE_*SAR`
        - SAP HANA Client           - `IMDB_CLIENT*SAR`

Alternatively, you can place all the files mentioned above into a single directory and use the role [sap_install_media_detect](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_install_media_detect) to identify the required files and set the role variables automatically so that the role `sap_swpm` has access to all the files needed for a successful installation of SAP ABAP Application Platform.

<!-- END Prerequisites -->

## Execution
<!-- BEGIN Execution -->
<!-- END Execution -->

<!-- BEGIN Execution Recommended -->
### Recommended
It is recommended to execute this role together with other roles in this collection, in the following order:</br>
1. [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure)
2. [sap_netweaver_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_preconfigure)
3. [sap_install_media_detect](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_install_media_detect)
4. *`sap_swpm`*

Note: For most scenarios, a database like SAP HANA must be available. Use the role [sap_hana_install](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_install) for installing the SAP HANA database.
<!-- END Execution Recommended -->

### Execution Flow
<!-- BEGIN Execution Flow -->

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

    Method 1: Predefined sections of the file `inifile_params.j2` will be used to create the file `inifile.params`. The variable `sap_swpm_inifile_sections_list` contains a list of sections which will part of the file `inifile.params`. All other sections will be ignored. The inifile parameters themselves will be set according to other role parameters. Example: The inifile parameter `archives.downloadBasket` will be set to the content of the role parameter `sap_swpm_software_path`.

    Method 2: The file `inifile.params` will be configured from the content of the dictionary `sap_swpm_inifile_parameters_dict`. This dictionary is defined like in the following example:

```
sap_swpm_inifile_parameters_dict:
  archives.downloadBasket: /software/download_basket
  NW_getFQDN.FQDN: example.com
```

It is also possible to use method 1 for creating the inifile and then replace or set additional variables using method 2: Define both of the related parameters, `sap_swpm_inifile_sections_list` and `sap_swpm_inifile_parameters_dict`.

- The file `inifile.params` is then transferred to a temporary directory on the managed node, to be used by the sapinst process.

### SAP SWPM

- Execute SWPM. This and the remaining steps can be skipped by setting the default of the parameter `sap_swpm_run_sapinst` to `false`.

### Post-Install

- Set expiry of Unix created users to 'never'

- Apply firewall rules for SAP NW (optional - false by default)
<!-- END Execution Flow -->

### Example
<!-- BEGIN Execution Example -->

#### Playbook for installing a Primary Application Server (PAS) instance

```yaml
---
- name: Ansible Play for SAP NetWeaver Application Server - Primary Application Server (PAS)
  hosts: nwas_pas
  become: true
  any_errors_fatal: true # https://docs.ansible.com/ansible/latest/user_guide/playbooks_error_handling.html#aborting-a-play-on-all-hosts
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
        sap_install_media_detect_db_client: "saphana"

    # Install SAP NetWeaver PAS via Ansible Role sap_swpm
    - name: Execute Ansible Role sap_swpm
      ansible.builtin.include_role:
        name: community.sap_install.sap_swpm
      vars:
        *** TODO: Fill in variables ***
```
<!-- END Execution Example -->

<!-- BEGIN Role Tags -->
### Role Tags
With the following tags, the role can be called to perform certain activities only:
- tag `sap_swpm_generate_inifile`: Only create the sapinst inifile, without running most of the preinstall steps.
  This can be useful for checking if the inifile is created as desired.
- tag `sap_swpm_sapinst_commandline`: Only show the sapinst command line.
- tag `sap_swpm_pre_install`: Perform all preinstallation steps, then exit.
- tag `sap_swpm_setup_firewall`: Only perform the firewall preinstallation settings (but only if variable `sap_swpm_setup_firewall` is set to `true`).
- tag `sap_swpm_update_etchosts`: Only update file `/etc/hosts` (but only if variable `sap_swpm_update_etchosts` is set to `true`).
!-- END Role Tags -->

## License
<!-- BEGIN License -->
Apache 2.0
<!-- END License -->

## Maintainers
<!-- BEGIN Maintainers -->
- [Bernd Finger](https://github.com/berndfinger)
- [Sean Freeman](https://github.com/seanfreeman)
<!-- END Maintainers -->
