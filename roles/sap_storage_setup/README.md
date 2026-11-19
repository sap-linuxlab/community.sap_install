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
- SWAP file or SWAP disk

This Ansible Role is agnostic, and will run on any Infrastructure Platform. Only LVM is used for local/block storage, to allow for further expansion if the SAP System requires further storage space in the future.
<!-- END Description -->

<!-- BEGIN Dependencies -->
## Dependencies
- `community.general`
    - Modules:
        - `lvg`
        - `lvol`
        - `filesystem`

- `ansible.posix`
    - Modules:
        - `mount`

Install required collection by executing:

```bash
ansible-galaxy collection install community.general
ansible-galaxy collection install ansible.posix
```
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

**Storage definition scenarios**

Each entry of `sap_storage_setup_definition` is configured as one of four scenarios, which are
selected by the keys that the entry defines.<br>The scenarios are evaluated in the order below and
the first match is used.

| Scenario   | `filesystem_type` | `disk_size` | `mountpoint` | `nfs_server`   | `nfs_path`    | `swap_path` |
| ---------- | ----------------- | ----------- | ------------ | -------------- | ------------- | ----------- |
| NFS mount  | not used          | -           | required     | required       | required      | -           |
| Swap file  | `swap`            | required    | not used     | -              | -             | required    |
| Swap disk  | `swap`            | required    | not used     | -              | -             | -           |
| Block disk | any except `swap` | required    | required     | -              | -             | -           |

> **NOTE for all**:
> - Value `-` marks a key that must not be defined.
> - An entry that matches no scenario fails the validation with a message naming the entry and the keys above.

> **NOTE for NFS**:
> - Key `nfs_server` is optional if the role variable `sap_storage_setup_nfs_server` is defined.
> - Key `nfs_path` accepts empty string to mount the path of `nfs_server` as it is, without creating a subdirectory.

<!-- END Execution -->

<!-- BEGIN Execution Recommended -->
<!-- END Execution Recommended -->

### Execution Flow
<!-- BEGIN Execution Flow -->
1. Gather facts about hosts.
2. Validate `sap_storage_setup_definition` and classify each entry as NFS mount, swap file, swap disk or block disk.
3. Skip entries that are already configured.
4. Detect multipath devices, if `sap_storage_setup_multipath_enable_and_detect` is enabled.
5. Create list of unused disk devices.
6. Match/Map unused disk devices to the block disk and swap disk entries, by exact size first and by approximate size second.
7. Create LVM Logical Volumes (and prerequisite LVM Volume Groups and LVM Physical Volumes), then format and mount them.
8. Enable swap disks.
9. Create and enable swap files.
10. Mount NFS temporarily, create required subdirectories, unmount and mount subdirectory on the NFS share.
<!-- END Execution Flow -->

<!-- BEGIN Execution Example -->
Example playbook to configure storage for SAP S/4HANA OneHost scenario on AWS platform that includes:

