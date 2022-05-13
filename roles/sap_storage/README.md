# sap_storage Ansible Role

Ansible role for preparing the storage requirements of an SAP system prior to installation
- physical volumes
- volume groups
- logical volumes
- filesystems

This can be used in 2 days
- `generic`     - using direct input of required directories, filesystems, physical volumes, volume groups, logical volumes, etc
- `cloud type`  - by providing a cloud type, the role will determine the physical volumes by reading the VM meta data

## Overview

### Execution

- Sample execution:

    ```bash
    ansible-playbook --connection=local --limit localhost -i "localhost," sap-storage.yml -e "@input_file.yml"
    ```

### Variables


| **Variable**                                  | **Info**                                  | **Default** | **Required** |
| :---                                          | :---                                      | :---        | :---         |
| sap_storage_cloud_type                        | 'generic' / 'az' / 'aws'                  | 'generic'   | yes          |
| sap_storage_action                            | 'prepare' / 'remove'                      | 'prepare'   | yes          |

### Input

- Sample input:

    ```yaml
    sap_storage_dict:
    hanadata:
        name: 'hanadata'
        directory: '/hana/data'
        vg: 'hanadatavg'
        lv: 'hanadatalv'
        pv: ["/dev/sdb"]
        numluns: '1'
        stripesize: ''
    hanalog:
        name: 'hanalog'
        directory: '/hana/log'
        vg: 'hanalogvg'
        lv: 'hanaloglv'
        pv: ["/dev/sdc", "/dev/sdd"]
        numluns: '2'
        stripesize: '32'
    hanashared:
        name: 'hanashared'
        directory: '/hana/shared'
        vg: 'hanasharedvg'
        lv: 'hanasharedlv'
        pv: ["/dev/sde"]
        numluns: '1'
        stripesize: ''
    usrsap:
        name: 'usrsap'
        directory: '/usr/sap'
        vg: 'usrsapvg'
        lv: 'usrsaplv'
        pv: ["/dev/sdf"]
        numluns: '1'
        stripesize: ''
    sapmnt:
        name: 'sapmnt'
        directory: '/sapmnt'
        vg: 'sapmntvg'
        lv: 'sapmntlv'
        pv: ["/dev/sdg"]
        numluns: '1'
        stripesize: ''
    ```

## Prerequisites

Disks have been attached to the VM and have the appropriate labels (hanadat, hanashared etc)

## License

Apache license 2.0

## Author Information

IBM Lab for SAP Solutions, Red Hat for SAP Community of Practice
