# sap_install_media_detect Ansible Role

Ansible Role for detection and extraction of SAP Software installation media

This role is used to prepare for installation of SAP Software, by searching a given directory for SAP installation media (e.g. SAR files),
moving files to subdirectories (i.e. `/sap_hana` and `/sap_swpm`) with the directory/file ownership permissons, then extracting the detected files.

Detection of installation media is available for SAP HANA and the various key installation files when using SAP SWPM to install
SAP Business Applications based upon SAP NetWeaver (e.g. SAP S/4HANA, SAP BW/4HANA, SAP ECC, SAP BW, SAP WebDispatcher etc).
As an example, SAP HANA Client would be detected and the SAP Kernel Part I/II would be detected.

Once detection (e.g. using `zipinfo -1` and `unrar lb`) and extraction are completed, the file paths are shown and stored as variables for subsequent use by other Ansible Tasks.

RAR files can be either handled by the unar package from EPEL or by another package which can list the contents of, and extract files from,
RAR files. See the comments and examples for the RAR file handling in `defaults/main.yml`. If the EPEL repo had been enabled at the time
when the role was run, it will remain enabled. If the EPEL repo was not present, the associated GPG key will be removed and the EPEL repo
will be disabled as the last task.

## Dependencies

This role does not depend on any other Ansible Role.

## Tags

With the following tags, the role can be called to perform certain activities only:
- tag `sap_install_media_detect_rar_handling`: Only perform the tasks for enabling the listing and extracting of files of type `RAR`. This
  includes enabling and disabling the EPEL repo for RHEL systems, if desired.
- tag `sap_install_media_detect_add_rar_extension`: Only add `.rar` to any files in `sap_install_media_detect_source_directory` which are of type `RAR` and have no ending. Needs to be used with tag `sap_install_media_detect_create_file_list`.
- tag `sap_install_media_detect_check_directories`: Find out if the directory `sap_install_media_detect_target_directory` or `sap_install_media_detect_source_directory` is writable.
- tag `sap_install_media_detect_create_file_list`: Only create a list of all files in `sap_install_media_detect_source_directory`, and create a list of any files which have no ending and are of type `RAR`.

## License

Apache license 2.0

## Author Information

IBM Lab for SAP Solutions, Red Hat for SAP Community of Practice, Bernd Finger