- 4 disks for `/hana/data`, `/hana/log`, `/hana/shared` and `/usr/sap`
- Remote filesystem for `/sapmnt` using directory `/sapmnt` on NFS server.
- Remote filesystem for `/software` using the path of the NFS server as it is.
- SWAP disk
- SWAP file
```yaml
---
- name: Ansible Play for SAP S/4HANA OneHost storage setup
  hosts: s01hana
  become: true
  tasks:
    - name: Execute Ansible Role sap_storage_setup
      ansible.builtin.include_role:
        name: community.sap_install.sap_storage_setup
      vars:
        sap_storage_setup_sid: "S01"
        sap_storage_setup_host_type:
          - hana_primary
          - nwas_abap_ascs
          - nwas_abap_pas

        sap_storage_setup_nwas_abap_ascs_instance_nr: '00'
        sap_storage_setup_nwas_abap_pas_instance_nr: '01'

        sap_storage_setup_definition:
          - name: hana_data
            mountpoint: /hana/data
            disk_size: 384
            filesystem_type: xfs

          - name: hana_log
            mountpoint: /hana/log
            disk_size: 128
            filesystem_type: xfs

          - name: hana_shared
            mountpoint: /hana/shared
            disk_size: 320
            filesystem_type: xfs

          - name: usr_sap
            mountpoint: /usr/sap
            disk_size: 128
            filesystem_type: xfs

          - name: sapmnt
            mountpoint: /sapmnt
            nfs_path: /sapmnt
            nfs_server: "fs-00000000000000000.efs.eu-central-1.amazonaws.com:/"
            nfs_filesystem_type: nfs4
            nfs_mount_options: "vers=4.1,hard,timeo=600,retrans=2,acl"

          - name: software
            mountpoint: /software
            nfs_path: ''
            nfs_server: "fs-00000000000000001.efs.eu-central-1.amazonaws.com:/sap_s4hana_2025"
            nfs_filesystem_type: nfs4
            nfs_mount_options: "vers=4.1,hard,timeo=600,retrans=2,acl"

          - name: swap_disk
            disk_size: 96
            filesystem_type: swap

          - name: swap_file
            filesystem_type: swap
            disk_size: 20
            swap_path: /swapfile1
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
- [Marcel Mamula](https://github.com/marcelmamula)
<!-- END Maintainers -->

## Role Variables
<!-- BEGIN Role Variables -->

### sap_storage_setup_definition <sup>required</sup>

- _Type:_ `list` of type `dictionary`

Describes list of the filesystems to be configured.<br>

- **disk_size**<br>
    Size of the disk device that is used for the filesystem.<br>
    For filesystems with no LVM logical volume striping, this is the total size of the filesystem.<br>
    For filesystems with LVM LV striping defined (`lvm_lv_stripes`), this is the size of each disk.
    The resulting filesystem size will be `disk_size` multiplied by `lvm_lv_stripes` (=disks).<br>
    An integer is handled as size in GB, a string can carry the unit suffix `G` or `T`, for example `100G`.<br>
    A disk is matched when its size is equal to this value, or within a range of 8 GB around it.

    - _Type:_ `raw`

- **filesystem_type**<br>
    The type of filesystem that will be created on the logical volume.<br>
    The role variable `sap_storage_setup_local_filesystem_type` is used when this key is not defined.

    - _Type:_ `str`
    - _Default:_ `xfs`

- **lvm_lv_name**<br>
    The name of the LVM volume.<br>
    The default name is derived from the name value of the filesystem definition entry, for example `lv_hanalog`.

    - _Type:_ `str`

- **lvm_lv_stripe_size**<br>
    When setting up a striped volume, the stripe size can be defined.<br>
    Example format - `128K`.

    - _Type:_ `str`

- **lvm_lv_stripes**<br>
    Number of disks that will be configured in a striped volume.<br>
    This requires the availability of the same amount of unused disks, which must be of the size defined in `disk_size`.<br>
    The role fails if fewer unused disks are found.<br>
    The role will warn if a striped volume already exists, but with different number of stripes.

    - _Type:_ `int`
    - _Default:_ `1`

- **lvm_pv_options**<br>
    Free-form options that are passed to the `pvcreate` command of the physical volume.

    - _Type:_ `str`

- **lvm_vg_name**<br>
    The name of the LVM volume group.<br>
    The default name is derived from the name value of the filesystem definition entry, for example `vg_hanalog`.

    - _Type:_ `str`

- **lvm_vg_options**<br>
    Free-form options that are passed to the `vgcreate` command of the volume group.

    - _Type:_ `str`

- **lvm_vg_physical_extent_size**<br>
    Adjustable size of the physical extents of the volume group in LVM.<br>
    Can be optionally suffixed by a unit (`k`/`K`/`m`/`M`/`g`/`G`), the default unit is megabyte `M`.

    - _Type:_ `str`
    - _Default:_ `4`

- **mountpoint**<br>
    The path to where the filesystem will be mounted.<br>
    Required for block disks and NFS mounts, and not used for swap.<br>
    The path must be absolute and must not contain whitespace.

    - _Type:_ `str`

- **name**<br>
    A unique name of the filesystem definition entry.<br>
    This name is used to generate volume group name and logical volume name, when `lvm_vg_name` or `lvm_lv_name` are not defined.<br>
    Allowed characters are letters, digits, `+`, `_`, `.` and `-`, and the name must not start with `-`.

    - _Type:_ `str`

- **nfs_filesystem_type**<br>
    The type of the NFS filesystem, for example `nfs`, `nfs4`.<br>
    The role variable `sap_storage_setup_nfs_filesystem_type` is used when this key is not defined.

    - _Type:_ `str`
    - _Default:_ `nfs4`

- **nfs_mount_options**<br>
    Mount options to use for the NFS mount.<br>
    The role variable `sap_storage_setup_nfs_mount_options` is used when this key is not defined.

    - _Type:_ `str`
    - _Default:_ `defaults`

- **nfs_path**<br>
    When defining an NFS filesystem, this is the directory path of the filesystem to be mounted.<br>
    The path is relative to the root path of `nfs_server` and is created on the NFS server if it does not exist.<br>
    An empty string mounts the path of `nfs_server` as it is, without creating a subdirectory.

    - _Type:_ `str`

- **nfs_server**<br>
    When defining an NFS filesystem, this is the address of the NFS server.<br>
    The address must contain the root path, in which the mount directories exist or will be created.<br>
    For example, `192.168.1.100:/`.<br>
    The role variable `sap_storage_setup_nfs_server` is used when this key is not defined.

    - _Type:_ `str`

- **swap_path**<br>
    The path to the swap file.<br>
    When this option is defined for a swap filesystem definition, it will create a swap file on an existing filesystem.<br>
    The path must be absolute and must not contain whitespace, and the directory that contains it must already exist.

    - _Type:_ `str`

Example:

```yaml
sap_storage_setup_definition:

  # Block Storage volume
  - name: hana_data
    mountpoint: /hana/data
    disk_size: 100
    filesystem_type: xfs

  # File Storage volume
  - name: hana_shared
    mountpoint: /hana/shared
    nfs_server: nfs.corp:/
    nfs_path: /hana_shared

  # Swap as Block Storage volume
  - name: swap_disk
    disk_size: 4
    filesystem_type: swap

  # Swap as file instead of Block Storage volume
  # See SAP Note 1597355 - Swap-space recommendation for Linux
  - name: swap_file
    swap_path: /swapfile
    disk_size: 4
    filesystem_type: swap
