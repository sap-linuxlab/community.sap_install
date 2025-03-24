<!-- BEGIN Title -->
# sap_hana_install Ansible Role
<!-- END Title -->
![Ansible Lint for sap_hana_install](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_hana_install.yml/badge.svg)

## Description
<!-- BEGIN Description -->
The Ansible role `sap_hana_install` installs SAP HANA using the SAP HANA database lifecycle manager (HDBLCM).
<!-- END Description -->

<!-- BEGIN Dependencies -->
## Dependencies
- `fedora.linux_system_roles`
    - Roles:
        - `selinux`

Install required collections by `ansible-galaxy collection install -vv -r meta/collection-requirements.yml`.
<!-- END Dependencies -->

## Prerequisites
<!-- BEGIN Prerequisites -->
Managed nodes:
- Directory with SAP Installation media is present and `sap_install_media_detect_source_directory` updated. Download can be completed using [community.sap_launchpad](https://github.com/sap-linuxlab/community).
- Ensure that servers are configured for SAP HANA. See [Recommended](#recommended) section.
- Ensure that volumes and filesystems are configured correctly. See [Recommended](#recommended) section.


### Prepare SAP HANA installation media
Place the following files in directory /software/hana or in any other directory specified by variable
`sap_hana_install_software_directory`:
1. The SAPCAR executable for the correct hardware architecture
2. The SAP HANA Installation .SAR file
    - SAP HANA 2.0 Server - `IMDB_SERVER*.SAR` file
3. Optional - SAP HANA Components .SAR files
    - Include other optional components such as `IMDB_AFL*.SAR` or `IMDB_LCAPPS*.SAR`
4. Optional - SAP Host Agent .SAR file
    - Include other optional components such as `SAPHOSTAGENT*SAR`

Example of `sap_hana_install_software_directory` content for SAP HANA installation:
```console
[root@hanahost SAP_HANA_INSTALLATION]# ls -l *.EXE *.SAR
-rwxr-xr-x. 1 nobody nobody  149561376 Mar  4  2021 IMDB_AFL20_054_1-80001894.SAR
-rwxr-xr-x. 1 nobody nobody  211762405 Mar  4  2021 IMDB_CLIENT20_007_23-80002082.SAR
-rwxr-xr-x. 1 nobody nobody    4483040 Mar  4  2021 SAPCAR_1010-70006178.EXE
-rwxr-xr-x. 1 nobody nobody  109492976 Mar  4  2021 IMDB_LCAPPS_2054_0-20010426.SAR
-rwxr-xr-x. 1 nobody nobody  109752805 Mar  4  2021 VCH202000_2054_0-80005463.SAR
-rwxr-xr-x. 1 nobody nobody 3694683699 Mar  4  2021 IMDB_SERVER20_054_0-80002031.SAR
-rwxr-xr-x. 1 nobody nobody   89285401 Sep 30 04:24 SAPHOSTAGENT51_51-20009394.SAR
```

**Considerations:**
- If more than one SAPCAR EXE file is present in the software directory, the role will select the latest version
  for the current hardware architecture. Alternatively, the file name of the SAPCAR EXE file can also be set with
  variable `sap_hana_install_sapcar_filename`. Example:
  ```
  sap_hana_install_sapcar_filename: SAPCAR_1115-70006178.EXE
  ```
- If more than one SAR file for a certain software product is present in the software directory, the automatic
  handling of such SAR files will fail after extraction, when moving the newly created product directories
  (like `SAP_HOST_AGENT`) to already existing destinations.
  For avoiding such situations, use following variable to provide a list of SAR files to extract: `sap_hana_install_sarfiles`.

  Example:
  ```
  sap_hana_install_sarfiles:
    - SAPHOSTAGENT54_54-80004822.SAR
    - IMDB_SERVER20_060_0-80002031.SAR
  ```

- If there is a file named `<filename>.sha256` in the software download directory
  `sap_hana_install_software_directory` which contains the checksum and the file name similar to the output
  of the sha256sum command, the role will examine the sha256sum for the corresponding SAPCAR or SAR file and the
  processing will continue only if the checksum matches.


### Extracted SAP HANA Software Installation Files
This role will detect if there is a file `hdblcm` already present in the directory specified by variable
`sap_hana_install_software_extract_directory` or in any directory below. If If found, it will skip
the .SAR extraction phase and proceed with the installation.

The default for `sap_hana_install_software_extract_directory` is `{{ sap_hana_install_software_directory }}/extracted` but it
can be set to a different directory.

If this role is executed on more than one host in parallel and the software extraction directory is shared among those hosts,
the role will only extract the files on the first host on which the extraction has started. The role will proceed on the other hosts
after the extraction of SAR files has completed.

If NFS is used for sharing the SAP HANA installation media between the nodes, then it is required to define
`sap_hana_install_configfile_directory`. The default for `sap_hana_install_configfile_directory` is
"{{ sap_hana_install_software_extract_directory }}/configfiles". This variable should point to a non nfs path. After installation,
if a cleanup of configfile is required, then set `sap_hana_install_cleanup_configfile_directory` as true. If a cleanup of
software extract directory is required then set `sap_hana_install_cleanup_extract_directory` as true. The default value for both
these cleanup actions are false.


- Example of directory `sap_hana_install_software_extract_directory` containing extracted SAP HANA software installation files
```console
[root@hanahost extracted]# ll -lrt
drwxr-xr-x 4 root root 4096 Sep 30 04:55 SAP_HANA_AFL
drwxr-xr-x 5 root root 4096 Sep 30 04:55 SAP_HANA_CLIENT
drwxr-xr-x 4 root root 4096 Sep 30 04:55 SAP_HANA_LCAPPS
drwxr-xr-x 8 root root 4096 Sep 30 04:57 SAP_HANA_DATABASE
drwxr-xr-x 2 root root 4096 Sep 30 04:58 SAP_HOST_AGENT
drwxr-xr-x 4 root root 4096 Sep 30 04:58 VCH_AFL_2020
```

#### SAP HANA hdblcm Configfile Processing

By default, the hdblcm configfile will be created dynamically in each run, as follows: After the role has
found the hdblcm command or extracted the SAP HANA SAR file, it will call the hdblcm command with the
option `--dump_configfile_template` to create a configfile template, which will then be converted into
a Jinja2 configfile template according to the following rules: For each hdblcm parameter, the value
will be either the value of the role variable prepended by the role name and an underscore, or a
default (if present in the hdblcm configfile template).

Example: The value of hdblcm parameter `system_usage` will be set to the value of role variable
`sap_hana_install_system_usage` or to `custom` in case the role variable has not been set.

The result of the templating is a new, customized hdblcm configfile, which will be used by the
hdblcm command for the SAP HANA installation.

This provides great flexibility for handling different SAP HANA releases, which typically have a slightly
different set of hdblcm parameters. For preparing the installation of a new SAP HANA system, it can be useful
to run the role with tag `sap_hana_install_preinstall` first. This will display the full path names of the
hdblcm configfile template, the Jinja2 template, and the result of the templating. By comparing the hdblcm
configfile template with the templating result (indicated by placeholder `TEMPLATING_RESULT` below), you
can quickly check if all role variables for the hdblcm command are set correctly and make any necessary
adjustments to the role variables.

For displaying only the modified default lines, in two columns, use:
`# diff -y --suppress-common-lines hdblcm_configfile_template.cfg TEMPLATING_RESULT`

For checking and comparing all non-empty hdblcm parameter settings, use:
`# diff -y <(awk 'BEGIN{FS="="}/^[a-z]/&&length($2)>0{print $0}' hdblcm_configfile_template.cfg)
   <(awk 'BEGIN{FS="="}/^[a-z]/&&length($2)>0{print $0}' TEMPLATING_RESULT)`

Note: If there is a file named `configfile.cfg` in the directory specified by role variable
`sap_hana_install_configfile_directory`, this file will be used and no dynamic hdblcm configfile processing
will be performed. Be aware that when using this file, any modifications to role variables after creation
of this file will not be reflected.

<!-- END Prerequisites -->

## Execution
<!-- BEGIN Execution -->
<!-- END Execution -->

<!-- BEGIN Execution Recommended -->
### Recommended
It is recommended to execute this role together with other roles in this collection, in the following order:</br>
1. [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure)
2. [sap_hana_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_preconfigure)
3. [sap_install_media_detect](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_install_media_detect)
4. *`sap_hana_install`*
<!-- END Execution Recommended -->

### Execution Flow
<!-- BEGIN Execution Flow -->
#### Perform Initial Checks

These checks will be performed by default but can be skipped by setting `sap_hana_install_force` to `true`.
- If variable `sap_hana_install_check_sidadm_user` is undefined or set to `yes`: Check if user sidadm exists. If yes,
  abort the role.
- Check if `/usr/sap/hostctrl/exe/saphostctrl` exists and get info on running HANA instances:
  - If a conflicting instances exist, the role aborts with a failure
  - If the desired instance is running, the role aborts with success
- If `/usr/sap/hostctrl/exe/saphostctrl`  does not exist:
  - Check if the directory `/hana/shared/<sid>` exists. If yes and not empty, abort the role.
  - Check if the directory `/usr/sap/<sid>` exists. If yes and not empty, abort the role.

#### Pre-Install

- Set all passwords to follow master password if set to 'y'.

- Prepare the software located in directory `sap_hana_install_software_directory`:

    - If file `hdblcm` is found, skip the next step and proceed with the `hdblcm` existence check.

    - If file `hdblcm` is not found, proceed with the next step.

- Prepare SAR files for `hdblcm`:

    - Get a list of hardware matching SAPCAR executables from `sap_hana_install_software_directory` in case its file name is not
      provided by role variable.

    - Select the most recent version of SAPCAR from the hardware matching SAPCAR executables identified before.

    - Get all SAR files from `sap_hana_install_software_directory` or use the SAR files provided by the corresponding role variable, if set.

    - Extract all SAR files into `sap_hana_install_software_extract_directory`.

Note: For each SAPCAR or SAR file called or used by the role, if variable `sap_hana_install_verify_checksums`
is set to `yes`, the role will perform a checksum verification against a specific or global checksum file.

- Check existence of `hdblcm` in `SAP_HANA_DATABASE` directory from the extracted SAR files.

- Check the existence of file `configfile.cfg` in the directory `configfiles` below `sap_hana_install_software_extract_directory`.

If this file exists, copy it to a temporary directory for use by the hdblcm command. Be aware that when using this file,
any modifications to role variables after creation of this file will not be reflected.

If this file is not present, perform the following three steps:

- Create a hdblcm configfile template directly from the hdblcm command, using option `dump_configfile_template`.

- Convert the configfile template into a Jinja2 template and download it to the control node.

- Process the Jinja2 template, using the configured role variables or default settings, to create a customized hdblm configfile
in a temporary directory for use by the hdblcm command in the next step.

#### SAP HANA Install

- Execute hdblcm, using the configfile mentioned above.

#### Post-Install

- Create and Store Connection Info in hdbuserstore.

- Set Log Mode key to overwrite value and apply to system.

- Apply SAP HANA license to the new deployed instance if set to `yes`.

- Set expiry of Unix created users to `never`.

- Update `/etc/hosts` (optional - `yes` by default).

- Apply firewall rules (optional - `no` by default).

- Generate input file for `sap_swpm`.

- Print a short summary of the result of the installation.

### Add hosts to an existing SAP HANA Installation

#### Pre-Install

- Process SAP HANA configfile based on input parameters.

#### SAP HANA Add Hosts

- For each host to be added, check if there is:
  - an instance profile in `/hana/shared/<SID>/profile/<SID>_HDB_<NR>`
  - a directory `/usr/sap/<SID>/HDB<NR>/`
  - an entry in the output of `./hdblcm --list_systems`
  If any of the above is true, abort the role.

- Execute hdblcm.

#### Post-Install

- Print a short summary of the result of the installation.
<!-- END Execution Flow -->

### Example
<!-- BEGIN Execution Example -->
#### Example playbook for installing a new scale-up (=single node) SAP HANA system
```yaml
---
- name: Ansible Play for SAP HANA installation - One host
  hosts: all
  become: true
  tasks:
    - name: Execute Ansible Role sap_hana_install
      ansible.builtin.include_role:
        name: community.sap_install.sap_hana_install
      vars:  
        sap_hana_install_software_directory: /software/hana
        sap_hana_install_common_master_password: 'NewPass$321'
        sap_hana_install_sid: 'H01'
        sap_hana_install_instance_nr: '00'
```

#### Example playbook for installing a new scale-out SAP HANA system
```yaml
---
- name: Ansible Play for SAP HANA installation - Scale-out
  hosts: all
  become: true
  tasks:
    - name: Execute Ansible Role sap_hana_install
      ansible.builtin.include_role:
        name: community.sap_install.sap_hana_install
      vars:  
        sap_hana_install_software_directory: /software/hana
        sap_hana_install_common_master_password: 'NewPass$321'
        sap_hana_install_root_password: 'NewPass$321'
        sap_hana_install_addhosts: 'host2:role=worker,host3:role=worker:group=g02,host4:role=standby:group=g02'
        sap_hana_install_sid: 'H01'
        sap_hana_install_instance_nr: '00'
```

#### Example playbook for adding additional nodes to an existing SAP HANA installation
```yaml
---
- name: Ansible Play for SAP HANA installation - Add host
  hosts: all
  become: true
  tasks:
    - name: Execute Ansible Role sap_hana_install
      ansible.builtin.include_role:
        name: community.sap_install.sap_hana_install
      vars:  
        sap_hana_install_software_directory: /software/hana
        sap_hana_install_new_system: no
        sap_hana_install_addhosts: 'host2:role=worker,host3:role=worker:group=g02,host4:role=standby:group=g02'
        sap_hana_install_common_master_password: 'NewPass$321'
        sap_hana_install_root_password: 'NewPass$321'
        sap_hana_install_sid: 'H01'
        sap_hana_install_instance_nr: '00'
```
<!-- END Execution Example -->


<!-- BEGIN Role Tags -->
### Role Tags
With the following tags, the role can be called to perform certain activities only:
- tag `sap_hana_install_check_installation`: Perform an installation check, using `hdbcheck` or
  `hdblcm --action=check_installation`.
- tag `sap_hana_install_chown_hana_directories`: Only perform the chown of the SAP HANA directories
  `/hana`, `/hana/shared`, `/hana/log`, and `/hana/data`. The main purpose of this tag is to use it
  with `--skip-tags`, to skip modifying these directories. This can be useful when using tag
  `sap_hana_install_preinstall`.
- tag `sap_hana_install_configure_firewall`: Use this flag to only configure the firewall ports for
  SAP HANA. Note: The role variable `sap_hana_install_update_firewall` has to be set to `yes` as
  well.
- tag `sap_hana_install_extract_sarfiles`: Use this flag with `--skip-tags` to run the SAR file
  preparation steps of tag `sap_hana_install_prepare_sarfiles` without extracting the SAR files.
- tag `sap_hana_install_generate_input_file`: Only generate the input file for SAP Application
  deployment
- tag `sap_hana_install_hdblcm_commandline`: Only show the hdblcm command line, without processing
  the hdblcm template. This can be useful for checking the hdblcm command line options, especially
  when using the `addhosts` function.
- tag `sap_hana_install_preinstall`: Only perform pre-install activities. This includes selecting
  the SAPCAR EXE file, extracting the SAR files if necessary, searching for hdblcm, and creating
  the hdblcm configfile.
- tag `sap_hana_install_prepare_sapcar`: Only copy the SAPCAR EXE files for the current architecture
  to the extraction directory, verify the checksums of these files, and select the latest
  version. Or copy the SAPCAR EXE file if given by role variable `sap_hana_install_sapcar_filename`
  and then verify the checksum.
- tag `sap_hana_install_prepare_sarfiles`: Run the steps of tag `sap_hana_install_prepare_sapcar`
  to select the correct SAPCAR file, then copy the selected or provided SAR files to the
  extraction directory (if requested), then verify the checksums of each SAR file. Lastly, extract
  these SAR files to the extraction directory.
- tag `sap_hana_install_set_log_mode`: Only set the log mode of an existing HANA installation to
  `overwrite`.
- tag `sap_hana_install_store_connection_information`: Only run the `hdbuserstore` command

<details>
  <summary><b>How to run sap_hana_install with tags</b></summary>

  #### Process SAPCAR and SAR files and create the hdblcm configfile:
  ```console
  ansible-playbook sap-hana-install.yml --tags=sap_hana_install_preinstall --skip-tags=sap_hana_install_chown_hana_directories
  ```

  #### Process only SAPCAR files:
  ```console
  ansible-playbook sap-hana-install.yml --tags=sap_hana_install_prepare_sapcar
  ```

  #### Process SAPCAR and SAR files without extracting SAR files:
  ```console
  ansible-playbook sap-hana-install.yml --tags=sap_hana_install_prepare_sarfiles --skip-tags=sap_hana_install_extract_sarfiles
  ```

  #### Display SAP HANA hdblcm command without using it 
  ```
  ansible-playbook sap-hana-install.yml --tags=sap_hana_install_hdblcm_commandline
  ```
</details>


<!-- END Role Tags -->

<!-- BEGIN Further Information -->
## Further Information
- Starting with SAP HANA 2.0 SPS08, the component LSS (Local Secure Store) will be installed by default
when installing SAP HANA. This requires the installation execution mode to be set to 'optimized', which is
now set in the file `defaults/main.yml`.

- For more examples on how to use this role in different installation scenarios, refer to the [ansible.playbooks_for_sap](https://github.com/sap-linuxlab/ansible.playbooks_for_sap) playbooks.
<!-- END Further Information -->

## License
<!-- BEGIN License -->
Apache 2.0
<!-- END License -->

## Maintainers
<!-- BEGIN Maintainers -->
- [Bernd Finger](https://github.com/berndfinger)
<!-- END Maintainers -->

## Role Variables
<!-- BEGIN Role Variables -->
### sap_hana_install_sid

- _Type:_ `string`

Enter SAP HANA System ID (SID).

### sap_hana_install_number

- _Type:_ `string`

Enter SAP HANA Instance number.

### sap_hana_install_fapolicyd_integrity

- _Type:_ `string`
- _Default:_ `sha256`

Select `fapolicyd` integrity check option.</br>
Available values: `none`, `size`, `sha256`, `ima`.

### sap_hana_install_check_sidadm_user

- _Type:_ `bool`
- _Default:_ `True`

Set to `False` to install SAP HANA even if the `sidadm` user exists.</br>
Default is `True`, in which case the installation will not be performed if the `sidadm` user exists.

### sap_hana_install_new_system

- _Type:_ `bool`
- _Default:_ `True`

Set to `False` to use existing SAP HANA database and add more hosts using variable `sap_hana_install_addhosts`.</br>
Default is `True`, in which case fresh SAP HANA installation will be performed.

### sap_hana_install_update_firewall

- _Type:_ `bool`
- _Default:_ `False`

The role can be configured to also set the required firewall ports for SAP HANA. If this is desired, set the variable `sap_hana_install_update_firewall` to `yes` (default is `no`).</br>
The firewall ports are defined in a variable which is compatible with the variable structure used by Linux System Role `firewall`.</br>
The firewall ports for SAP HANA are defined in member `port` of the first field of variable `sap_hana_install_firewall` (`sap_hana_install_firewall[0].port`), see file `defaults/main.yml`.</br>
If the member `state` is set to `enabled`, the ports will be enabled. If the member `state` is set to `disabled`, the ports will be disabled, which might be useful for testing.</br>

Certain parameters have identical meanings, for supporting different naming schemes in playbooks and inventories.</br>
You can find those in the task `Rename some variables used by hdblcm configfile` of the file `tasks/main.yml`.</br>
Example: The parameter `sap_hana_install_number`, which is used by the role to define the hdblm parameter `number` (= SAP HANA instance number)</br>
 can be defined by setting `sap_hana_instance_number`, `sap_hana_install_instance_nr`, `sap_hana_install_instance_number`, or `sap_hana_install_number`.</br>
 The order of precedence is from left to right.
<!-- END Role Variables -->
