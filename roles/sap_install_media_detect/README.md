<!-- BEGIN Title -->
# sap_install_media_detect Ansible Role
<!-- END Title -->
![Ansible Lint for sap_install_media_detect](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_install_media_detect.yml/badge.svg)

## Description
<!-- BEGIN Description -->
The Ansible Role `sap_install_media_detect` is used to detect and extract SAP installation media.

This role scans the source directory, classifies the files by their SAP file type, and extracts and sorts them into subdirectories.</br>
The `sapfile` utility decides which files are extracted, and the role parameters select which components are detected.

Detection of compatible installation media is available for a wide range of SAP applications, such as:

- SAP S/4HANA
- SAP BW/4HANA
- SAP ECC
- SAP Solution Manager
- SAP Web Dispatcher
- SAP Business Applications based upon SAP NetWeaver
- SAP HANA Database (SAR file only)
- Other SAP products based on SAP NetWeaver
<!-- END Description -->

<!-- BEGIN Dependencies -->
## Dependencies
- **Optional:** Installing the `ansible.posix` Ansible collection on the Ansible Control node will improve copy performance when the `sap_install_media_detect_target_directory` variable is used, on the first execution as well as on every re-execution.
<!-- END Dependencies -->

<!-- BEGIN Prerequisites -->
## Prerequisites
Managed nodes:

- A directory with SAP installation media is present and the variable `sap_install_media_detect_source_directory` is set.
  > Files can be downloaded using [community.sap_launchpad](https://github.com/sap-linuxlab/community.sap_launchpad) Ansible Collection.
<!-- END Prerequisites -->

## Execution
<!-- BEGIN Execution -->
This role covers the following scenarios, which are detected automatically from the state of the source and target directories.

| Scenario | Source directory | Target directory | Main directory | Result |
| :--- | :--- | :--- | :--- | :--- |
| **A** | writable | not defined | source directory | runs |
| **B** | writable | defined | target directory | runs |
| **C** | read only | defined | target directory | runs |
| **D** | read only | not defined | - | **fails** |

Scenario breakdown:

- **A** - All tasks are executed in the source directory.
- **B** - The installation media is copied from the source directory into the target directory, and all remaining tasks are executed there. The source directory is left unchanged.
- **C** - Same as **B**. The read-only source directory is only ever read from.
- **D** - The role fails immediately, because it cannot rename, extract or move anything in a read-only source directory. Set `sap_install_media_detect_target_directory` to a writable directory to turn this into scenario **C**.

> **NOTE:** The **main directory** is the directory where all the files reside before classification and organization.
<!-- END Execution -->

<!-- BEGIN Execution Recommended -->
### Recommended
It is recommended to execute this role together with other roles in this collection, in the following order:</br>
#### SAP HANA
1. [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure)
2. [sap_hana_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_preconfigure)
3. *`sap_install_media_detect`*
4. [sap_hana_install](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_install)
5. [sap_ha_install_hana_hsr](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_install_hana_hsr) - High Availability specific
6. [sap_ha_pacemaker_cluster](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_pacemaker_cluster) - High Availability specific

#### SAP NetWeaver
1. [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure)
2. [sap_netweaver_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_netweaver_preconfigure)
3. *`sap_install_media_detect`*
4. [sap_swpm](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_swpm)
5. [sap_ha_pacemaker_cluster](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_pacemaker_cluster) - High Availability specific
<!-- END Execution Recommended -->

### Execution Flow
<!-- BEGIN Execution Flow -->
Pre-task steps:

1. Assert and validate provided role variables.
2. Detect provided directories and set the path to the main directory.
3. Reset the subdirectories of the main directory.
4. Scan files available in the source directory.
5. Copy files to the target directory if `sap_install_media_detect_target_directory` was provided.
6. Deduplicate files depending on the `sap_install_media_detect_rename_target_file_exists` variable.
7. Scan files available in the main directory and categorize them using the `file` command.
8. Rename files without extension using categorization results from the previous step.
9. Deploy the `sapfile` utility to the managed node.
10. Ensure that programs for handling ZIP and RAR are installed, if required.
11. Ensure that `SAPCAR` is provided and executable, if required.
12. Execute the `sapfile` utility against the list of available files and process its results.
    - Components selected by the role variables are validated here, so a component whose installation media is missing fails before anything is extracted or moved into a subdirectory.

Organization steps:

13. Create directories in the main directory based on the results from the `sapfile` utility classification.
    - Permissions and ownership are applied based on the variables (e.g. `sap_install_media_detect_directory_owner`).
14. Execute commands to unarchive files marked for extraction by the `sapfile` utility classification.
15. Distribute files into subdirectories based on the results from the `sapfile` utility classification.
16. Locate all files in the SWPM basket subdirectory `sap_swpm_download_basket` and validate them against components selected by the role variables.
    - Example: Ensure that `igsexe_*.SAR` and `igshelper_*.SAR` files are present when `sap_install_media_detect_igs` is set to `true`.
17. Locate all files in the extraction subdirectories and validate them against components selected by the role variables.
    - Example: Ensure that `.*DATA_UNITS.*` directories are present when `sap_install_media_detect_export` is set to `sapecc`.

Post-task steps:

18. Remove the temporary directory created for the `sapfile` utility handling.
19. Disable the `EPEL` repository and remove its GPG key on Red Hat hosts, if it was configured by this role.
20. Set the variables for `sap_swpm`, `sap_hana_install` and `sap_anydb_install_oracle` Ansible roles from this collection.
    - This removes the need to define all variables for those roles and lets them be defined from the detection results instead.
21. Show a summary of the role execution with a detailed breakdown of all completed steps.
<!-- END Execution Flow -->

### Example
<!-- BEGIN Execution Example -->
Example playbook to extract SAP installation media for an SAP S/4HANA system.

```yaml
---
- name: Ansible Play for SAP S/4HANA system
  hosts: all
  become: true
  tasks:

    - name: Execute Ansible Role sap_install_media_detect
      ansible.builtin.include_role:
        name: community.sap_install.sap_install_media_detect
      vars:
        sap_install_media_detect_source_directory: '/software'
        sap_install_media_detect_swpm: true
        sap_install_media_detect_hostagent: true
        sap_install_media_detect_igs: true
        sap_install_media_detect_kernel: true
        sap_install_media_detect_kernel_db: 'saphana'
        sap_install_media_detect_db: 'saphana'
        sap_install_media_detect_db_client: 'saphana'
        sap_install_media_detect_export: 'saps4hana'
```

Example playbook to extract SAP installation media for an SAP HANA database located in the `/software_source/sap_hana_2_sps08` directory and prepare it in the `/software` directory.
> **NOTE:** This example shows scenario **C**, where the source directory on a shared filesystem can be used along with read-only permissions.

```yaml
---
- name: Ansible Play for SAP HANA database
  hosts: all
  become: true
  tasks:

    - name: Execute Ansible Role sap_install_media_detect
      ansible.builtin.include_role:
        name: community.sap_install.sap_install_media_detect
      vars:
        sap_install_media_detect_source_directory: '/software_source/sap_hana_2_sps08'
        sap_install_media_detect_target_directory: '/software'
        sap_install_media_detect_hostagent: true
        sap_install_media_detect_db: 'saphana'
```
<!-- END Execution Example -->

<!-- BEGIN Execution Summary -->
### Summary
Example of the role summary for a run of scenario **B** or **C** without a tag against SAP S/4HANA system files.

```bash
ok: [s02pas] =>
    msg: |-
        SAP Install Media Detect - Summary
        ==========================================================================
        Source directory: /software_source/sap_s4hana_2023 (Read Only)
        Main directory:   /software_target

        Reset of the main directory
          Files moved back out of subdirectories: 0
          Subdirectories of a previous run removed: 0

        Installation media
          Files found: 42
          Copied from the source directory into the main directory, which can already hold files of its own.
          Files without extension: 0
          File extension added: 0

        Archive handling
          RAR archives present: no
          SAP archives present: yes
          SAPCAR files used by sapfile utility: SAPCAR_1300-70007716.EXE

        Classification
          Components requested by the role parameters: db_client_saphana, db_saphana, export_saps4hana, hostagent, igs, kernel, kernel_db (any database), swpm
          Files classified: 42
          Files matching the requested components: 42
          Files not requested and therefore ignored: 0

        Organization of the installation media
          Archives extracted: 4
            ZIP archives: 0
            SAP archives: 4
            RAR archives: 0
          Extraction subdirectories: sap_hana_client_extracted, sap_hana_extracted
          Files moved into their component subdirectory: 39
          Files copied into every component subdirectory: 6
          Component subdirectories: sap_hana, sap_swpm, sap_swpm_download_basket

        Requested files per SAP file type
          sap_export_s4hana        30
              S4CORE108_INST_EXPORT_1.zip ... S4CORE108_INST_EXPORT_30.zip
          sap_hostagent            1    SAPHOSTAGENT67_67-80004822.SAR
          sap_igs                  2    igsexe_4-70005417.sar, igshelper_17-10010245.sar
          sap_kernel               1    SAPEXE_51-70007807.SAR
          sap_kernel_db_hdb        1    SAPEXEDB_51-70007806.SAR
          sap_s4hana_lang          1    S4HANAOP108_ERP_LANG_EN.SAR
          sap_swpm                 1    SWPM20SP23_1-80003424.SAR
          sapcar                   1    SAPCAR_1300-70007716.EXE
          saphana                  1    IMDB_SERVER20_079_8-80002031.SAR
          saphana_client           1    IMDB_CLIENT20_028_17-80002082.SAR
          saphana_other            2    IMDB_AFL20_079P_800-80001894.SAR, IMDB_LCAPPS_2079P_801-20010426.SAR
```

Example of the role summary for a run with the `sap_install_media_detect_reset` tag.

```bash
ok: [s02pas] =>
    msg: |-
        SAP Install Media Detect - Summary
        ==========================================================================
        Source directory: /software
        Main directory:   /software

        Reset of the main directory
          Files moved back out of subdirectories: 39
          Subdirectories of a previous run removed: 5
```
<!-- END Execution Summary -->

<!-- BEGIN Role Tags -->
### Role Tags
The role can be limited to a part of its workflow with the following tags. Each tag runs the workflow from the beginning up to a defined point, so a tag is never an entry point into the middle of the role. Running the role without a tag performs all steps.

| Tag | Runs | Writes to the main directory |
| :--- | :--- | :--- |
| `sap_install_media_detect_reset` | Validation, Detection and Reset | **Yes** |
| `sap_install_media_detect_prepare` | Validation, Detection, Scan and File types | No |
| `sap_install_media_detect_classify` | Preparation, `sapfile` utility, `SAPCAR` and Classification | Permissions of `SAPCAR` only |
| none | All steps | **Yes** |

Tag breakdown:

- `sap_install_media_detect_reset` - Moves the SAP archive files out of the subdirectories of a previous run back into the main directory and removes those subdirectories afterwards, so the installation media is in the same place as before the role was executed for the first time. Directories with the pattern `*_extracted` are removed as well, because they are recreated during extraction.
- `sap_install_media_detect_prepare` - Reports what the source directory holds without copying, renaming, moving or removing a single file. Programs for handling `ZIP` and `RAR` files are installed if the installation media requires them.
- `sap_install_media_detect_classify` - Adds the classification on top of the preparation, so the summary also reports which SAP file types the installation media holds. It only reads the installation media and completes in a fraction of the time of a full run.

> **NOTE:** The summary is shown for every run, including a run that is limited to a tag.
<!-- END Role Tags -->

<!-- BEGIN Further Information -->
## Further Information
For more examples on how to use this role in different installation scenarios, refer to the [ansible.playbooks_for_sap](https://github.com/sap-linuxlab/ansible.playbooks_for_sap) playbooks.

### Multiple files of the same component
The SAP IGS files and the SAP Maintenance Planner stack file resolve to the newest file when the installation media holds more than one of them, which is determined by the modification time.</br>
The SAP kernel and the SAP Web Dispatcher fail instead, because handing over the wrong file makes the later installation fail rather than this role.

> **NOTE:** The SAP kernel is checked on the number of files. The role does not compare versions, so it does not verify that the `SAPEXE` and the `SAPEXEDB` file belong to the same SAP kernel patch level.

### Variables set for other roles
The role hands the detection results over to the roles of this collection that consume the SAP installation media, so those variables do not have to be defined by hand. Only the variables of the detected components are set, and the role prints the ones it set at the end of its execution.

| Variable | Consuming role | Set when |
| :--- | :--- | :--- |
| `sap_hana_install_software_directory` | `sap_hana_install` | `sap_install_media_detect_db` is `saphana` |
| `sap_hana_install_software_extract_directory` | `sap_hana_install` | `sap_install_media_detect_db` is `saphana` and `sap_install_media_detect_extract_archives` is `true` |
| `sap_anydb_install_oracle_extract_path` | `sap_anydb_install_oracle` | An Oracle database is detected |
| `sap_swpm_software_path` | `sap_swpm` | Always |
| `sap_swpm_path` | `sap_swpm` | `sap_install_media_detect_swpm` is `true` |
| `sap_swpm_sapcar_path` | `sap_swpm` | `SAPCAR` is detected |
| `sap_swpm_sapcar_file_name` | `sap_swpm` | `SAPCAR` is detected |
| `sap_swpm_cd_rdbms_path` | `sap_swpm` | An SAP HANA client is detected |
| `sap_swpm_cd_sapase_path` | `sap_swpm` | An SAP ASE database is detected |
| `sap_swpm_cd_sapase_client_path` | `sap_swpm` | An SAP ASE client is detected |
| `sap_swpm_cd_sapmaxdb_path` | `sap_swpm` | An SAP MaxDB database is detected |
| `sap_swpm_cd_ibmdb2_path` | `sap_swpm` | An IBM Db2 database is detected |
| `sap_swpm_cd_ibmdb2_client_path` | `sap_swpm` | An IBM Db2 client is detected |
| `sap_swpm_cd_oracle_path` | `sap_swpm` | An Oracle database is detected |
| `sap_swpm_cd_oracle_client_path` | `sap_swpm` | An Oracle client is detected |
| `sap_swpm_cd_export_path` | `sap_swpm` | An installation export is detected |
| `sap_swpm_cd_export_pt1_path` | `sap_swpm` | The SAP ECC IDES or the SAP Solution Manager ABAP export is detected |
| `sap_swpm_cd_export_pt2_path` | `sap_swpm` | The SAP ECC IDES or the SAP Solution Manager ABAP export is detected |
| `sap_swpm_mp_stack_path` | `sap_swpm` | `sap_install_media_detect_mpstack` is `true` |
| `sap_swpm_mp_stack_file_name` | `sap_swpm` | `sap_install_media_detect_mpstack` is `true` |

> **NOTE:** The SAP kernel, the SAP IGS and the SAP Web Dispatcher are not handed over through a variable. They are placed in the directory of `sap_swpm_software_path`, where the `sap_swpm` role picks them up.
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
### sap_install_media_detect_source_directory

- _Type:_ `str`
- _Default:_ `/software`

Path to the directory that holds the SAP installation media.

### sap_install_media_detect_target_directory

- _Type:_ `str`

Path to the directory into which the SAP installation media is copied and where it is prepared.</br>
Use it only if the installation media should be prepared in a different directory than `sap_install_media_detect_source_directory`, which is required when the source directory is read only.</br>
See the scenarios in the [Execution](#execution) section.

### sap_install_media_detect_create_target_directory

- _Type:_ `bool`
- _Default:_ `True`

Create the target directory if it does not yet exist. If set to `false`, the role only checks that the directory is present.

### sap_install_media_detect_extract_archives

- _Type:_ `bool`
- _Default:_ `True`

Extract the archives of the SAP installation media. Set to `false` if the archives should not be extracted.

### sap_install_media_detect_move_or_copy_archives

- _Type:_ `bool`
- _Default:_ `True`

Move or copy the SAP installation media into the component subdirectories.</br>
Set to `false` if all files should stay in one directory.

### sap_install_media_detect_rename_target_file_exists

- _Type:_ `str`
- _Default:_ `skip`

Behavior when a file without a file name extension is renamed and a file of the new name already exists:</br>
- `skip` - The renaming is skipped and the existing file is used instead.
- `fail` - The role fails.
- `overwrite` - The existing file is removed and replaced by the renamed file.

The name is matched case insensitively, so both `file.SAR` and `file.sar` are an existing file for the new name `file.SAR`.</br>
> **NOTE:** When a target directory is used and the source directory holds the same installation media once with and once without its file extension, `overwrite` removes the renamed file and copies both source files again on every run.
> Remove the duplicate from the source directory to avoid that.

### sap_install_media_detect_sapcar_path

- _Type:_ `str`

(Optional) Fully qualified path to the `SAPCAR` program.</br>
If it is not defined, the role uses the `SAPCAR*.EXE` file of the SAP installation media.</br>
> **NOTE:** Ensure that `SAPCAR` is compatible with the CPU architecture of the managed node.

### sap_install_media_detect_db

- _Type:_ `str`

Select which database type to detect.</br>
Available values: `saphana`, `sapase`, `sapmaxdb`, `oracledb`, `ibmdb2`

### sap_install_media_detect_db_client

- _Type:_ `str`

Select which database client to detect.</br>
Available values: `saphana`, `sapase`, `sapmaxdb`, `oracledb`, `ibmdb2`

### sap_install_media_detect_kernel

- _Type:_ `bool`
- _Default:_ `False`

Enable to detect the SAP kernel files, which are the database independent `SAPEXE` and the database dependent `SAPEXEDB`.

### sap_install_media_detect_kernel_db

- _Type:_ `str`

Select which database the database dependent SAP kernel (`SAPEXEDB`) belongs to.</br>
Available values: `saphana`, `sapase`, `sapmaxdb`, `oracledb`, `ibmdb2`</br>
Only used together with `sap_install_media_detect_kernel` set to `true`, and only necessary if the SAP installation media holds more than one `SAPEXEDB` file.

### sap_install_media_detect_export

- _Type:_ `str`

Select which installation export to detect.</br>
Available values: `saps4hana`, `sapbw4hana`, `sapecc`, `sapecc_ides`, `sapnwas_abap`, `sapnwas_java`, `sapsolman_abap`, `sapsolman_java`

### sap_install_media_detect_swpm

- _Type:_ `bool`
- _Default:_ `False`

Enable to detect the SAP Software Provisioning Manager (SWPM) files.

### sap_install_media_detect_hostagent

- _Type:_ `bool`
- _Default:_ `False`

Enable to detect the SAP Host Agent files.

### sap_install_media_detect_igs

- _Type:_ `bool`
- _Default:_ `False`

Enable to detect the SAP IGS files, which are the IGS program and its helper.

### sap_install_media_detect_webdisp

- _Type:_ `bool`
- _Default:_ `False`

Enable to detect the SAP Web Dispatcher files.

### sap_install_media_detect_mpstack

- _Type:_ `bool`
- _Default:_ `False`

Enable to detect the SAP Maintenance Planner stack file.

### sap_install_media_detect_rar_handling

- _Type:_ `bool`
- _Default:_ `True`

Handle RAR files. Set to `false` to skip the handling of RAR files, in which case no program for listing and extracting them is installed.

### sap_install_media_detect_rar_use_unar

- _Type:_ `bool`
- _Default:_ `True`

Use the `unar` package, which the role installs, for handling RAR files.</br>
Set to `false` to use another program instead, which is then defined by `sap_install_media_detect_rar_list`, `sap_install_media_detect_rar_extract` and `sap_install_media_detect_rar_extract_directory_argument`.</br>
Operating system specific behavior:
- Red Hat: This also enables the `EPEL` and `CRB` repositories. `EPEL` is disabled again at the end of the role, if the role enabled it.
- SUSE: The package comes from the Basesystem module, which has to be enabled beforehand.

### sap_install_media_detect_epel_gpg_key_url

- _Type:_ `str`
- _Default:_ `https://download.fedoraproject.org/pub/epel/RPM-GPG-KEY-EPEL-{{ ansible_facts['distribution_major_version'] }}`

(Red Hat specific) URL of the `EPEL` GPG key, used when `sap_install_media_detect_rar_use_unar` is set to `true`.</br>
The key is imported with the `rpm_key` module, which requires the URL to be specified.

### sap_install_media_detect_use_rpm_key_module_for_removing_the_key

- _Type:_ `bool`
- _Default:_ `True`

(Red Hat specific) Remove the `EPEL` GPG key with the `rpm_key` module and the URL of the key.</br>
Set to `false` to use the `rpm -e` command instead.

### sap_install_media_detect_rar_list

- _Type:_ `str`

Fully qualified path to the program that lists the contents of a RAR file, including the argument that makes it list.</br>
The role appends the path of the RAR file, so the value has to end with that argument. Example for `unrar`: `/usr/bin/unrar lb`</br>
Only used when `sap_install_media_detect_rar_use_unar` is set to `false`. The role does not install this program, it only executes it.

### sap_install_media_detect_rar_extract

- _Type:_ `str`

Fully qualified path to the program that extracts a RAR file, including the argument that makes it extract.</br>
The role appends the path of the RAR file, so the value has to end with that argument. Example for `unrar`: `/usr/bin/unrar x`</br>
Only used when `sap_install_media_detect_rar_use_unar` is set to `false`. The role does not install this program, it only executes it.

### sap_install_media_detect_rar_extract_directory_argument

- _Type:_ `str`

Argument of the extraction program that specifies the directory to extract into.</br>
The role appends this argument and then the directory, so the value has to start with a space character.</br>
Set it to an empty string if the program takes the directory as a bare argument, which is the case for `unrar`.</br>
Only used when `sap_install_media_detect_rar_use_unar` is set to `false`.

### sap_install_media_detect_directory_owner

- _Type:_ `str`
- _Default:_ `root`

Owner of the component subdirectories created by this role.

### sap_install_media_detect_directory_group

- _Type:_ `str`
- _Default:_ `root`

Group of the component subdirectories created by this role.

### sap_install_media_detect_directory_mode

- _Type:_ `str`
- _Default:_ `0755`

Permissions of the component subdirectories created by this role.</br>
> **NOTE:** The value has to be a quoted octal string, because an unquoted `0755` is read as a decimal number.

### sap_install_media_detect_files_owner

- _Type:_ `str`
- _Default:_ `root`

Owner of the SAP installation media files.

### sap_install_media_detect_files_group

- _Type:_ `str`
- _Default:_ `root`

Group of the SAP installation media files.

### sap_install_media_detect_files_mode

- _Type:_ `str`
- _Default:_ `0644`

Permissions of the SAP installation media files.</br>
> **NOTE:** The value has to be a quoted octal string, because an unquoted `0644` is read as a decimal number.

### sap_install_media_detect_sapcar_owner

- _Type:_ `str`
- _Default:_ `root`

Owner of the `SAPCAR` program.

### sap_install_media_detect_sapcar_group

- _Type:_ `str`
- _Default:_ `root`

Group of the `SAPCAR` program.

### sap_install_media_detect_sapcar_mode

- _Type:_ `str`
- _Default:_ `0755`

Permissions of the `SAPCAR` program.</br>
The value has to keep the program executable, because the roles that consume the SAP installation media call it to extract the SAP archives.</br>
> **NOTE:** The value has to be a quoted octal string, because an unquoted `0755` is read as a decimal number.
<!-- END Role Variables -->