```

### sap_storage_setup_multipath_enable_and_detect

- _Type:_ `bool`
- _Default:_ `False`

**(Block Storage Specific)**<br>
Define if multipathing should be enabled and dynamic multipath devices detected and used for the filesystem setup.<br>

### sap_storage_setup_local_filesystem_type

- _Type:_ `str`
- _Default:_ `xfs`

**(Block Storage Specific)**<br>
The filesystem type used for block storage volumes.<br>
Applies to every definition entry that does not define its own `filesystem_type` key.

### sap_storage_setup_sid

- _Type:_ `str`
- _Default:_ `''`

**(NFS Mount Specific)**<br>
SID of the SAP instance, as a string of 3 characters.<br>
The value is converted to uppercase, so `s01` and `S01` create the same directories.<br>
This variable is used for NFS mounts only, where it is the first path element of the `/usr/sap`
subdirectories that are created on the NFS server. A definition without NFS mounts does not need it.<br>

### sap_storage_setup_host_type

- _Type:_ `list` or `str`
- _Default:_ `''`

**(NFS Mount Specific)**<br>
The type of service the target system is going to be configured for, when NFS mounts are used.<br>
This can be a list of multiple types which apply to a single host.<br>

Together with `sap_storage_setup_sid`, it selects the subdirectories that are created below `/usr/sap/<SID>/` on the NFS server, and it has no effect on
block disks or swap.<br>
A definition without NFS mounts does not need it.<br>
An unsupported value fails the validation, it is not ignored.

| Value              | Directory created below `/usr/sap/<SID>/`            |
| ------------------ | ---------------------------------------------------- |
| `hana_primary`     | none                                                 |
| `hana_secondary`   | none                                                 |
| `nwas_abap_ascs`   | `ASCS<nr>`                                           |
| `nwas_java_scs`    | `SCS<nr>`                                            |
| `nwas_ers`         | `ERS<nr>`                                            |
| `nwas_abap_ers`    | `ERS<nr>`, obsolete, kept for backward compatibility |
| `nwas_java_ers`    | `ERS<nr>`, obsolete, kept for backward compatibility |
| `nwas_abap_pas`    | `D<nr>`                                              |
| `nwas_abap_aas`    | `D<nr>`                                              |
| `nwas_java_ci`     | `J<nr>`                                              |
| `nwas_webdisp`     | `W<nr>`                                              |

The directory `<SID>/SYS` is created for every host type.<br>
`<nr>` is taken from the matching instance number variable, see
[sap_storage_setup_*_instance_nr](#sap_storage_setup__instance_nr).

### sap_storage_setup_*_instance_nr

- _Type:_ `str`
- _Default:_ `''`

**(NFS Mount Specific)**<br>
Instance number of an SAP instance, used to complete the `/usr/sap/<SID>/` subdirectory name of the
matching host type. One variable exists per host type that creates a subdirectory:

| Variable                                       | Host type          | Directory  |
| ---------------------------------------------- | ------------------ | ---------- |
| `sap_storage_setup_nwas_abap_ascs_instance_nr` | `nwas_abap_ascs`   | `ASCS<nr>` |
| `sap_storage_setup_nwas_java_scs_instance_nr`  | `nwas_java_scs`    | `SCS<nr>`  |
| `sap_storage_setup_nwas_ers_instance_nr`       | `nwas_ers`         | `ERS<nr>`  |
| `sap_storage_setup_nwas_abap_ers_instance_nr`  | `nwas_abap_ers`    | `ERS<nr>`  |
| `sap_storage_setup_nwas_java_ers_instance_nr`  | `nwas_java_ers`    | `ERS<nr>`  |
| `sap_storage_setup_nwas_abap_pas_instance_nr`  | `nwas_abap_pas`    | `D<nr>`    |
| `sap_storage_setup_nwas_abap_aas_instance_nr`  | `nwas_abap_aas`    | `D<nr>`    |
| `sap_storage_setup_nwas_java_ci_instance_nr`   | `nwas_java_ci`     | `J<nr>`    |
| `sap_storage_setup_nwas_webdisp_instance_nr`   | `nwas_webdisp`     | `W<nr>`    |

The value must be a quoted string of exactly two digits, for example `'01'`.<br>
Only the variables of the host types listed in `sap_storage_setup_host_type` are required, and only
when the definition contains NFS mounts.

### sap_storage_setup_nfs_server

- _Type:_ `str`

**(NFS Mount Specific)**<br>
The address of the NFS server, including the root path in which the mount directories exist or
will be created, for example `192.168.1.100:/`.<br>
Applies to every NFS entry that does not define its own `nfs_server` key.<br>
This variable has no default and is undefined by default, which requires the `nfs_server` key on
every NFS entry.

### sap_storage_setup_nfs_filesystem_type

- _Type:_ `str`
- _Default:_ `nfs4`

**(NFS Mount Specific)**<br>
The NFS protocol used for NFS mounts, for example `nfs` or `nfs4`.<br>
Applies to every NFS entry that does not define its own `nfs_filesystem_type` key.

### sap_storage_setup_nfs_mount_options

- _Type:_ `str`
- _Default:_ `defaults`

**(NFS Mount Specific)**<br>
The mount options used for NFS mounts.<br>
Applies to every NFS entry that does not define its own `nfs_mount_options` key.
<!-- END Role Variables -->
