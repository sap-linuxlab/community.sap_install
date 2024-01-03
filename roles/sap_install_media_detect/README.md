# sap_install_media_detect Ansible Role

Ansible Role for detection and extraction of SAP Software installation media

This role is used to prepare for installation of SAP Software, by searching a given directory for SAP installation media (e.g. SAR files),
moving files to subdirectories (i.e. `/sap_hana` and `/sap_swpm`) with the directory/file ownership permissions, then extracting the detected files.

Detection of installation media is available for SAP HANA and the various key installation files when using SAP SWPM to install
SAP Business Applications based upon SAP NetWeaver (e.g. SAP S/4HANA, SAP BW/4HANA, SAP ECC, SAP BW, SAP WebDispatcher etc).
As an example, SAP HANA Client would be detected and the SAP Kernel Part I/II would be detected.

Once detection (e.g. using `zipinfo -1` and `unrar lb`) and extraction are completed, the file paths are shown and stored as variables for subsequent use by other Ansible Tasks.

RAR files can be either handled by the unar package from EPEL or by another package which can list the contents of, and extract files from,
RAR files. See the comments and examples for the RAR file handling in `defaults/main.yml`. If the EPEL repo had been enabled at the time
when the role was run, it will remain enabled. If the EPEL repo was not present, the associated GPG key will be removed and the EPEL repo
will be disabled as the last task.

## Execution Flow

- At the beginning of the execution of the role, a new tool `sapfile` is pushed to a temporary directory on the managed node.
- Also a package which contains a command for extracting and listing content of files of type `RAR` is installed.
- The next step is to check if source and/or target directories exist. If role parameter `sap_install_media_detect_target_directory` is defined, files will later be copied from `sap_install_media_detect_source_directory`. This is the `remote_dir` case.
- If the system on which the `sap_install_media_detect_source_directory` is not writable, the role would normally fail because one or both of the following conditions are not met:
  - The SAPCAR EXE file is not executable.
  - There are one or more `ZIP` or `RAR` files without extension.
- In this `remote_dir` case, to make sure the role does not fail, it needs to be run first on the node on which `sap_install_media_detect_source_directory` is writable, with role parameter `sap_install_media_detect_file_server_only` set to `true` so the role will not perform and further file detection activities.
- After the SAPCAR EXE file is executable and there are no more `ZIP` or `RAR` files without extension, the role can be called on a managed node where `sap_install_media_detect_source_directory` is not writable.
- A new list of all files with the correct final file names will then be created, and for each of the files, the SAP file types are determined using the `sapfile` tool, either using the file names or - if this information is not sufficient - from information inside the file.
- We then assert that there is at least (or exactly, depending on the file type) one file available for each of the `sap_install_media_detect_*` parameters. For example, if `sap_install_media_detect_kernel_db` is set to `saphana`, then there must be one SAP Kernel DB dependent file for SAP HANA.
- In case of `remote_dir`, the next step is to copy all files from `sap_install_media_detect_source_directory` to `sap_install_media_detect_target_directory`.
- Then we extract files which are configured in `sapfile` to be extracted, and copy or move files which are configured in `sapfile` to be copied or moved. Certain files like `SAPCAR*.EXE` and the SAP Host Agent will be copied to two different directories.
- Once all necessary files have been extracted and all files are copied or moved to where we want them to be, we are using the Ansible find module to identify the different file types by using file or directory name patterns.
- The last step is to fill all required `sap_swpm` parameters from the result of the previous find step, and display all the variables.

## Variables and Parameters

See the file `defaults/main.yml`.

## Dependencies

This role does not depend on any other Ansible Role.

## Tags

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

Note: After running the role with the following four tags, the SAP archive files will be in the same place as before running the role the first time. The directories with pattern `*_extracted` will remain in place.
`sap_install_media_detect_provide_sapfile_utility,sap_install_media_detect_check_directories,sap_install_media_detect_create_file_list_phase_1,sap_install_media_detect_move_files_to_main_directory`

## License

Apache license 2.0

## Author Information

IBM Lab for SAP Solutions, Red Hat for SAP Community of Practice, Bernd Finger
