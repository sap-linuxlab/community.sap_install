<!-- BEGIN Title -->
# sap_storage_setup Ansible Role
<!-- END Title -->
![Ansible Lint for sap_storage_setup](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_storage_setup.yml/badge.svg)

## Description
<!-- BEGIN Description -->
The Ansible Role `sap_storage_setup` is used to prepare a host with the storage requirements of an SAP System (prior to software installation).

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

Install required collection by `ansible-galaxy collection install community.general`.
<!-- END Dependencies -->

<!-- BEGIN Prerequisites -->
## Prerequisites
Managed nodes:

- All local/block storage volumes must be attached to the host.
- All remote/file storage mounts must be available with host accessibility (e.g. port 2049).
<!-- END Prerequisites -->

## Execution
<!-- BEGIN Execution -->
**:warning: Do not execute this Ansible Role against existing SAP systems unless you know what you are doing and you prepare inputs to avoid unintended changes caused by default inputs.**</br>

:warning: While this Ansible Role has protection against overwrite of existing disks and filesystems - sensible review and care is required for any automation of disk storage.</br>
Please review the documentation and samples/examples carefully. It is strongly suggested to initially execute the Ansible Playbook calling this Ansible Role,</br>
with `ansible-playbook --check` for Check Mode - this will perform no changes to the host and show which changes would be made.

**Considerations**

- This role does not permit static definition for mountpoint to use a specific device (e.g. `/dev/sdk`).<br>
  The definition will define the disk size to use for the mountpoint, and match accordingly.
- This role enforces that 1 mountpoint will use 1 LVM Logical Volume (LV) that consumes 100% of an LVM Volume Group (VG),<br>
  with the LVM Volume Group (VG) consuming 100% of `1..n` LVM Physical Volumes (PV).
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
## Further Information
For more examples on how to use this role in different installation scenarios, refer to the [ansible.playbooks_for_sap](https://github.com/sap-linuxlab/ansible.playbooks_for_sap) playbooks.
<!-- END Further Information -->

## License
<!-- BEGIN License -->
Apache 2.0
<!-- END License -->

## Maintainers
<!-- BEGIN Maintainers -->
- [Janine Fuchs](https://github.com/ja9fuchs)
<!-- END Maintainers -->

## Role Variables
<!-- BEGIN Role Variables -->

Minimum required parameters:

- [sap_storage_setup_definition](#sap_storage_setup_definition-required)
- [sap_storage_setup_host_type](#sap_storage_setup_host_type-required)
- [sap_storage_setup_sid](#sap_storage_setup_sid-required)


### sap_storage_setup_definition <sup>required</sup>

- _Type:_ `list`

Describes list of the filesystems to be configured.<br>

- **disk_size**<br>
    Size of the disk device that is used for the filesystem.<br>For filesystems with no LVM logical volume striping, this is the total size of the filesystem.<br>For filesystems with LVM LV striping defined (`lvm_lv_stripes`), this is the size of each disk. The resulting filesystem size will be `disk_size` multiplied by `lvm_lv_stripes` (=disks).

    - _Type:_ `int`

- **filesystem_type**<br>
    The type of filesystem that will be created on the logical volume.

    - _Type:_ `str`
    - _Default:_ `xfs`

- **lvm_lv_name**<br>
    The name of the LVM volume.<br>The default name is derived from the name value of the filesystem definition entry, for example 'lv_hanalog'.

    - _Type:_ `str`

- **lvm_lv_stripe_size**<br>
    When setting up a striped volume, the stripe size can be defined.<br>Example format - "128K".

    - _Type:_ `str`

- **lvm_lv_stripes**<br>
    Number of disks that will be configured in a striped volume.<br>This requires the availability of the same amount of unused disks, which must be of the size defined in `disk_size`.

    - _Type:_ `int`
     _Default:_ `1`

- **lvm_vg_name**<br>
    The name of the LVM volume group.<br>The default name is derived from the name value of the filesystem definition entry, for example 'vg_hanalog'.

    - _Type:_ `str`

- **lvm_vg_physical_extent_size**<br>
    Adjustable size of the physical extents of the volume group in LVM.

    - _Type:_ `int`
    - _Default:_ `4`

- **mountpoint**<br>
    The path to where the filesystem will be mounted.<br>This can be left out for the definition of a swap volume.

    - _Type:_ `str`

- **name**<br>
    A name of the filesystem definition entry.<br>This name is used to generate volume group name and logical volume name.

    - _Type:_ `str`

- **nfs_filesystem_type**<br>
    The type of the NFS filesystem, for example `nfs`, `nfs4`.

    - _Type:_ `str`
    - _Default:_ `nfs4`

- **nfs_mount_options**<br>
    Mount options to use for the NFS mount.<br>Generic default is `hard,acl`.<br>Defaults depend on the specific platform detected by the role or defined explicitly.

    - _Type:_ `str`
    - _Default:_ `hard,acl`

- **nfs_path**<br>
    When defining an NFS filesystem, this is the directory path of the filesystem to be mounted.

    - _Type:_ `str`

- **nfs_server**<br>
    When defining an NFS filesystem, this is the address of the NFS server.<br>The address must contain the root path, in which the mount directories exist or will be created.<br>For example, `192.168.1.100:/`.

    - _Type:_ `str`

- **swap_path**<br>
    The path to the swap file.<br>When this option is defined for a swap filesystem definition, it will create a swap file on an existing filesystem.

    - _Type:_ `str`

Example:

```yaml
sap_storage_setup_definition:

  # Block Storage volume
  - name: hana_data                # required: string, filesystem name used to generate lvm_lv_name and lvm_vg_name
    mountpoint: /hana/data         # required: string, directory path where the filesystem is mounted
    disk_size: 100                 # required: integer, size in GB
    filesystem_type: xfs           # optional: string, value 'xfs'. Use 'swap' to create swap filesystem

  # File Storage volume
  - name: hana_shared              # required: string, reference name
    mountpoint: /hana/shared       # required: string, directory path where the filesystem is mounted
    nfs_server: nfs.corp:/         # required: string, server and parent directory of the NFS Server; value default from var sap_storage_setup_nfs_server

  # Swap as file instead of Block Storage volume
  # See SAP Note 1597355 - Swap-space recommendation for Linux
  - name: swap                     # required: string, reference name
    swap_path: /swapfile           # required: string, directory path where swap file is created
    disk_size: 4                   # required: integer, size in GB of swap file
    filesystem_type: swap          # required: string, must be value 'swap'
```

### sap_storage_setup_host_type <sup>required</sup>

- _Type:_ `list`

The type of service the target system is going to be configured for.<br>
This can be a list of multiple types which apply to a single host.<br>
If not defined, the default will be inherited from the global parameter `sap_host_type`. One of these parameters must be defined.<br>
Available values: `hana_primary`, `hana_secondary`, `nwas_abap_ascs`, `nwas_abap_ers`, `nwas_abap_pas`, `nwas_abap_aas`, `nwas_java_scs`, `nwas_java_ers`

### sap_storage_setup_multipath_enable_and_detect

- _Type:_ `bool`
- _Default:_ `False`

Define if multipathing should be enabled and dynamic multipath devices detected and used for the filesystem setup.<br>

### sap_storage_setup_sid <sup>required</sup>

- _Type:_ `str`

SID of the SAP service.<br>
If not defined, the default will be inherited from the global parameter `sap_system_sid`. One of these parameters must be defined.<br>
<!-- END Role Variables -->
