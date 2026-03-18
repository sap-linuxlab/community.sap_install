<!-- BEGIN Title -->
# sap_install_media_detect Ansible Role
<!-- END Title -->
![Ansible Lint for sap_install_media_detect](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_install_media_detect.yml/badge.svg)

## Description
<!-- BEGIN Description -->
The Ansible Role `sap_install_media_detect` is used to detect and extract SAP installation media.

This role searches provided source directory, sorts files based on type and extracts them to target directory.<br>
Extraction can be further adjusted to create individual folders based on defined inputs.

Detection of supported installation media is available for SAP HANA and wide range of SAP Applications like:

- SAP S/4HANA
- SAP BW/4HANA
- SAP ECC
- SAP BW
- SAP WebDispatcher
- SAP Business Applications based upon SAP NetWeaver
- Other SAP products based on SAP NetWeaver
<!-- END Description -->

<!-- BEGIN Dependencies -->
<!-- END Dependencies -->

<!-- BEGIN Prerequisites -->
## Prerequisites
Managed nodes:

- Directory with SAP Installation media is present and `sap_install_media_detect_source_directory` updated. Download can be completed using [community.sap_launchpad](https://github.com/sap-linuxlab/community.sap_launchpad) Ansible Collection.
<!-- END Prerequisites -->

## Execution
<!-- BEGIN Execution -->
<!-- END Execution -->

<!-- BEGIN Execution Recommended -->
### Recommended
It is recommended to execute this role together with other roles in this collection, in the following order:</br>
#### SAP HANA
1. [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure)
2. [sap_hana_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_preconfigure)
3. *`sap_install_media_detect`*
4. [sap_hana_install](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_install)
5. [sap_ha_install_hana_hsr](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_install_hana_hsr) - High Availability specific
6. [sap_ha_pacemaker_cluster](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_pacemaker_cluster) - High Availability specific

#### SAP Netweaver
1. [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure)
2. [sap_netweaver_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_netweaver_preconfigure) 
3. *`sap_install_media_detect`*
4. [sap_swpm](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_swpm)
5. [sap_ha_pacemaker_cluster](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_pacemaker_cluster) - High Availability specific
<!-- END Execution Recommended -->

### Execution Flow
<!-- BEGIN Execution Flow -->
1. At the beginning of the execution of the role, a new tool `sapfile` is pushed to a temporary directory on the managed node.
2. Also a package which contains a command for extracting and listing content of files of type `RAR` is installed.
3. The next step is to check if source and/or target directories exist. If role parameter `sap_install_media_detect_target_directory` is defined, files will later be copied from `sap_install_media_detect_source_directory`. This is the `remote_dir` case.
4. If the system on which the `sap_install_media_detect_source_directory` is not writable, the role would normally fail because one or both of the following conditions are not met:
    - The SAPCAR EXE file is not executable.
    - There are one or more `ZIP` or `RAR` files without extension.
5. In this `remote_dir` case, to make sure the role does not fail, it needs to be run first on the node on which `sap_install_media_detect_source_directory` is writable, with role parameter `sap_install_media_detect_file_server_only` set to `true` so the role will not perform and further file detection activities.
6. After the SAPCAR EXE file is executable and there are no more `ZIP` or `RAR` files without extension, the role can be called on a managed node where `sap_install_media_detect_source_directory` is not writable.
7. A new list of all files with the correct final file names will then be created, and for each of the files, the SAP file types are determined using the `sapfile` tool, either using the file names or - if this information is not sufficient - from information inside the file.
8. We then assert that there is at least (or exactly, depending on the file type) one file available for each of the `sap_install_media_detect_*` parameters. For example, if `sap_install_media_detect_kernel_db` is set to `saphana`, then there must be one SAP Kernel DB dependent file for SAP HANA.
9. In case of `remote_dir`, the next step is to copy all files from `sap_install_media_detect_source_directory` to `sap_install_media_detect_target_directory`.
10. Then we extract files which are configured in `sapfile` to be extracted, and copy or move files which are configured in `sapfile` to be copied or moved. Certain files like `SAPCAR*.EXE` and the SAP Host Agent will be copied to two different directories.
11. Once all necessary files have been extracted and all files are copied or moved to where we want them to be, we are using the Ansible find module to identify the different file types by using file or directory name patterns.
12. The last step is to fill all required `sap_swpm` parameters from the result of the previous find step, and display all the variables.
    - Once detection (e.g. using `zipinfo -1` and `unrar lb`) and extraction are completed, the file paths are shown and stored as variables for subsequent use by other Ansible Tasks.

#### (Red Hat) Additional steps for RAR files

RAR files can be either handled by the unar package from EPEL or by another package which can list the contents of, and extract files from, RAR files.<br>
See the comments and examples for the RAR file handling in `defaults/main.yml`.

- If the EPEL repo had been enabled at the time when the role was run, it will remain enabled.
- If the EPEL repo was not present, the associated GPG key will be removed and the EPEL repo will be disabled as the last task.
<!-- END Execution Flow -->

### Example
<!-- BEGIN Execution Example -->
Example playbook to extract SAP Installation media for SAP ASCS Netweaver.
```yaml
---
- name: Ansible Play for SAP NetWeaver ASCS - Extract SAP Installation media
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
```
<!-- END Execution Example -->

<!-- BEGIN Role Tags -->
### Role Tags
With the following tags, the role can be called to perform certain activities only:

- tag `sap_install_media_detect_zip_handling`: Only perform the task for enabling the listing and extracting of files of type `ZIP`.
- tag `sap_install_media_detect_rar_handling`: Only perform the tasks for enabling the listing and extracting of files of type `RAR`. This
  includes enabling and disabling the EPEL repo for RHEL systems, if desired.
- tag `sap_install_media_detect_add_file_extension`: Add file name extensions to any files in `sap_install_media_detect_source_directory` which are of type `RAR` or `ZIP` and have no ending. Needs to be used with tag `sap_install_media_detect_create_file_list_phase_1`.
- tag `sap_install_media_detect_check_directories`: Find out if the directory `sap_install_media_detect_target_directory` or `sap_install_media_detect_source_directory` is writable.
- tag `sap_install_media_detect_provide_sapfile_utility `: Provides the sapfile utility on the managed node. This tool is required for determining the SAP file type.
- tag `sap_install_media_detect_create_file_list_phase_1`: Create a list of all files in `sap_install_media_detect_source_directory`, and create a list of any files which have no ending and are of type `RAR`.
- tag `sap_install_media_detect_create_file_list_phase_2`: Create a final list of all required files in `sap_install_media_detect_source_directory` or `sap_install_media_detect_target_directory` (if that one is defined)
- tag `sap_install_media_detect_organize_files`: Copies all required files from `sap_install_media_detect_source_directory` or `sap_install_media_detect_target_directory` (if that one is defined) and extracts all required files into the target directories if specified by the output of the sapfile command.
- tag `sap_install_media_detect_move_files_to_main_directory`: Move SAP archive files from level 1 subdirectories (where they might reside after the role has been used initially) back to the main software directory. Those subdirectories will afterwards be removed. This is to make sure the role will produce the same result no matter how often it is executed (= idempotency). The directories with pattern `*_extracted` will remain in place.
- tag `sap_install_media_detect_find_files_after_extraction`: Finds all required files after they have been extracted so the final variables can be filled in the next step.
- tag `sap_install_media_detect_set_global_vars`: Set all final variables for later use by Ansible roles or tasks.

**Note:** After running the role with the following four tags, the SAP archive files will be in the same place as before running the role the first time.<br>
The directories with pattern `*_extracted` will remain in place.

- `sap_install_media_detect_provide_sapfile_utility`
- `sap_install_media_detect_check_directories`
- `sap_install_media_detect_create_file_list_phase_1`
- `sap_install_media_detect_move_files_to_main_directory`
<!-- END Role Tags -->

<!-- BEGIN Further Information -->
## Further Information
For more examples on how to use this role in different installation scenarios, refer to the [ansible.playbooks_for_sap](https://github.com/sap-linuxlab/ansible.playbooks_for_sap) playbooks.
<!-- END Further Information -->

## License
<!-- BEGIN License -->
Apache 2.0
<!-- END License -->

## Maintainers
<!-- BEGIN Maintainers -->
- [Bernd Finger](https://github.com/berndfinger)
<!-- END Maintainers -->

## Role Variables
<!-- BEGIN Role Variables -->
### sap_install_media_detect_rar_handling

- _Type:_ `bool`
- _Default:_ `True`

Set this parameter to `false` for skipping the handling of RAR files. In this case, also no `unar` or other RAR handling software will be installed.


### sap_install_media_detect_rar_package

- _Type:_ `str`
- _Default:_ `EPEL`

Set this parameter to use either the `unar` package from `EPEL` or another software package for handling RAR files.</br>
Based on this setting, the commands for listing and extracting RAR files are being set in tasks/prepare/enable_rar_handling.yml

### sap_install_media_detect_epel_gpg_key_url

- _Type:_ `str`
- _Default:_ `https://download.fedoraproject.org/pub/epel/RPM-GPG-KEY-EPEL-{{ ansible_distribution_major_version }}`

URL for the EPEL GPG key

### sap_install_media_detect_use_rpm_key_module_for_removing_the_key

- _Type:_ `bool`
- _Default:_ `True`

The `EPEL` GPG key can be removed with the rpm_key module and the URL for the key, or by using the `rpm -e` command.</br>
For using the rpm -e command, set this variable to 'false'.

### sap_install_media_detect_file_server_only

- _Type:_ `bool`
- _Default:_ `False`

If this role is running on a file server on which the SAP software is not to be installed, set the following to true.</br>
If this role is running on a system on which the SAP software is to be installed, set the following to false.

### sap_install_media_detect_rar_list

- _Type:_ `str`
- _Default:_ `/usr/bin/unrar lb`

Fully qualified path to the program for listing RAR files, including the argument for listing files.</br>
If not specified, the `lsar` program (or a link with the name `lsar`, pointing to the actual `lsar` program) is expected to be located in one of the PATH directories.</br>
If sap_install_media_detect_rar_package is set to `EPEL`, this variable is not used.

### sap_install_media_detect_rar_extract

- _Type:_ `str`
- _Default:_ `/usr/bin/unrar x`

Fully qualified path to the program for extracting RAR files, including the argument for extracting files.</br>
If not specified, the `unar` program (or a link with the name `unar`, pointing to the actual `unar` program) is expected to be located in one of the PATH directories.</br>
If sap_install_media_detect_rar_package is set to `EPEL`, this variable is not used.

### sap_install_media_detect_rar_extract_directory_argument

- _Type:_ `str`

Fully qualified path to an additional argument to the program for extracting RAR files, for specifying the directory into which the archive is to be extracted.</br>
Needs to be empty or start with a space character.</br>
If sap_install_media_detect_rar_package is set to 'EPEL', this variable is not used.

### sap_install_media_detect_source_directory

- _Type:_ `str`
- _Default:_ `/software`

Directory where the SAP software is located

### sap_install_media_detect_target_directory

- _Type:_ `str`

Directory where the SAP software is located after the role is run, if different from `sap_install_media_detect_source_directory`

### sap_install_media_detect_create_target_directory

- _Type:_ `bool`
- _Default:_ `True`

Create target directory if it does not yet exist. If set to false, perform a check only

### sap_install_media_detect_rename_target_file_exists

- _Type:_ `str`
- _Default:_ `skip`

If there are two files of the same RAR or ZIP type, one with and one without suffix, the following parameter will determine what the role will do for such a file:</br>
- `skip` the file renaming.
- `fail` execution.
- `overwrite` the file with the suffix by the file without suffix.

### sap_install_media_detect_extract_archives

- _Type:_ `bool`
- _Default:_ `True`

If you want the role to not extract archives which have the extract flag set, set the following parameter to `false`.

### sap_install_media_detect_move_or_copy_archives

- _Type:_ `bool`
- _Default:_ `True`

If you want the role to not move or copy archive files to the `target_dir` subdirectories, set the following parameter to `false`.

### sap_install_media_detect_assert_after_sapfile

- _Type:_ `bool`
- _Default:_ `True`

By default, the presence of at least one file for each file type according to the configured role parameters is asserted. Set the following parameter to 'false' to skip this step.

### sap_install_media_detect_db

- _Type:_ `str`

Select which database type to detect.</br>
Available values: `saphana`, `sapase`, `sapmaxdb`, `oracledb`, `ibmdb2`

### sap_install_media_detect_db_client

- _Type:_ `str`

Select which database client to detect.</br>
Available values: `saphana`, `sapase`, `sapmaxdb`, `oracledb`, `ibmdb2`

### sap_install_media_detect_swpm

- _Type:_ `bool`
- _Default:_ `False`

Enable to detect SWPM.

### sap_install_media_detect_hostagent

- _Type:_ `bool`
- _Default:_ `False`

Enable to detect SAP Hostagent.

### sap_install_media_detect_igs

- _Type:_ `bool`
- _Default:_ `False`

Enable to detect SAP IGS.

### sap_install_media_detect_kernel

- _Type:_ `bool`
- _Default:_ `False`

Enable to detect SAP Kernel files.

### sap_install_media_detect_kernel_db

- _Type:_ `str`

Select which database kernel to detect.</br>
Available values: `saphana`, `sapase`, `sapmaxdb`, `oracledb`, `ibmdb2`</br>
Only necessary if there is more than one SAPEXEDB file in the source directory

### sap_install_media_detect_webdisp

- _Type:_ `bool`
- _Default:_ `False`

Enable to detect SAP Web Dispatcher.

### sap_install_media_detect_mpstack

- _Type:_ `bool`
- _Default:_ `False`

Enable to detect SAP Maintenance Planner stack file.

### sap_install_media_detect_export

- _Type:_ `str`

Select which database export to detect.</br>
Available values: `saps4hana`, `sapbw4hana`, `sapecc`, `sapecc_ides`, `sapnwas_abap`, `sapnwas_java`, `sapsolman_abap`, `sapsolman_java`
<!-- END Role Variables -->