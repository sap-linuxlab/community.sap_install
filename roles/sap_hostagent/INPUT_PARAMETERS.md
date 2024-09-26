## Input Parameters for sap_hostagent Ansible Role
<!-- BEGIN Role Input Parameters -->

### sap_hostagent_installation_type

- _Type:_ `string`
- _Default:_ `rpm`

Select type of installation source for SAPHOSTAGENT.</br>
Available options: `sar`, `sar-remote`, `bundle`, `rpm`


## Input Parameters for SAR
Following input parameters are used by both Local SAR and Remote SAR.

### sap_hostagent_sar_file_name

- _Type:_ `string`

Name of SAR file containing SAPHOSTAGENT.

### sap_hostagent_sapcar_file_name

- _Type:_ `string`

Name of SAR file containing SAPCAR.

## Input Parameters for Local SAR

### sap_hostagent_sar_local_path

- _Type:_ `string`

Local directory path where SAR file is located. Do not use together with `sap_hostagent_sar_remote_path`.

### sap_hostagent_sapcar_local_path

- _Type:_ `string`

Local directory path where SAPCAR file is located. Do not use together with `sap_hostagent_sapcar_remote_path`.

## Input Parameters for Remote SAR

### sap_hostagent_sar_remote_path

- _Type:_ `string`

Remote directory path where SAR file is located. Do not use together with `sap_hostagent_sar_local_path`.

### sap_hostagent_sapcar_remote_path

- _Type:_ `string`

Local directory path where SAPCAR file is located. Do not use together with `sap_hostagent_sapcar_local_path`.


## Input Parameters for RPM

### sap_hostagent_rpm_local_path

- _Type:_ `string`

Local directory path where RPM file is located. Do not use together with `sap_hostagent_rpm_remote_path`.

### sap_hostagent_rpm_remote_path

- _Type:_ `string`

Remote directory path where RPM file is located. Do not use together with `sap_hostagent_rpm_local_path`.

### sap_hostagent_rpm_file_name

- _Type:_ `string`

Name of RPM package containing SAPHOSTAGENT.


## Input Parameters for SAP Bundle

### sap_hostagent_bundle_path

- _Type:_ `string`

Remote directory path where SAP Bundle file is located after being extracted.


## Input Parameters for SSL setup

### sap_hostagent_config_ssl

- _Type:_ `bool`
- _Default:_ `False`

Enable to configure PSE and create CSR.</br>
Adding signed certificates from a valid CA is not supported yet.

### sap_hostagent_ssl_passwd

- _Type:_ `string`

Enter password for the CSR. It is used when `sap_hostagent_config_ssl` is set.

### sap_hostagent_ssl_org

- _Type:_ `string`

Enter Organization information for the CSR. It is used when `sap_hostagent_config_ssl` is set.

### sap_hostagent_ssl_country

- _Type:_ `string`

Enter Country information for the CSR. It is used when `sap_hostagent_config_ssl` is set.


### sap_hostagent_agent_tmp_directory

- _Type:_ `string`
- _Default:_ `/tmp/hostagent`

Temporary directory for processing of source file.

### sap_hostagent_clean_tmp_directory

- _Type:_ `bool`
- _Default:_ `False`

Enable to remove temporary directory after installation.

<!-- END Role Input Parameters -->