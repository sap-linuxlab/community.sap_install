# sap_hana_install Ansible Role

Ansible role for SAP HANA Installation

## Requirements

The role requires additional collections which are specified in `meta/collection-requirements.yml`. Before using this role,
make sure that the required collections are installed, for example by using the following command:

`ansible-galaxy install -vv -r meta/collection-requirements.yml`

### Configure your system for the installation of SAP HANA

- Make sure required volumes and filesystems are configured in the host.
You can use the role `sap_storage_setup` to configure this. More info [here](/roles/sap_storage_setup)

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
    [root@hanahost SAP_HANA_INSTALLATION]# ls -l *.EXE *.SAR
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
variable `sap_hana_install_sapcar_filename`. Example:
```
sap_hana_install_sapcar_filename: SAPCAR_1115-70006178.EXE
```

If more than one SAR file for a certain software product is present in the software directory, the automatic
handling of such SAR files will fail after extraction, when moving the newly created product directories
(like `SAP_HOST_AGENT`) to already existing destinations.
For avoiding such situations, use following variable to provide a list of SAR files to extract:

`sap_hana_install_sarfiles`.

Example:
```
sap_hana_install_sarfiles:
  - SAPHOSTAGENT54_54-80004822.SAR
  - IMDB_SERVER20_060_0-80002031.SAR
```

If there is a file named `<filename>.sha256` in the software download directory
`sap_hana_install_software_directory` which contains the checksum and the file name similar to the output
of the sha256sum command, the role will examine the sha256sum for the corresponding SAPCAR or SAR file and the
processing will continue only if the checksum matches.

#### Extracted SAP HANA Software Installation Files

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

## Further Variables and Parameters

### Input Parameters

If the variable `sap_hana_install_check_sidadm_user` is set to `no`, the role will install SAP HANA even
if the sidadm user exists. Default is `yes`, in which case the installation will not be performed if the
sidadm user exists.

The variable `sap_hana_install_new_system` determines if the role will perform a fresh SAP HANA installation
or if it will add further hosts to an existing SAP HANA system as specified by variable
`sap_hana_install_addhosts`. Default is `yes` for a fresh SAP HANA installation.

The role can be configured to also set the required firewall ports for SAP HANA. If this is desired, set
the variable `sap_hana_install_update_firewall` to `yes` (default is `no`). The firewall ports are defined
in a variable which is compatible with the variable structure used by Linux System Role `firewall`.
The firewall ports for SAP HANA are defined in member `port` of the first field of variable
`sap_hana_install_firewall` (`sap_hana_install_firewall[0].port`), see file `defaults/main.yml`. If the
member `state` is set to `enabled`, the ports will be enabled. If the member `state` is set to `disabled`,
the ports will be disabled, which might be useful for testing.

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

These checks are only performed if `sap_hana_install_force` is set to `true`. Its default value is `false`
- If variable `sap_hana_install_check_sidadm_user` is undefined or set to `y`: Check if user sidadm exists. If yes,
  abort the role.

- Check if `/usr/sap/hostctrl/exe/saphostctrl` exists and get info on running HANA instances.
  - If conflicting instances exist the role aborts with a failure
  - If desired instance is running, the role aborts with success

- If  `/usr/sap/hostctrl/exe/saphostctrl`  does not exist
   -  Check if directory `/hana/shared/<sid>` exists. If yes and not empty, abort the role.
  - Check if directory `/usr/sap/<sid>` exists. If yes and not empty, abort the role.

#### Pre-Install

- Set all passwords to follow master password if set to 'y'.

- Prepare the software located in directory `sap_hana_install_software_directory`:

    - If file `hdblcm` is found, skip the next step and proceed with the `hdblcm` existence check.

    - If file `hdblcm` ist not found, proceed with the next step.

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

- Apply SAP HANA license to the new deployed instance if set to `y`.

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

## Tags

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

Sample call for only processing the SAPCAR and SAR files and creating the hdblcm configfile:
```
# ansible-playbook sap-hana-install.yml --tags=sap_hana_install_preinstall --skip-tags=sap_hana_install_chown_hana_directories
```

Sample call for only processing the SAPCAR files:
```
# ansible-playbook sap-hana-install.yml --tags=sap_hana_install_prepare_sapcar
```

Sample call for only processing the SAPCAR and SAR files, without extracting the SAR files:
```
# ansible-playbook sap-hana-install.yml --tags=sap_hana_install_prepare_sarfiles --skip-tags=sap_hana_install_extract_sarfiles
```

Sample call for only displaying the SAP HANA hdblcm command line:
```
# ansible-playbook sap-hana-install.yml --tags=sap_hana_install_hdblcm_commandline
```

## License

Apache license 2.0

## Author Information

Red Hat for SAP Community of Practice, IBM Lab for SAP Solutions, Markus Koch, Thomas Bludau, Bernd Finger, Than Ngo, Rainer Leber
