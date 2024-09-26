<!-- BEGIN Title -->
# sap_storage_setup Ansible Role
<!-- END Title -->
![Ansible Lint for sap_storage_setup](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_storage_setup.yml/badge.svg)

## Description
<!-- BEGIN Description -->
Ansible Role `sap_storage_setup` is used to prepare a host with the storage requirements of an SAP System (prior to software installation).

This role can prepare host with:
- Local block storage volume setup as LVM Logical Volumes, Filesystem formatting and mount to defined directory path
- Remote file storage mount (and subdirectories as required)
- SWAP file or SWAP partition

This Ansible Role is agnostic, and will run on any Infrastructure Platform. Only LVM is used for local/block storage, to allow for further expansion if the SAP System requires further storage space in the future.
<!-- END Description -->

<!-- BEGIN Dependencies -->
## Dependencies
- `community.general`
    - Modules:
        - `lvg`
        - `lvol`
        - `filesystem`
Install required collection by `ansible-galaxy install community.general`.
<!-- END Dependencies -->

<!-- BEGIN Prerequisites -->
## Prerequisites
Managed nodes:
- All local/block storage volumes must be attached to the host
- All remote/file storage mounts must be available with host accessibility (e.g. port 2049).
<!-- END Prerequisites -->

## Execution
<!-- BEGIN Execution -->
**:warning: Do not execute this Ansible Role against existing SAP systems unless you know what you are doing and you prepare inputs to avoid unintended changes caused by default inputs.**</br>
:warning: While this Ansible Role has protection against overwrite of existing disks and filesystems - sensible review and care is required for any automation of disk storage. Please review the documentation and samples/examples carefully. It is strongly suggested to initially execute the Ansible Playbook calling this Ansible Role, with `ansible-playbook --check` for Check Mode - this will perform no changes to the host and show which changes would be made.

Role can be executed independently or as part of [ansible.playbooks_for_sap](https://github.com/sap-linuxlab/ansible.playbooks_for_sap) playbooks.

**Considerations**
- This role does not permit static definition for mountpoint to use a specific device (e.g. `/dev/sdk`). The definition will define the disk size to use for the mountpoint, and match accordingly.
- This role enforces that 1 mountpoint will use 1 LVM Logical Volume (LV) that consumes 100% of an LVM Volume Group (VG), with the LVM Volume Group (VG) consuming 100% of 1..n LVM Physical Volumes (PV).
    - Following roles and modules offer alternative for more granular control of LVM setup:
        - Role `storage` from [fedora.linux_system_roles](https://github.com/linux-system-roles/storage)
        - Modules `filesystem`, `lvg`, `lvol` from [community.general](https://galaxy.ansible.com/ui/repo/published/community/general/)
<!-- END Execution -->

<!-- BEGIN Execution Recommended -->
<!-- END Execution Recommended -->

### Execution Flow
<!-- BEGIN Execution Flow -->
1. Gather facts about hosts.
2. Create list of unused disk devices
3. Match/Map unused disk devices to the `sap_storage_setup_definition`
4. Create LVM Logical Volumes (and prerequisite LVM Volume Groups and LVM Physical Volumes)
5. Create swap file or swap partition
6. Mount NFS temporarily, create required subdirectories, unmount and mount subdirectory on the NFS share
<!-- END Execution Flow -->

<!-- BEGIN Execution Example -->
Example playbook to configure SAP HANA OneHost node on AWS that includes:
- 3 disks for `/hana/data`, `/hana/log` and ` /hana/shared`
- Remote filesystem for `/software`
- SWAP
```yaml
---
- name: Ansible Play for SAP HANA HA storage setup
  hosts: hana_primary
  become: true
  tasks:
    - name: Execute Ansible Role sap_storage_setup
      ansible.builtin.include_role:
        name: community.sap_install.sap_storage_setup
      vars:
        sap_storage_setup_sid: "H01"
        sap_storage_setup_host_type: "hana_primary"
        sap_storage_setup_definition:
          - name: hana_data
            mountpoint: /hana/data
            disk_size: 150
            filesystem_type: xfs

          - name: hana_log
            mountpoint: /hana/log
            disk_size: 100
            filesystem_type: xfs

          - name: hana_shared
            mountpoint: /hana/shared
            disk_size: 200
            filesystem_type: xfs

          - name: software
            mountpoint: /software
            nfs_path: /software
            nfs_server: "fs-00000000000000000.efs.eu-central-1.amazonaws.com:/software"
            nfs_filesystem_type: "nfs4"
            nfs_mount_options: "vers=4.1,hard,timeo=600,retrans=2,acl"

          - name: swap
            disk_size: 96
            filesystem_type: swap
```
<!-- END Execution Example -->

<!-- BEGIN Role Tags -->
<!-- END Role Tags -->

<!-- BEGIN Further Information -->
<!-- END Further Information -->

## License
<!-- BEGIN License -->
Apache 2.0
<!-- END License -->

## Maintainers
<!-- BEGIN Maintainers -->
- [Janine Fuchs](https://github.com/ja9fuchs)
<!-- END Maintainers -->

## Role Input Parameters
All input parameters used by role are described in [INPUT_PARAMETERS.md](https://github.com/sap-linuxlab/community.sap_install/blob/main/roles/sap_storage_setup/INPUT_PARAMETERS.md)
