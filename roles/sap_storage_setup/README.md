# sap_storage_setup Ansible Role

Ansible Role for preparing a host with the storage requirements of an SAP System (prior to software installation)

## Scope

This Ansible Role provides:
- local/block storage volumes setup as LVM Logical Volumes, Filesystem formatting and mount to defined directory path
- remote/file storage mount (and subdirectories as required)
- swap file or swap partition

This Ansible Role has been tested for the following SAP software deployment types:
- SAP HANA Scale-up, Scale-out and Scale-up High Availability
- SAP NetWeaver AS in Sandbox (Two-Tier/OneHost), Standard (Three-Tier/DualHost), Distributed (Multi-Tier) and Distributed High Availability

This Ansible Role is agnostic, and will run on any Infrastructure Platform. Only LVM is used for local/block storage, to allow for further expansion if the SAP System requires further storage space in the future.

Please note, while this Ansible Role has protection against overwrite of existing disks and filesystems - sensibile review and care is required for any automation of disk storage. Please review the documentation and samples/examples carefully. It is strongly suggested to initially execute the Ansible Playbook calling this Ansible Role, with `ansible-playbook --check` for Check Mode - this will perform no changes to the host and show which changes would be made.

## Requirements

The Ansible Role requires the `community.general` Ansible Collection (uses the `lvg`, `lvol` and `filesystem` Ansible Modules).

Before using this Ansible Role, please make sure that the required collections are installed; for example, by using the command `ansible-galaxy install community.general`

## Prerequisites

All local/block storage volumes must be attached to the host, and all remote/file storage mounts must be available with host accessibility (e.g. port 2049).

## Variables and Parameters

The 3 critical variables are:
- `sap_storage_setup_definition` - a list with a dictionary for each mountpoint (e.g. /hana/data) for the host
- `sap_storage_setup_host_type` - a list which defines SAP Software on the host (e.g. list containing both hana_primary and nwas_abap_ascs values if creating a Sandbox Two-Tier/OneHost)
- `sap_storage_setup_sid` - a string with the SAP System ID of the logical system (e.g. D01)

## Execution Flow

The Ansible Role is sequential:
- Get host facts
- Create list of unused disk devices
- Match/Map unused disk devices to the `sap_storage_setup_definition`
- Create LVM Logical Volumes (and prerequisite LVM Volume Groups and LVM Physical Volumes)
- Create swap file or swap partition
- Mount NFS temporarily, create required subdirectories, unmount and mount subdictory on the NFS share

## Sample

Please see a full sample using multiple hosts to create an SAP S/4HANA Distributed deployment in the [/playbooks](../../playbooks/) directory of the Ansible Collection `sap_install`.

## License

Apache 2.0

## Author Information

Red Hat for SAP Community of Practice, Janine Fuchs, IBM Lab for SAP Solutions

---
<!-- BEGIN: Role Input Parameters -->
## Role Input Parameters

Minimum required parameters:

- [sap_storage_setup_definition](#sap_storage_setup_definition)
- [sap_storage_setup_host_type](#sap_storage_setup_host_type)
- [sap_storage_setup_sid](#sap_storage_setup_sid)


### sap_storage_setup_definition <sup>required</sup>

- _Type:_ `list`

Describes the filesystems to be configured.<br>

- **disk_size**<br>
    Size of the disk device that is used for the filesystem.<br>For filesystems with no LVM logical volume striping, this is the total size of the filesystem.<br>For filesystems with LVM LV striping defined (`lvm_lv_stripes`), this is the size of each disk. The resulting filesystem size will be `disk_size` multiplied by `lvm_lv_stripes` (=disks).
- **filesystem_type**<br>
    _Default:_ `xfs`<br>
    The type of filesystem that will be created on the logical volume.
- **lvm_lv_name**<br>
    The name of the LVM volume.<br>The default name is derived from the name value of the filesystem definition entry, for example 'lv_hanalog'.
- **lvm_lv_stripe_size**<br>
    When setting up a striped volume, the stripe size can be defined.<br>Example format - "128K".
- **lvm_lv_stripes**<br>
    _Default:_ `1`<br>
    Number of disks that will be configured in a striped volume.<br>This requires the availability of the same amount of unused disks, which must be of the size defined in `disk_size`.
- **lvm_vg_name**<br>
    The name of the LVM volume group.<br>The default name is derived from the name value of the filesystem definition entry, for example 'vg_hanalog'.
- **lvm_vg_physical_extent_size**<br>
    _Default:_ `4`<br>
    Adjustable size of the physical extents of the volume group in LVM.
- **mountpoint**<br>
    The path to where the filesystem will be mounted.<br>This can be left out for the definition of a swap volume.
- **name**<br>
    A name of the filesystem definition entry.<br>This name is used to generate volume group name and logical volume name.
- **nfs_filesystem_type**<br>
    _Default:_ `nfs4`<br>
    The type of the NFS filesystem, for example `nfs`, `nfs4`.
- **nfs_mount_options**<br>
    Mount options to use for the NFS mount.<br>Generic default is `hard,acl`.<br>Defaults depend on the specific platform detected by the role or defined explicitly.
- **nfs_path**<br>
    When defining an NFS filesystem, this is the directory path of the filesystem to be mounted.
- **nfs_server**<br>
    When defining an NFS filesystem, this is the address of the NFS server.<br>The address must contain the root path, in which the mount directories exist or will be created.<br>For example, `192.168.1.100:/`.
- **swap_path**<br>
    The path to the swap file.<br>When this option is defined for a swap filesystem definition, it will create a swap file on an existing filesytem.

Example:

```yaml
sap_storage_setup_definition:
- disk_size: 100G
  filesystem_type: xfs
  mountpoint: /hana/data
  name: hanadata
- disk_size: 100G
  filesystem_type: xfs
  mountpoint: /hana/log
  name: hanalog
```

### sap_storage_setup_host_type <sup>required</sup>


The type of service the target system is going to be configured for.<br>
This can be a list of multiple types which apply to a single host.<br>
If not defined, the default will be inherited from the global parameter `sap_host_type`. One of these parameters must be defined.<br>

### sap_storage_setup_sid <sup>required</sup>

- _Type:_ `str`

SID of the SAP service.<br>
If not defined, the default will be inherited from the global parameter `sap_system_sid`. One of these parameters must be defined.<br>

<!-- END: Role Input Parameters -->
