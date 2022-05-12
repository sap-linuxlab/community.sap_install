# sap_install_media_detect Ansible Role

Ansible Role for detection and extraction of SAP Software installation media

This role is used to prepare for installation of SAP Software, by searching a given directory for SAP installation media (e.g. SAR files),
moving files to subdirectories (i.e. `/sap_hana` and `/sap_swpm`) with the directory/file ownership permissons, then extracting the detected files.

Detection of installation media is available for SAP HANA and the various key installation files when using SAP SWPM to install
SAP Business Applications based upon SAP NetWeaver (e.g. SAP S/4HANA, SAP BW/4HANA, SAP ECC, SAP BW, SAP WebDispatcher etc).
As an example, SAP HANA Client would be detected and the SAP Kernel Part I/II would be detected.

Once detection and extraction are completed, the file paths are shown and stored as variables for subsequent use by other Ansible Tasks.

## Dependencies

This role does not depend on any other Ansible Role.

## License

Apache license 2.0

## Author Information

IBM Lab for SAP Solutions, Red Hat for SAP Community of Practice
