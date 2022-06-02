# sap_hostagent Ansible Role

SAP Host Agent is an agent that can accomplish several life-cycle management tasks, such as operating system monitoring, database monitoring, system instance control and provisioning.

It is recommended to install SAP Host Agent upfront in any HA environment.

You can find the latest Documentation in [SAP NOTE 1907566](https://launchpad.support.sap.com/#/notes/1907566)

This role installs or updates the SAP Host Agent on a RHEL 7.x or 8.x system. It is provided as RPM package, tarball or as part of an SAP softwarebundle.
While Red Hat recommends RPM for easier upgrade, this role take care of all formats.

## Requirements

This role is intended to use on a RHEL system that gets SAP software.
So your system needs to be installed with at least the RHEL core packages, properly registered and prepared for HANA or Netweaver installation.

It needs access to the software repositories required to install SAP HANA (see also: [How to subscribe SAP HANA systems to the Update Services for SAP Solutions](https://access.redhat.com/solutions/3075991))

You can use the [redhat_sap.sap_rhsm](https://galaxy.ansible.com/redhat_sap/sap_rhsm) Galaxy Role to automate this process

To install SAP software on Red Hat Enterprise Linux you need some additional packages which come in a special repository. To get this repository you need to have one
of the following products:

- [RHEL for SAP Solutions](https://access.redhat.com/solutions/3082481) (premium, standard, developer Edition)
- [RHEL for Business Partner NFRs](https://partnercenter.redhat.com/NFRPageLayout)

[Click here](https://developers.redhat.com/products/sap/download/) to achieve a personal developer edition of RHEL for SAP Solutions. Please register as a developer and download the developer edition.

- [Registration Link](http://developers.redhat.com/register) :
  Here you can either register a new personal account or link it to an already existing **personal** Red Hat Network account.
- [Download Link](https://access.redhat.com/downloads/):
  Here you can download the Installation DVD for RHEL with your previously registered account

*NOTE:* This is a regular RHEL installation DVD as RHEL for SAP Solutions is no additional
 product but only a special bundling. The subscription grants you access to the additional
 packages through our content delivery network(CDN) after installation.

It is also important that your disks are setup according to the [SAP storage requirements for SAP HANA](https://www.sap.com/documents/2015/03/74cdb554-5a7c-0010-82c7-eda71af511fa.html). This [BLOG](https://blogs.sap.com/2017/03/07/the-ultimate-guide-to-effective-sizing-of-sap-hana/) is also quite helpful when sizing HANA systems.

## Role Variables

### RPM based installations

| variable | info | required? |
|:--------:|:----:|:---------:|
|sap_hostagent_installation_type|Source type of the installation for SAPHOSTAGENT|yes, with `rpm` value|
|sap_hostagent_rpm_local_path|Local directory path where RPM file is located|yes, unless `sap_hostagent_rpm_remote_path` is used|
|sap_hostagent_rpm_remote_path|Local directory path where RPM file is located|yes, unless `sap_hostagent_rpm_local_path` is used|
|sap_hostagent_rpm_file_name|Local RPM file name|yes|
|sap_hostagent_agent_tmp_directory|Temporary directory path that will be created on the target host|no (defaulted in the role)|
|sap_hostagent_clean_tmp_directory|Boolean variable to indicate if the temporary directory will be removed or not afer the installation| no (defaulted in the role)|

### SAR based installations (content on ansible control node)

| variable | info | required? |
|:--------:|:----:|:---------:|
|sap_hostagent_installation_type|Source type of the installation for SAPHOSTAGENT|yes with `sar` value|
|sap_hostagent_sar_local_path|Local directory path where SAR file is located|yes|
|sap_hostagent_sar_file_name|Local SAR file name|yes|
|sap_hostagent_sapcar_local_path|Local directory path where SAPCAR tool file is located|yes|
|sap_hostagent_sapcar_file_name|Local SAPCAR tool file name|yes|
|sap_hostagent_agent_tmp_directory|Temporary directory path that will be created on the target host|no (defaulted in the role)|
|sap_hostagent_clean_tmp_directory|Boolean variable to indicate if the temporary directory will be removed or not afer the installation| no (defaulted in the role)|

### SAR based installations (with content existing on target node)

| variable | info | required? |
|:--------:|:----:|:---------:|
|sap_hostagent_installation_type|Source type of the installation for SAPHOSTAGENT|yes with `sar-remote` value|
|sap_hostagent_sar_remote_path|Remote directory path where SAR tool file is located|yes|
|sap_hostagent_sar_file_name|SAR tool file name|yes|
|sap_hostagent_sapcar_remote_path|Remote directory path of SAR archive|yes|
|sap_hostagent_sapcar_file_name|Remote file name of SAR archive|yes|
|sap_hostagent_agent_tmp_directory|Temporary directory path that will be created on the target host|no (defaulted in the role)|
|sap_hostagent_clean_tmp_directory|Boolean variable to indicate if the temporary directory will be removed or not afer the installation| no (defaulted in the role)|


### SAP Bundle based installations

| variable | info | required? |
|:--------:|:----:|:---------:|
|sap_hostagent_installation_type|Source type of the installation for SAPHOSTAGENT|yes with `bundle` value|
|sap_hostagent_bundle_path|Target host directory path where SAP Installation Bundle has been unarchived|
|sap_hostagent_agent_tmp_directory|Temporary directory path that will be created on the target host|no (defaulted in the role)|
|sap_hostagent_clean_tmp_directory|Boolean variable to indicate if the temporary directory will be removed or not afer the installation| no (defaulted in the role)|

### SSL Configuration

Right now the role will configure the PSE and create a CSR. Adding signed certificates from a valid CA is not supported yet

| variable | info | required? |
|:--------:|:----:|:---------:|
|sap_hostagent_config_ssl|This boolean variable will configure Agent for SSL communication|no (defaulted in the role)|
|sap_hostagent_ssl_passwd|Password to be used for the CSR|yes when `sap_hostagent_config_ssl` True|
|sap_hostagent_ssl_org|Organization information for the CSR|yes when `sap_hostagent_config_ssl` True|
|sap_hostagent_ssl_country|Country information for the CSR|yes when `sap_hostagent_config_ssl` True|

## Dependencies

Before using this role ensure your system has been configured properly to run SAP applications.

You can use the supported role `sap_general_preconfigure` comming with RHEL 7 and 8 with RHEL for SAP Solutions Subscription

The upstream version of this role can be found [here](https://github.com/linux-system-roles/sap_general_preconfigure)

## Example Playbook

```yaml
    - hosts: servers
      roles:
      - role: sap_hostagent
```

## Example Inventory

When using RPM:

```yaml
sap_hostagent_installation_type: "rpm"
sap_hostagent_rpm_local_path: "/mylocaldir/SAPHOSTAGENT"
sap_hostagent_rpm_file_name: "saphostagentrpm_44-20009394.rpm"
sap_hostagent_clean_tmp_directory: true
```

When using SAR:

```yaml
sap_hostagent_installation_type: "sar"
sap_hostagent_sar_local_path: "/mylocaldir/SAPHOSTAGENT"
sap_hostagent_sar_file_name: "SAPHOSTAGENT44_44-20009394.SAR"
sap_hostagent_sapcar_local_path: "/mylocaldir/SAPHOSTAGENT"
sap_hostagent_sapcar_file_name: "SAPCAR_1311-80000935.EXE"
sap_hostagent_clean_tmp_directory: true
```

When using SAP Bundle:

```yaml
sap_hostagent_installation_type: "bundle"
sap_hostagent_bundle_path: "/usr/local/src/HANA-BUNDLE/51053381"
sap_hostagent_clean_tmp_directory: true
```

## License

Apache license 2.0

## Author Information

IBM Lab for SAP Solutions, Red Hat for SAP Community of Practice
