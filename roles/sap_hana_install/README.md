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

- Directory with SAP Installation media is present and `sap_install_media_detect_source_directory` updated. Download can be completed using [community.sap_launchpad](https://github.com/sap-linuxlab/community.sap_launchpad).
- Ensure that servers are configured for SAP HANA. See [Recommended](#recommended) section.
- Ensure that volumes and filesystems are configured correctly. See [Recommended](#recommended) section.
  - SAP HANA Scale-Out requires shared filesystems:
    - `/hana/shared` customizable in the variable `sap_hana_install_shared_path`.
    - `/lss/shared` customizable in the variable `sap_hana_install_lss_inst_path`. **Specific to SAP HANA 2.0 SPS08 or higher.**


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

- If more than one SAPCAR EXE file is present in the software directory, the role will select the latest version for the current hardware architecture.<br>
  Alternatively, the file name of the SAPCAR EXE file can also be set with variable `sap_hana_install_sapcar_filename`.<br>
  Example:<br>
```yaml
sap_hana_install_sapcar_filename: SAPCAR_1115-70006178.EXE
```
- If more than one SAR file for a certain software product is present in the software directory, the automatic
  handling of such SAR files will fail after extraction, when moving the newly created product directories
  (like `SAP_HOST_AGENT`) to already existing destinations.<br>
  For avoiding such situations, use following variable to provide a list of SAR files to extract: `sap_hana_install_sarfiles`.<br>
  Example:<br>
```yaml
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
This Ansible Role can be executed in following scenarios:

1. Install new SAP HANA System on one host.
    - `sap_hana_install_new_system` is `true`.
    - `sap_hana_install_addhosts` is not defined or empty String.
    - Playbook inventory: One host.

2. Install new SAP HANA System on multiple hosts for High Availability.
    - `sap_hana_install_new_system` is `true`.
    - `sap_hana_install_addhosts` is not defined or empty String.
    - Playbook inventory: Multiple hosts.

3. Install new SAP HANA Scale-Out System on multiple hosts.
    - `sap_hana_install_new_system` is `true`.
    - `sap_hana_install_addhosts` is defined as valid addhosts String.
    - Playbook inventory: Multiple hosts.

4. Install new hosts to existing SAP HANA Scale-Out System
    - `sap_hana_install_new_system` is `false`.
    - `sap_hana_install_addhosts` is defined as valid addhosts String.
    - `sap_hana_install_sapadm_password` is defined.
    - Playbook inventory: Multiple hosts.
<!-- END Execution -->

<!-- BEGIN Execution Recommended -->
### Recommended
It is recommended to execute this role together with other roles in this collection, in the following order:</br>

1. [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure)
2. [sap_hana_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_preconfigure)
3. [sap_install_media_detect](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_install_media_detect)
4. *`sap_hana_install`*
<!-- END Execution Recommended -->

<!-- BEGIN Execution Flow -->
### Execution Flow
#### Validate mandatory variables
- If the mandatory variables are undefined or invalid (e.g. empty string, wrong length, etc.), abort the role with failure. Variables that are mandatory:
  - `sap_hana_install_sid`
  - `sap_hana_install_number`
  - `sap_hana_install_master_password`
  - `sap_hana_install_addhosts` if the variable `sap_hana_install_new_system` is set to `false`.
- All other password variables are set to the value of `sap_hana_install_master_password` if `sap_hana_install_use_master_password` is set to `y`.
- If the variable `sap_hana_install_new_system` is undefined or invalid and `sap_hana_install_master_password` is not set to `true`, abort the role with failure.


#### Check existing installation
This part is performed when:

- Always, unless `sap_hana_install_force` is set to `true`.

- If the file `/usr/sap/hostctrl/exe/saphostctrl` is present, get a list of instances with `saphostctrl -function ListInstances`:
  - If an instance with the same SID and Instance Number is found, skip Pre-Tasks and Installation and proceed to either Addhosts or Post-Tasks.
  - If an instance with the same SID but different Instance number is found, abort the role with failure.
  - If an instance with the same Instance number but different SID is found, abort the role with failure.
- If the file `/usr/sap/hostctrl/exe/saphostctrl` is not present:
  - If the directory `/hana/shared/<SID>` exists and contains files, abort the role with failure.
  - If the directory `/usr/sap/<SID>` exists and contains files, abort the role with failure.
  - If the variable `sap_hana_install_groupid` is defined, check if group `sapsys` already exists:
    - If it already exists with a different group ID, abort the role with failure.
  - If the variable `sap_hana_install_check_sidadm_user` is defined, check if user `<sidadm>` already exists:
    - If it already exists, abort the role with failure.
- If the existing instance was not found when adding hosts, abort the role with failure.


#### Check Addhosts
This part is performed when:

- The variable `sap_hana_install_addhosts` is defined and not empty String.

**Addhosts are relevant to both Installation and Addhosts operations, because we need to delegate Pre-Tasks and Post-Tasks to them.**

Steps:

1. If the variable `sap_hana_install_addhosts` does not contain hosts, abort the role with failure.
    - This list of the `all hosts` is used for all Post-Tasks steps for idempotency.
2. Gather list of all Instance profiles in `/hana/shared/<SID>/profile/`.
3. Gather list of all directories in `/usr/sap/<SID>/HDB<Instance Number>/`.
4. If the existing instance profile or directory was found in hosts list, create separate list without them.
    - This list of the `new hosts` is used for one-time tasks. 


#### Pre-Tasks for Installation
This part is performed when:

- The variable `sap_hana_install_new_system` is set to `true`.
- Existing SAP HANA was not detected.

Steps:

1. If the variable `sap_hana_install_configure_fapolicyd` is set to `true` and operating system is `RedHat`, install and disable `fapolicyd` on all new hosts.
2. Configure permissions for the SAP HANA directories on all new hosts.
3. If the variable `sap_hana_install_configure_selinux` is set to `true`, configure `SELinux` on all new hosts.
4. Prepare the directory defined in variable `sap_hana_install_software_directory`.
5. If the `hdblcm` was not found in the directory `sap_hana_install_software_directory`:
    - Find latest `SAPCAR` executable in the directory `sap_hana_install_software_directory` and use latest one matching OS Architecture.
    - Extract found `SAR` files using selected `SAPCAR` executable.
    - If the variable `sap_hana_install_verify_checksums` is set to `true`, validate checksum.
6. If the file `configfiles/configfile.cfg` is found in the directory defined in `sap_hana_install_software_directory`, make copy of it and use it for installation.
  - If the file was not found, create template using `hdblcm` command and fill it in with jinja2 template.


#### Pre-Tasks for Addhosts
This part is performed when:

- The variable `sap_hana_install_new_system` is set to `false`.
- Existing SAP HANA was detected.
- New hosts identified in the variable `sap_hana_install_addhosts`.

Steps:

1. Gather details of user `<sid>adm` and group `sapsys` on managed node.
    - If the user or group is not present, abort the role with failure.
    - Generate password hash for `sapadm` user using the value of `sap_hana_install_sapadm_password` variable.
2. Create the user `<sid>adm` on all addhosts.
    - This is not required during installation, because the `root` user is used instead.
3. If the variable `sap_hana_install_configure_fapolicyd` is set to `true` and operating system is `RedHat`, install and disable `fapolicyd` on all new hosts.
4. Configure permissions for the SAP HANA directories on all new hosts.
5. If the variable `sap_hana_install_configure_selinux` is set to `true`, configure `SELinux` on all new hosts.
6. If the file `configfiles/configfile.cfg` is found in the directory defined in `sap_hana_install_software_directory`, make copy of it and use it for installation.
    - If the file was not found, create template using `hdblcm` command and fill it in with jinja2 template.


#### Installation
This part is performed when:

- The variable `sap_hana_install_new_system` is set to `true`.
- Existing SAP HANA was not detected.

Steps:

1. Execute the `hdblcm` executable in the directory `sap_hana_install_software_directory` using the configfile prepared in pre-tasks.


#### Addhosts
This part is performed when:

- The variable `sap_hana_install_new_system` is set to `false`.
- Existing SAP HANA was detected.
- New hosts identified in the variable `sap_hana_install_addhosts`.

Steps:

1. Prepare new addhosts string only with new hosts and update `configfile.cfg`.
2. Execute the `hdblcm` executable in the directory `/hana/shared/<SID>/hdblcm/` using the configfile prepared in pre-tasks.


#### Post-Tasks for Installation
This part is performed when:

- The variable `sap_hana_install_new_system` is set to `true`.

Steps:

1. Update Secure User Store configuration (`hdbuserstore`) for `<sid>adm` user, for new installations.
2. Set Log Mode key to overwrite value and apply to system, for new installations.
3. Apply SAP HANA license if the variable `sap_hana_install_apply_license` is set to `true`, for new installations.
4. Recreate the initial tenant database if the variable `sap_hana_install_recreate_tenant_database` is set to `true`, for new installations.
5. Set expiration of unix users to `never` if the variable `sap_hana_install_set_sidadm_noexpire` is set to `true`, for new installations.
6. Apply firewall rules if the variable `sap_hana_install_update_firewall` is set to `true`.
7. Apply SELinux policies if the variable `sap_hana_install_configure_selinux` is set to `true`.
8. (Red Hat specific) Configure `fapolicyd` if the variable `sap_hana_install_configure_fapolicyd` is set to `true`.
Additionally, if `sap_hana_install_enable_fapolicyd` is set to `true`, also enable and start the `fapolicyd` service.
9. Output final status of installed system.


#### Post-Tasks for Addhosts
This part is performed when:

- The variable `sap_hana_install_new_system` is set to `false`.

Steps:

1. Update Secure User Store configuration (`hdbuserstore`) for `<sid>adm` user, for new hosts.
5. Set expiration of unix users to `never` if the variable `sap_hana_install_set_sidadm_noexpire` is set to `true`, for new hosts.
6. Apply firewall rules if the variable `sap_hana_install_update_firewall` is set to `true`.
7. Apply SELinux policies if the variable `sap_hana_install_configure_selinux` is set to `true`.
8. (Red Hat specific) Configure `fapolicyd` if the variable `sap_hana_install_configure_fapolicyd` is set to `true`.
Additionally, if `sap_hana_install_enable_fapolicyd` is set to `true`, also enable and start the `fapolicyd` service.
9. Output final status of installed system.
<!-- END Execution Flow -->

### Example
<!-- BEGIN Execution Example -->
#### Example playbook for installing a new scale-up (=single node) SAP HANA system
```yaml
---
- name: Ansible Play for SAP HANA installation - One host
  hosts: host0
  become: true
  tasks:
    - name: Execute Ansible Role sap_hana_install
      ansible.builtin.include_role:
        name: community.sap_install.sap_hana_install
      vars:
        sap_hana_install_software_directory: /software/hana
        sap_hana_install_master_password: 'My SAP HANA Master Password'
        sap_hana_install_sid: 'H01'
        sap_hana_install_instance_nr: '00'
```

#### Example playbook for installing a new scale-out SAP HANA system
Installs SAP HANA on `host0` and other hosts listed in `sap_hana_install_addhosts`: `host1` and `host2`.</br>
**NOTE:** Requires working SSH communication between hosts.
```yaml
---
- name: Ansible Play for SAP HANA installation - Scale-out
  hosts: host0, host1, host2, host3
  become: true
  tasks:
    - name: Execute Ansible Role sap_hana_install
      ansible.builtin.include_role:
        name: community.sap_install.sap_hana_install
      vars:
        sap_hana_install_software_directory: /software/hana
        sap_hana_install_master_password: 'My SAP HANA Master Password'
        sap_hana_install_root_password: 'My root password'
        sap_hana_install_addhosts: 'host1:role=worker,host2:role=worker:group=g02,host3:role=standby:group=g02'
        sap_hana_install_sid: 'H01'
        sap_hana_install_instance_nr: '00'
```

#### Example playbook for adding additional nodes to an existing SAP HANA installation
Installs SAP HANA on `host1` and `host2`, while running on host `host0` where existing SAP HANA is installed.</br>
**NOTE:** Requires working SSH communication between hosts.
```yaml
---
- name: Ansible Play for SAP HANA installation - Add hosts
  hosts: host0, host1
  become: true
  tasks:
    - name: Execute Ansible Role sap_hana_install
      ansible.builtin.include_role:
        name: community.sap_install.sap_hana_install
      vars:
        sap_hana_install_software_directory: /software/hana
        sap_hana_install_new_system: false
        sap_hana_install_addhosts: 'host1,host2'
        sap_hana_install_master_password: 'My SAP HANA Master Password'
        sap_hana_install_sapadm_password: 'My sapadm password'
        sap_hana_install_sid: 'H01'
        sap_hana_install_instance_nr: '00'
```
<!-- END Execution Example -->


<!-- BEGIN Role Tags -->
### Role Tags
Note: When using tags, only one tag at a time is possible.

With the following tags, the role can be called to perform certain activities only:

- tag `sap_hana_install_hdblcm_commandline`: Only show the hdblcm command line, without processing
  the hdblcm template. This can be useful for checking the hdblcm command line options, especially
  when using the `addhosts` function.
- tag `sap_hana_install_create_configfile`: Only generate the hdblcm configfile.
- tag `sap_hana_install_check_hana_exists`: Only check if there is already HANA installed with the
  desired SID and instance number.

The following tags have been removed in this release:

- tag `sap_hana_install_preinstall`
- tag `sap_hana_install_chown_hana_directories`
- tag `sap_hana_install_prepare_sapcar`
- tag `sap_hana_install_prepare_sarfiles`
- tag `sap_hana_install_extract_sarfiles`
- tag `sap_hana_install_configure_firewall`
- tag `sap_hana_install_configure_fapolicyd`
- tag `sap_hana_install_generate_input_file`
- tag `sap_hana_install_store_connection_information`
- tag `sap_hana_install_set_log_mode`
- tag `sap_hana_install_check_installation`

#### How to run sap_hana_install with tags

Display SAP HANA hdblcm command line without performing an installation:
```
ansible-playbook sap-hana-install.yml --tags=sap_hana_install_hdblcm_commandline
```

Only create the hdblcm configfile:
```console
ansible-playbook sap-hana-install.yml --tags=sap_hana_install_create_configfile
```

Perform a SAP HANA existence check:
```console
ansible-playbook sap-hana-install.yml --tags=sap_hana_install_check_hana_exists
```
<!-- END Role Tags -->

<!-- BEGIN Further Information -->
## Further Information
- ### Local Secure Store (LSS)
  Starting with SAP HANA 2.0 SPS08, the LSS component is installed by default when installing SAP HANA. This role will install all components (including LSS) and the installation will use default values.
  - If you don't want to install LSS, the simplest way is to set parameter `sap_hana_install_components: 'server'` (the default is `all`).
  - If you want to install LSS, check/set the following parameters and adjust accordingly as the defaults may not be suitable (list below shows the default values hdblcm will use):
    ```
    sap_hana_install_lss_inst_path: /lss/shared
    sap_hana_install_lss_user_password: ''
    sap_hana_install_lss_userid: ''
    sap_hana_install_lss_groupid: ''
    sap_hana_install_lss_user_home: /usr/sap/${SID}/lss/home
    sap_hana_install_lss_user_shell: /bin/sh
    sap_hana_install_lss_backup_password: ''
    sap_hana_install_secure_store: localsecurestore
    ```
> **NOTE**: SAP HANA 2.0 SPS08 requires LSS filesystem to be shared across all Scale-Out (cluster) hosts.</br>
> This role will check if directory defined in `sap_hana_insall_lss_inst_path` is present for SPS08 or higher and if it is mounted as shared file system.

- ### Additional examples
  For more examples on how to use this role in different installation scenarios, refer to the [ansible.playbooks_for_sap](https://github.com/sap-linuxlab/ansible.playbooks_for_sap) playbooks.
<!-- END Further Information -->

## License
<!-- BEGIN License -->
Apache 2.0
<!-- END License -->

## Maintainers
<!-- BEGIN Maintainers -->
- [Bernd Finger](https://github.com/berndfinger)
- [Marcel Mamula](https://github.com/marcelmamula)
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

### sap_hana_install_set_sidadm_noexpire

- _Type:_ `bool`
- _Default:_ `true`

Set to `true` to ensure the SAP system user `{{ sap_hana_install_sid | lower }}adm` is configured with a non-expiring password.</br>
Set to `false` to skip this step — typically done when the user is managed by a central identity provider (e.g. Active Directory or LDAP).

### sap_hana_install_new_system

- _Type:_ `bool`
- _Default:_ `True`

Set to `False` to use existing SAP HANA database and add more hosts using variable `sap_hana_install_addhosts`.</br>
Default is `True`, in which case fresh SAP HANA installation will be performed.

### sap_hana_install_addhosts

- _Type:_ `string`

If the following variable is specified, the role will perform a scaleout installation or it will add additional hosts to an existing SAP HANA system.</br>
Example: `sap_hana_install_addhosts: 'host2:role=worker,host3:role=worker:group=g02,host4:role=standby:group=g02',host5`.

### sap_hana_install_update_firewall

- _Type:_ `bool`
- _Default:_ `False`

The role can be configured to also set the required firewall ports for SAP HANA. If this is desired, set the variable `sap_hana_install_update_firewall` to `true` (default is `false`).</br>
The firewall ports are defined in a variable which is compatible with the variable structure used by Linux System Role `firewall`.</br>
The firewall ports for SAP HANA are defined in member `port` of the first field of variable `sap_hana_install_firewall` (`sap_hana_install_firewall[0].port`), see file `defaults/main.yml`.</br>
If the member `state` is set to `enabled`, the ports will be enabled. If the member `state` is set to `disabled`, the ports will be disabled, which might be useful for testing.</br>

Certain parameters have identical meanings, for supporting different naming schemes in playbooks and inventories.</br>
You can find those in the task `Rename some variables used by hdblcm configfile` of the file `tasks/main.yml`.</br>
Example: The parameter `sap_hana_install_number`, which is used by the role to define the hdblm parameter `number` (= SAP HANA instance number)</br>
 can be defined by setting `sap_hana_instance_number`, `sap_hana_install_instance_nr`, `sap_hana_install_instance_number`, or `sap_hana_install_number`.</br>
 The order of precedence is from left to right.
<!-- END Role Variables -->
