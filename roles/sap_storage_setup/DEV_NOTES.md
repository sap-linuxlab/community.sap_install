# Collection of development notes

Notes about open items, cloud platforms and unused code, which are not relevant for the users of the role.

> **NOTE:** All the code in this file will have to be improved in terms of fully qualified module names, structure, fact and register names, before being reused in future.

## Open items

### Permissions and ownership of the mount point
The role creates every mount point with the default permissions of the `mount` module and does not
change the owner. A filesystem that is handed over to an SAP installation usually needs a specific
owner, group and mode, for example `sapsys` on `/usr/sap`.

Implementing it requires new keys in `sap_storage_setup_definition`, for example `owner`, `group`
and `mode`, together with their argument spec entries, validation and README documentation.
Marked as TODO in `tasks/configuration/configure_lvg_lvm.yml`.

### Logical volume that exists, but is not mounted
Block disk entries are skipped by comparing the key `mountpoint` against the mounted paths. An entry
whose logical volume exists, but is not mounted at the moment, is therefore not skipped and enters
the device mapping stage. It cannot claim a disk, because the disks of the existing volume carry a
physical volume signature and are excluded from the unused disks, so the entry ends in the warning
about definitions without an unused device. The result is correct, but the reported reason is not.

Comparing the volume group and logical volume name against the output of `lvs` would report it
accurately, the same way the swap disks are compared using the `stat` module.

## Cloud platforms

Cloud platforms will need to be considered if they are implemented as additive workflow to existing, or completely separate.

### AWS
No code was implemented, only few variables were staged.

#### Variables
```yaml
sap_storage_setup_aws_nfs_options: 'nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport,acl'
sap_storage_setup_aws_imds_url:
sap_storage_setup_aws_vmsize_url:
sap_storage_setup_aws_vmsize:
```

### Azure
Code was commented out without being transformed into native Ansible code. Moved here as notes for future developments.

#### Variables
```yaml
sap_storage_setup_az_imds_json:
sap_storage_setup_az_imds_url: 'http://169.254.169.254/metadata/instance/compute?api-version=2020-09-01'
sap_storage_setup_az_vmsize_url: 'http://169.254.169.254/metadata/instance/compute/vmSize?api-version=2017-08-01&format=text'
sap_storage_setup_az_vmsize:
sap_storage_setup_az_lun: '/dev/disk/azure/scsi1/lun'
```

#### Pre-tasks
```yaml
# Striped volume
- name: SAP Storage Preparation - {{ sap_storage_setup_cloud_type | upper }} - {{ sap_storage_setup_az_vmsize }} - {{ item.value.name }} - Striped
 block:

   # Get LUNs from metadata
   - name: SAP Storage Preparation - {{ sap_storage_setup_cloud_type | upper }} - {{ sap_storage_setup_az_vmsize }} - {{ item.value.name }} Get LUNs from metadata
     shell: |
       for i in {1..{{ item.value.numluns }}}
       do
         {{ item.value.vg }}${i}lun="{{ sap_storage_setup_az_lun }} \
           `awk '/caching/ { r=""; f=1 } f { r = (r ? r ORS : "") $0 } \
           /writeAcceleratorEnabled/ \
           { if (f && r ~ /{{ item.value.name }}${i}/) print r; f=0 }' \
           {{ sap_storage_setup_az_imds_json }} \
           | grep lun | sed 's/[^0-9]*//g'`"
         echo ${{ item.value.vg }}${i}lun
       done
     args:
       executable: /bin/bash
     register: pvs_reg

   - set_fact:
       pvs_list: "{{ pvs_reg.stdout.split() }}"

   # Create Volume Group
   - name: SAP Storage Preparation - {{ sap_storage_setup_cloud_type | upper }} - {{ sap_storage_setup_az_vmsize }} - {{ item.value.name }} Volume Group Striped
     lvg:
       vg: "{{ item.value.vg }}"
       pvs: "{{ pvs_list | join(',') }}"
       force: yes

   # Create Logical Group
   - name: SAP Storage Preparation - {{ sap_storage_setup_cloud_type | upper }} - {{ sap_storage_setup_az_vmsize }} - {{ item.value.name }} Logical Volume - Striped
     lvol:
       vg: "{{ item.value.vg }}"
       lv: "{{ item.value.lv }}"
       size: 100%VG
       opts: "-i{{ item.value.numluns }} -I{{ item.value.stripesize }}"

 when:
   - "item.value.numluns != '1'"

# Single volume
- name: SAP Storage Preparation - {{ sap_storage_setup_cloud_type | upper }} - {{ sap_storage_setup_az_vmsize }} - {{ item.value.name }} - Single Volume
 block:

   # Get LUNs from metadata
   - name: SAP Storage Preparation - {{ sap_storage_setup_cloud_type | upper }} - {{ sap_storage_setup_az_vmsize }} - {{ item.value.name }} Get LUNs from metadata
     shell: |
       {{ item.value.vg }}lun="{{ sap_storage_setup_az_lun }} \
         `awk '/caching/ { r=""; f=1 } f { r = (r ? r ORS : "") $0 } \
         /writeAcceleratorEnabled/ \
         { if (f && r ~ /{{ item.value.name }}/) print r; f=0 }' \
         {{ sap_storage_setup_az_imds_json }} \
         | grep lun | sed 's/[^0-9]*//g'`"
       echo ${{ item.value.vg }}lun
     args:
       executable: /bin/bash
     register: pvs_reg

   - set_fact:
       pvs_one: "{{ pvs_reg.stdout }}"

   # Create Volume Group
   - name: SAP Storage Preparation - {{ sap_storage_setup_cloud_type | upper }} - {{ sap_storage_setup_az_vmsize }} - {{ item.value.name }} Volume Group One
     lvg:
       vg: "{{ item.value.vg }}"
       pvs: "{{ pvs_one }}"
       force: yes

   # Create Logical Group
   - name: SAP Storage Preparation - {{ sap_storage_setup_cloud_type | upper }} - {{ sap_storage_setup_az_vmsize }} - {{ item.value.name }} Logical Volume - One
     lvol:
       vg: "{{ item.value.vg }}"
       lv: "{{ item.value.lv }}"
       size: 100%VG

 when:
   - "item.value.numluns == '1'"

# Create Filesystem
- name: SAP Storage Preparation - {{ sap_storage_setup_cloud_type | upper }} - {{ sap_storage_setup_az_vmsize }} - {{ item.value.name }} Filesystem
 filesystem:
   fstype: xfs
   dev: "/dev/{{ item.value.vg }}/{{ item.value.lv }}"

# Mount Filesystem
- name: SAP Storage Preparation - {{ sap_storage_setup_cloud_type | upper }} - {{ sap_storage_setup_az_vmsize }} - {{ item.value.name }} Mount
 mount:
   path: "{{ item.value.directory }}"
   fstype: xfs
   src: "/dev/mapper/{{ item.value.vg }}-{{ item.value.lv }}"
   state: mounted
```

