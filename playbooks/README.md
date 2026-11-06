
# Ansible Collection Playbooks

The playbooks in this directory are samples of how to use the roles of this collection.<br>
Each `sample-` playbook shows one role or scenario with the mandatory variables only, so copy it and adapt it for your own playbooks.<br>
The header of every sample lists its prerequisites and refers to the README of the role for all available variables.

> **NOTE: For complete end-to-end deployments of SAP systems, use [ansible.playbooks_for_sap](https://github.com/sap-linuxlab/ansible.playbooks_for_sap) (AP4S).**<br>
> It is the collection of ready-to-use playbooks, which combine the roles of this collection into full scenarios.<br>
> The samples here intentionally cover a single role each.

## Samples

All host groups, hostnames, addresses and passwords are placeholders.<br>
Passwords in the samples are examples only, do not use them. Protect real credentials, e.g. with `ansible-vault`.

| Area | Sample | Shows |
| --- | --- | --- |
| Preconfigure | `sample-sap-general-preconfigure.yml` | Role `sap_general_preconfigure` |
| Preconfigure | `sample-sap-hana-preconfigure.yml` | Roles `sap_general_preconfigure` and `sap_hana_preconfigure` |
| Preconfigure | `sample-sap-netweaver-preconfigure.yml` | Roles `sap_general_preconfigure` and `sap_netweaver_preconfigure` |
| Storage | `sample-sap-storage-setup.yml` | Role `sap_storage_setup` with multipath, striped and plain block disks, swap disk, swap file and NFS mount |
| Installation media | `sample-sap-install-media-detect.yml` | Role `sap_install_media_detect` for SAP HANA, ASCS and PAS hosts |
| SAP HANA | `sample-sap-hana-install-scaleup.yml` | Role `sap_hana_install`, scale-up system |
| SAP HANA | `sample-sap-hana-install-scaleout.yml` | Role `sap_hana_install`, scale-out system |
| SAP SWPM | `sample-sap-swpm-role-variables.yml` | Role `sap_swpm` with role variables, installation or restore |
| SAP SWPM | `sample-sap-swpm-templates.yml` | Role `sap_swpm` with `sap_swpm_templates_install_dictionary` |
| SAP SWPM | `sample-sap-swpm-existing-inifile.yml` | Role `sap_swpm` with an existing `inifile.params` |
| High Availability | `sample-sap-ha-pacemaker-cluster-hana-scale-up.yml` | Role `sap_ha_pacemaker_cluster`, SAP HANA scale-up cluster |
| High Availability | `sample-sap-ha-pacemaker-cluster-ascs-ers.yml` | Role `sap_ha_pacemaker_cluster`, SAP NetWeaver ASCS and ERS cluster |

The directory `vars` contains the variable files used by the SWPM samples, because their variable sets are too long to read inline.

For SAP HANA System Replication, see the example in the README of the role `sap_ha_install_hana_hsr`.

## Usage

Copy a sample and adapt the host groups and variables for your environment. Then run it against your inventory:

```bash
ansible-playbook -i my_inventory sample-sap-hana-install-scaleup.yml
```

When running against remote hosts, the connection user needs to be able to become root.<br>
Pass `-u <user>` for the SSH user, `-k` to ask for the SSH password and `-K` to ask for the privilege escalation password, if they are required.

> **NOTE:** Use `--check` first with the sample `sample-sap-storage-setup.yml`, to review changes before disks are configured.

## Plugin tests

The playbooks starting with `test-` test the plugins of this collection and are not samples for users.

> **NOTE:** Playbooks with a hyphen in the file name cannot be called directly by `ansible-playbook` using the collection name.<br>
> That is why all playbooks in this directory are meant to be copied or run by their file path.

