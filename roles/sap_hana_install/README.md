# sap_hana_install Ansible Role

Ansible role for SAP HANA Installation

## Prerequisites

### Configure your system for the installation of SAP HANA

- Make sure required volumes and filesystems are configured in the host.
You can use the role `sap_storage` to configure this. More info [here](/roles/sap_storage)

- Run the roles `sap_general_preconfigure` and `sap_hana_preconfigure` for installing required packages and
for configuring system settings.

### SAP HANA Software Installation .SAR Files

Place the following files in directory /software/hana or in any other directory specified by variable
`sap_hana_install_software_directory`:

1. The SAPCAR executable for the correct hardware architecture

2. The SAP HANA Installation .SAR file
    - SAP HANA 2.0 Server - `IMDB_SERVER*.SAR` file

3. Optional - SAP HANA Components .SAR files
    - Include other optional components such as `IMDB_AFL*.SAR` or `IMDB_LCAPPS*.SAR`

4. Optional - SAP Host Agent .SAR file
    - Include other optional components such as `SAPHOSTAGENT*SAR`

#### Sample Directory Contents - with .SAR files

- Sample directory `sap_hana_install_software_directory` containing SAP HANA software installation files
    ```console
    [root@hanahost SAP_HANA_INSTALLATION]# ll -lrt
    -rwxr-xr-x. 1 nobody nobody  149561376 Mar  4  2021 IMDB_AFL20_054_1-80001894.SAR
    -rwxr-xr-x. 1 nobody nobody  211762405 Mar  4  2021 IMDB_CLIENT20_007_23-80002082.SAR
    -rwxr-xr-x. 1 nobody nobody    4483040 Mar  4  2021 SAPCAR_1010-70006178.EXE
    -rwxr-xr-x. 1 nobody nobody  109492976 Mar  4  2021 IMDB_LCAPPS_2054_0-20010426.SAR
    -rwxr-xr-x. 1 nobody nobody  109752805 Mar  4  2021 VCH202000_2054_0-80005463.SAR
    -rwxr-xr-x. 1 nobody nobody 3694683699 Mar  4  2021 IMDB_SERVER20_054_0-80002031.SAR
    -rwxr-xr-x. 1 nobody nobody   89285401 Sep 30 04:24 SAPHOSTAGENT51_51-20009394.SAR
    ```

If more than one SAPCAR EXE file is present in the software directory, the role will select the latest version
for the current hardware architecture. Alternatively, the file name of the SAPCAR EXE file can also be set with
variable `sap_hana_install_sapcar_filename`.

If more than one SAR file for a certain software product is present in the software directory, the automatic
handling of such SAR files will fail after extraction, when moving the newly created product directories
(like `SAP_HOST_AGENT`) to already existing destinations.
For avoiding such situations, use following variable to provide a list of SAR files to extract:
`sap_hana_install_sarfiles_list`.

Example:
```
sap_hana_install_sarfiles_list:
  - SAPHOSTAGENT54_54-80004822.SAR
  - IMDB_SERVER20_060_0-80002031.SAR
```

#### Extracted SAP HANA Software Installation Files

This role will detect if there is a file `hdblcm` already present in the directory specified by variable
`sap_hana_install_software_extract_directory` or in any directory below. If If found, it will skip
the .SAR extraction phase and proceed with the installation.

The default for `sap_hana_install_software_extract_directory` is `{{ sap_hana_install_software_directory }}/extracted` but it
can be set to a different directory.

If this role is executed on more than one host in parallel and the software extraction directory is shared among those hosts,
the role will only extract the files on the first host on which the extraction has started. The role will proceed on the other hosts
after the extraction of SAR files has completed.

- Sample directory `sap_hana_install_software_extract_directory` containing extracted SAP HANA software installation files
    ```console
    [root@hanahost extracted]# ll -lrt
    drwxr-xr-x 4 root root 4096 Sep 30 04:55 SAP_HANA_AFL
    drwxr-xr-x 5 root root 4096 Sep 30 04:55 SAP_HANA_CLIENT
    drwxr-xr-x 4 root root 4096 Sep 30 04:55 SAP_HANA_LCAPPS
    drwxr-xr-x 8 root root 4096 Sep 30 04:57 SAP_HANA_DATABASE
    drwxr-xr-x 2 root root 4096 Sep 30 04:58 SAP_HOST_AGENT
    drwxr-xr-x 4 root root 4096 Sep 30 04:58 VCH_AFL_2020
    ```

## Further Variables and Parameters

### Input Parameters