#### Configuration
```yaml
# Create json format of IMDS
- name: SAP Storage Preparation - {{ sap_storage_setup_cloud_type | upper }} - Create json format of IMDS
 shell: |
   curl -H Metadata:true --noproxy "*" "{{ sap_storage_setup_az_imds_url }}" | python3 -mjson.tool
 register: az_imds_reg
 args:
    executable: /bin/bash
# If this fails, that means this VM is not Azure?

- set_fact:
   sap_storage_setup_az_imds_json: "{{ az_imds_reg.stdout }}"

# Pull VMSize
- name: SAP Storage Preparation - {{ sap_storage_setup_cloud_type | upper }} - Pull VMSize
 shell: |
   curl -H Metadata:true --noproxy "*" "{{ sap_storage_setup_az_vmsize_url }}"
 register: az_vmsize_reg
 args:
    executable: /bin/bash

- debug:
   msg:
     - "{{ az_vmsize_reg.stdout }}"

- set_fact:
   sap_storage_setup_az_vmsize: "{{ az_vmsize_reg.stdout }}"

# Include vars depending on VM Size
- name: SAP Storage Preparation - {{ sap_storage_setup_cloud_type | upper }} - Load Variables for {{ sap_storage_setup_az_vmsize }}
 include_vars: "{{ sap_storage_setup_cloud_type }}_tasks/vmsizes/{{ sap_storage_setup_az_vmsize }}.yml"
```

#### Post-tasks
```yaml
# Unmount Filesystem
- name: SAP Storage Preparation - {{ sap_storage_setup_cloud_type | upper }} - {{ item.value.name }} Unmount Filesystem
 mount:
   path: "{{ item.value.directory }}"
   state: absent

# Remove Filesystem
- name: SAP Storage Preparation - {{ sap_storage_setup_cloud_type | upper }} - {{ item.value.name }} Remove Filesystem
 shell: |
   /sbin/wipefs --all -f /dev/mapper/{{ item.value.vg }}-{{ item.value.lv }}

# Remove Logical Volume
- name: SAP Storage Preparation - {{ sap_storage_setup_cloud_type | upper }} - {{ item.value.name }} Remove Logical Volume
 lvol:
   lv: "{{ item.value.lv }}"
   vg: "{{ item.value.vg }}"
   state: absent
   force: yes

# Remove Volume Group
- name: SAP Storage Preparation - {{ sap_storage_setup_cloud_type | upper }} - {{ item.value.name }} Remove Volume Group
 lvg:
   vg: "{{ item.value.vg }}"
   state: absent
   force: yes
```


## Remove Storage
Following code was commented out in `generic_tasks/remove_storage.yml`.

```yaml
# Unmount Filesystem
- name: SAP Storage Preparation - {{ sap_storage_setup_cloud_type | upper }} - {{ item.value.name }} Unmount Filesystem
 mount:
   path: "{{ item.value.directory }}"
   state: absent

# INFO:
# this only works right using community Ansible Galaxy filesystem module
# only interested with native Ansible modules for now
# - name: SAP Storage Preparation - {{ sap_storage_setup_cloud_type | upper }} - {{ item.value.name }} Filesystem
#   filesystem:
#     dev: "/dev/mapper/{{ item.value.vg }}/{{ item.value.lv }}"
#     state: absent

# Remove Filesystem
- name: SAP Storage Preparation - {{ sap_storage_setup_cloud_type | upper }} - {{ item.value.name }} Remove Filesystem
 shell: |
   /sbin/wipefs --all -f /dev/mapper/{{ item.value.vg }}-{{ item.value.lv }}
 ignore_errors: yes

# Remove Logical Volume
- name: SAP Storage Preparation - {{ sap_storage_setup_cloud_type | upper }} - {{ item.value.name }} Remove Logical Volume
 lvol:
   lv: "{{ item.value.lv }}"
   vg: "{{ item.value.vg }}"
   state: absent
   force: yes

# Remove Volume Group
- name: SAP Storage Preparation - {{ sap_storage_setup_cloud_type | upper }} - {{ item.value.name }} Remove Volume Group
 lvg:
   vg: "{{ item.value.vg }}"
   state: absent
   force: yes

```
