## Input Parameters for sap_install_media_detect Ansible Role
<!-- BEGIN Role Input Parameters -->
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

Fully qualified path to an additional argument to the program for extracting RAR files, for specifying the directory into which the archive is to be extracted. Needs to be empty or start with a space character.</br>
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

If there are two files of the same RAR or ZIP type, one with and one without suffix, the following parameter will determine what the role will do for such a file: `skip` the file renaming, `fail`, or `overwrite` the file with the suffix by the file without suffix

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

Select which database type to detect: `saphana`, `sapase`, `sapmaxdb`, `oracledb`, `ibmdb2`

### sap_install_media_detect_db_client

- _Type:_ `str`

Select which database client to detect: `saphana`, `sapase`, `sapmaxdb`, `oracledb`, `ibmdb2`

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

Select which database kernel to detect: `saphana`, `sapase`, `sapmaxdb`, `oracledb`, `ibmdb2`</br
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

Select which database export to detect: `saps4hana`, `sapbw4hana`, `sapecc`, `sapecc_ides`, `sapnwas_abap`, `sapnwas_java`, `sapsolman_abap`, `sapsolman_java`
<!-- END Role Input Parameters -->