If the variable `sap_hana_install_check_sidadm_user` is set to `no`, the role will install SAP HANA even
if there the sidadm user exists. Default is `yes`, in which case the installation will not be performed if the
sidadm user is contained in the user database.

The variable `sap_hana_install_new_system` determines if the role will perform a fresh SAP HANA installation or
if it will add further hosts to an existing SAP HANA system as specified by variable
`sap_hana_install_addhosts`. Default is `yes` for a fresh SAP HANA installation.

### Default Parameters

Please check the default parameters file for more information on other parameters that can be used as an input
- [**sap_hana_install** default parameters](defaults/main.yml)

## Execution

Sample Ansible Playbook Execution

- Local Host Installation
    - `ansible-playbook --connection=local --limit localhost -i "localhost," sap-hana-install.yml -e "@inputs/HDB.install"`

- Target Host Installation
    - `ansible-playbook -i "<target-host>" sap-hana-install.yml -e "@inputs/HDB.install"`

## Sample playbooks
### Sample playbook for installing a new scale-up (=single node) SAP HANA system

```yaml
---
- hosts: all
  collections:
    - community.sap_install
  become: true
  vars:
    sap_hana_install_software_directory: /software/hana
    sap_hana_install_common_master_password: 'NewPass$321'
    sap_hana_install_sid: 'H01'
    sap_hana_install_instance_number: '00'
  roles:
    - sap_hana_install
```

### Sample playbook for installing a new scale-out SAP HANA system

```yaml
---
- hosts: all
  collections:
    - community.sap_install
  become: true
  vars:
    sap_hana_install_software_directory: /software/hana
    sap_hana_install_common_master_password: 'NewPass$321'
    sap_hana_install_root_password: 'NewPass$321'
    sap_hana_install_addhosts: 'host2:role=worker,host3:role=worker:group=g02,host4:role=standby:group=g02'
    sap_hana_install_sid: 'H01'
    sap_hana_install_instance_number: '00'
  roles:
    - sap_hana_install
```

### Sample playbook for adding additional nodes to an existing SAP HANA installation

```yaml
---
- hosts: all
  collections:
    - community.sap_install
  become: true
  vars:
    sap_hana_install_software_directory: /software/hana
    sap_hana_install_new_system: no
    sap_hana_install_addhosts: 'host2:role=worker,host3:role=worker:group=g02,host4:role=standby:group=g02'
    sap_hana_install_common_master_password: 'NewPass$321'
    sap_hana_install_root_password: 'NewPass$321'
    sap_hana_install_sid: 'H01'
    sap_hana_install_instance_number: '00'
  roles:
    - sap_hana_install
```

You can find more complex playbooks in directory `playbooks` of the collection `community.sap_install`.

## Flow

### New SAP HANA Installation

#### Perform Initial Checks

- If variable `sap_hana_install_check_sidadm_user` is undefined or set to `y`: Check if user sidadm exists. If yes,
  abort the role.

- Check if directory `/hana/shared/<sid>` exists. If yes, abort the role.

- Check if directory `/usr/sap/<sid>` exists. If yes, abort the role.

#### Pre-Install 

- Set all passwords to follow master password if set to 'y'

- Prepare software located in directory `sap_hana_install_software_directory`

    - If file `hdblcm` is found, proceed to 4.

    - If not, proceed to 3.

- Prepare .SAR files for `hdblcm` 

    - Get all .SAR files from `sap_hana_install_software_directory`

    - Extract all .SAR files from `sap_hana_install_software_directory`

- Check existence of `hdblcm` in `SAP_HANA_DATABASE` directory from the extracted SAR files

- Process SAP HANA `configfile` based on input parameters

#### SAP HANA Install

- Execute hdblcm

#### Post-Install

- Create and Store Connection Info in hdbuserstore

- Set Log Mode key to overwrite value and apply to system

- Apply SAP HANA license to the new deployed instance if set to 'y'

- Set expiry of Unix created users to 'never'

- Update `/etc/hosts` (optional - yes by default)

- Apply firewall rules (optional - no by default)

- Generate input file for `sap_swpm`

- Print a short summary of the result of the installation

### Add hosts to an existing SAP HANA Installation

#### Pre-Install 

- Process SAP HANA `configfile` based on input parameters

#### SAP HANA Add Hosts

- For each host to be added, check if there is:
  - an instance profile in `/hana/shared/<SID>/profile/<SID>_HDB_<NR>`
  - a directory `/usr/sap/<SID>/HDB<NR>/`
  - an entry in the output of `./hdblcm --list_systems`
  If any of the above is true, abort the role.

- Execute hdblcm

#### Post-Install

- Print a short summary of the result of the installation
