
## Input Parameters for sap_netweaver_preconfigure Ansible Role
<!-- BEGIN Role Input Parameters -->

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

<!-- END Role Input Parameters -->