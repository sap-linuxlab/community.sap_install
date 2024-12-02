# sap_swpm Ansible Role DEVELOPER NOTES

## Common Errors

### Error - Missing signature files for installation media

```shell
INFO
DU at '/software_path/51052029_1/EXP1' is not signed.

WARNING
Data unit '/software_path/51052029_1/EXP1' is not signed.
DETAILS: The found data unit must not be used.
SOLUTION: Ensure that you use the latest available version of Installation Export 1 ECC 6.0 EhP8 downloaded from the SAP Support Portal and ensure that its content is unchanged.
Not accepted
```

After SWPM 1.0 SP22 and SAP SWPM 2.0 SP00, all SAP Software installation media requires a separate signature file (SIGNATURE.SMF). The signature file is missing in older installation media.

For example, IDES for SAP ECC 6.0 EhP8. See the following error message and SAP Note 2622019 - "EXPORT_1 is not signed" error during IDES installation.


### Error - NIECONN_REFUSED

```shell
FAIL: NIECONN_REFUSED
```

During SAP SWPM execution, it is common to see this **FALSE positive** error message. This is often due to restart of SAP NetWeaver AS in the installation procedures.

If this error occurs and SAP SWPM does not succeed, execute `sapcontrol -nr <Instance_Number> -function StartService <SAPSID>` to ensure that sapstartsrv is running and debug the underlying cause of the error; such as Network Port blocked, incorrect /etc/hosts file etc that is causing issues starting SAP NetWeaver AS.


### Error - Unprivileged users have permissions

```shell
Group of installation directory '/xxxxx/' is root, not sapinst.

Unprivileged users have permissions 'rx' instead of no permissions at all on directory 'xxxxx/'
```

During SAP SWPM execution, user group permissions on directories are verified.

If this error occurs, verify with `getent group` to ensure sapinst has more users than root; such as: `sapinst:x:<<NUMBER>>:root,<<SID>>adm`

To resolve, ensure the SWPM Unattended Parameter `nwUsers.sapsysGID` is set but remove any value from it. For example, in `sap_swpm` Ansible Role with default mode execution:
```yaml
sap_swpm_sapadm_uid: ""
sap_swpm_sapsys_gid: ""
sap_swpm_sidadm_uid: ""
```


### Error - No Profile used

```shell
sapparam(1c): No Profile used
```

During SAP SWPM execution, a target profile directory is created (auto-populated by the `sap_swpm` Ansible Role).

If this error occurs, it may cause additional errors such as `getProfileDir reported an error: Empty directory name is not allowed`.

To resolve, ensure the SWPM Unattended Parameter `NW_readProfileDir.profileDir` is set and has been provided a string path with the SAP System ID (e.g. `/sapmnt/<SID>/profile`). For example, in `sap_swpm` Ansible Role with default mode execution:
```yaml
sap_swpm_sid: "S01"
sap_swpm_inifile_list:
  - nw_config_other
  ...

```

Alternatively, use Shell environment variable named `SAPSYSTEMNAME=` when executing `./sapinst`.


### Error - Wrong password for SYSTEM user of the SYSTEMDB Tenant for SAP HANA MDC

```shell
NW_GetSidNoProfiles | NW_getDBInfo | NW_HDB_getDBInfo

Error code FCO-00011 and MUT-03025

The step getDBInfoMultiDbSystemDB reported an error:
The database connection with database user SYSTEM cannot be set up.
Check that the database is online and the password of user SYSTEM is correct.
```

During SAP SWPM execution, a connection to the SAP HANA MDC SystemDB Tenant is required.

To resolve, ensure the SWPM Unattended Parameter `NW_HDB_getDBInfo.systemDbPassword` is set and correct. For example, in `sap_swpm` Ansible Role with default mode execution:
```yaml
sap_swpm_db_systemdb_password: "Password"
```


### Error - Wrong password for SYSTEM user of the target SAP HANA MDC Tenant

```shell
NW_GetSidNoProfiles | NW_getDBInfo | NW_HDB_getDBInfo

Error code FCO-00011 and MUT-03025

The step getDBInfo reported an error:
The database connection with database user SYSTEM cannot be set up.
Check that the database is online and the password of user SYSTEM is correct.
```

During SAP SWPM execution, a connection to the SAP HANA MDC Tenant target and database schema (e.g. `SAPHANADB` or `SAPABAP1`) is required.

To resolve, ensure the SWPM Unattended Parameter `storageBasedCopy.hdb.systemPassword` and `NW_HDB_getDBInfo.systemPassword` is set and correct. For example, in `sap_swpm` Ansible Role with default mode execution:
```yaml
sap_swpm_db_system_password: "Password"
```

This may also occur after System Copy Database Backup Restore when the wrong password is given for SYSTEM user of the Database Schema (e.g. `SAPHANADB` or `SAPABAP1`). Such as the error below:

```Shell
NW_CreateDBandLoad | NW_CreateDB | NW_HDB_DB

The step RevalidateSystemuserPassword reported an error:
Start SAPinst in interactive mode to solve this problem.
```

To resolve, ensure the SWPM Unattended Parameter `HDB_Schema_Check_Dialogs.schemaPassword` is correctly set. For example, in `sap_swpm` Ansible Role with default mode execution:
```yaml
sap_swpm_db_system_password: "Password"
sap_swpm_db_schema_password: "Password"
```


### Error - Wrong password for SYSTEM user of Database Schema for the SAP HANA Backup file

```shell
NW_CreateDBandLoad | NW_CreateDB | NW_HDB_DB

The step RevalidateSchemauserPassword reported an error:
The database connection with database user SYSTEM cannot be set up.
Check that the database is online and the password of user SYSTEM is correct.
```

During SAP SWPM execution, when using a Database Backup File the SYSTEM user of the Database Schema within the backup (e.g. `SAPHANADB`, or `SAPABAP1`) is required.

To resolve, ensure the SWPM Unattended Parameter `NW_HDB_getDBInfo.systemPasswordBackup` value is the correct password. For example, in `sap_swpm` Ansible Role with default mode execution:
```yaml
sap_swpm_backup_system_password: "Password"
```


### Error - Wrong password for DDIC user of Database Schema for the SAP HANA Backup file

```shell
NW_CI_Instance | abapReports | NW_DDIC_Password

ERROR   (root/sapinst) id=rfcmod.jsco.wrongPassword
The step checkDDIC000Password was executed with status ERROR
The password you specified for user DDIC is wrong.
<p> SOLUTION: Enter the correct password. </p>
```

During SAP SWPM execution, when using a Database Backup File the DDIC user of the Database Schema within the backup (e.g. `SAPHANADB`, or `SAPABAP1`) is required after the data load occurs.

To resolve, ensure the SWPM Unattended Parameter `NW_DDIC_Password.ddic000Password` value is the correct password. For example, in `sap_swpm` Ansible Role with default mode execution:
```yaml
sap_swpm_ddic_000_password: "Password"
```


### Error - Wrong schema name for database connection set up

```shell
The database connection with database user SYSTEM cannot be set up.
Check that the database is online and the password of the user SYSTEM is correct
```

During SAP SWPM execution, when using a Database Backup File Database Schema name is required after the data load occurs.

To resolve, ensure the SWPM Unattended Parameter for the Database Schema (e.g. `HDB_Schema_Check_Dialogs.schemaName` for SAP HANA) is set and provided with the correct schema name (e.g. `SAPHANADB` , `SAPABAP1` based upon different SAP Software and versions). For example, in `sap_swpm` Ansible Role with default mode execution:
```yaml
sap_swpm_db_schema: "SAPABAP1"
```


### Error - Wrong domain name

```shell
NW_GetSidNoProfiles | NW_getFQDN

The step askFQDN reported an error:
Cannot resolve host 'xxxxxx' by name
```

During SAP SWPM execution, the FQDN is used for connections.

To resolve, ensure the SWPM Unattended Parameter `NW_getFQDN.FQDN` for the FQDN is correct. For example, in `sap_swpm` Ansible Role with default mode execution:
```yaml
sap_swpm_set_fqdn: true
sap_swpm_fqdn: "name.internal.corp"
```


### Error - Restricted file permissions for current working directory

```shell
NW_First_Steps | Preinstall

The step checkInstDirPermissions was executed with status ERROR
The installation directory /xxxxx is not owned by group <i>sapinst</i>.
<p> SOLUTION: SAPinst will set the appropriate permission on the directory if you choose <i>Ok</i>. </p>
```

During SAP SWPM execution, the current working directory should be `0755` permission.

This should be achieved automatically by the `sap_swpm` Ansible Role, whereby the variable `sap_swpm_sapinst_path: /path_here` is set to `0755` prior to execution of `sapinst`.


### Error - Incomplete parameters for Database Backup Restore and connection set up

```shell
NWCreateDBandLoad | hdb_recovery_dialogs

The step ask_recovery_connect_data_existing_database reported an error
```

During SAP SWPM execution, when using a Database Backup File additional variables are required for the data load.

To resolve, ensure the SWPM Unattended PArameters below are set:
```shell
HDB_Recovery_Dialogs.backupLocation = ""
HDB_Recovery_Dialogs.backupName = ""
HDB_Recovery_Dialogs.sapControlWsdlUrl = "http://HOST:PORT/SAPControl?wsdl"
HDB_Recovery_Dialogs.sidAdmName = ""
HDB_Recovery_Dialogs.sidAdmPassword = ""
```

For example, in `sap_swpm` Ansible Role with default mode execution:
```yaml
sap_swpm_backup_location: ""
sap_swpm_backup_prefix: ""
sap_swpm_db_host: ""
sap_swpm_db_instance_nr: ""
sap_swpm_db_sid: ""
sap_swpm_db_sidadm_password: ""
```


---


## SAP SWPM for SAP NWAS JAVA installations

There are two deployment methods executed for SAP SWPM for SAP NWAS JAVA, which uses two sequential executions:
- Method 1 ***(nw_java_import.buildJEEusingExtraMileTool = `false`)***:
  1. JLoad: <sub>`com.sap.engine.offline.OfflineToolStart com.sap.inst.jload.Jload`</sub>
  2. Deploy Controller Runner tool: <sub>`com.sap.engine.services.dc.api.cmd.Runner deploy`</sub>
- Method 2 ***(nw_java_import.buildJEEusingExtraMileTool = `true`)***:
  1. BatchDeployer (ExtraMile) Tool: <sub>`com.sap.engine.offline.OfflineToolStart com.sap.engine.extramile.BatchDeployer`</sub>
  2. Deploy Controller Runner tool: <sub>`com.sap.engine.services.dc.api.cmd.Runner deploy`</sub>

The BatchDeployer (ExtraMile) Tool for SAP NetWeaver JAVA notes (see SNote 1715441), has some restrictions:
- Core SCAs (e.g. SERVERCORE) are deployed sequentially in a specific order
- J2EEAPPS cannot be deployed with this tool
- Only for offline deployments, does not support online deployments


### SAP SWPM for SAP NWAS JAVA - JLoad with IMPORT.XML

**Example command:**
```shell
/tmp/sapinst_instdir/NW750/SYB/INSTALL/STD/sapjvm/sapjvm_8/bin/java \
-classpath \
/tmp/sapinst_instdir/NW750/SYB/INSTALL/STD/install/lib/sap.com~tc~bl~offline_launcher~impl.jar \
-Xmx2048m \
-XX:+HeapDumpOnOutOfMemoryError \
com.sap.engine.offline.OfflineToolStart com.sap.inst.jload.Jload \
-dataDir /software/sapnwas_java_export_extracted/DATA_UNITS/JAVA_EXPORT_JDMP \
-job /tmp/sapinst_instdir/NW750/SYB/INSTALL/STD/IMPORT.XML
```

**Example IMPORT.XML file (from JAVA_EXPORT_JDMP):**
```xml
<import file="EXPDUMP">
   <object name="BC_ACA_DC_DATA" type="T" action="create"/>
   <object name="BC_ACA_DC_DATA" action="insert"/>
   <object name="BC_SLM_USER" type="T" action="create"/>
   <object name="BC_SLM_USER" action="insert"/>
   <object name="J2EE_CONFIG" type="T" action="create"/>
   <object name="J2EE_CONFIG" action="insert"/>
   <object name="SR_SD" type="T" action="create"/>
   <object name="SR_SD" action="insert"/>
</import>
```


### SAP SWPM for SAP NWAS JAVA - BatchDeployer (ExtraMile) with list files

**Example command (run for each list file):**
```shell
/tmp/sapinst_instdir/NW750/SYB/INSTALL/STD/sapjvm/sapjvm_8/bin/java \
-classpath \
/tmp/sapinst_instdir/NW750/SYB/INSTALL/STD/install/lib/sap.com~tc~bl~offline_launcher~impl.jar \
-Xmx256m \
com.sap.engine.offline.OfflineToolStart com.sap.engine.extramile.BatchDeployer \
-pf /tmp/sapinst_instdir/NW750/SYB/INSTALL/STD/extramileconfig.properties \
-rd /software/sapnwas_java_export_extracted/DATA_UNITS/JAVA_J2EE_OSINDEP_UT \
-list /tmp/sapinst_instdir/NW750/SYB/INSTALL/STD/deployJDD.lst
# -list /tmp/sapinst_instdir/NW750/SYB/INSTALL/STD/deployFS.lst
# -list /tmp/sapinst_instdir/NW750/SYB/INSTALL/STD/deployOffline.lst
```

**Example deployJDD.lst file:**
```
BASETABLES22_0.SCA
```

**Example deployFS.lst file:**
```
CORETOOLS22_0.SCA
JSPM22_0.SCA
```

**Example deployOffline.lst file:**
```
J2EEFRMW22_0.SCA
CFGZACE22_0.SCA
SERVERCORE22_0.SCA
ENGINEAPI22_0.SCA
CFGZA22_0.SCA
```


### SAP SWPM for SAP NWAS JAVA - Deploy Controller Runner tool

The Deploy Controller Runner tool (deploycontroller) for the Java 'offline deployment' of SCA files will:

- import of various JAR files, including '-classpath /tmp/sapinst_instdir/NW750/xxx/INSTALL/STD/install/lib/`tc~je~cl_deploy.jar`' and many others
- with system property values '-Ddc.api.verbose=false'
- with JVM heap size as '-Xmx256m'
- and executing to the P4 Port using Java Class `com.sap.engine.services.dc.api.cmd.Runner` calling the function `deploy` and operator `-l` with deployment list file `/tmp/sapinst_instdir/NW750/xxx/INSTALL/STD/deploy.lst` and other function operators (e.g. `--port 5 *<java_ci_inst_no>* 04`)

> For further details, see /tmp/sapinst_instdir/NW750/xxx/INSTALL/STD/log/dc_log/deploy_api.0.log

**Example command:**
```shell
/tmp/sapinst_instdir/NW750/SYB/INSTALL/STD/sapjvm/sapjvm_8/bin/java \
-classpath \
/tmp/sapinst_instdir/NW750/SYB/INSTALL/STD/install/lib/tc~je~cl_deploy.jar:\
/tmp/sapinst_instdir/NW750/SYB/INSTALL/STD/j2eeclient/sap.com~tc~je~clientlib~impl.jar \
-Xmx256m \
-Ddc.api.verbose=false \
com.sap.engine.services.dc.api.cmd.Runner deploy \
-l /tmp/sapinst_instdir/NW750/SYB/INSTALL/STD/deploy.lst \
-e stop \
-u lower \
-w safety \
--lcm bulk \
-t 14400000 \
--host nw01 \
--port 52004
```

**Example deploy.lst files:**
```
/software/sapnwas_java_export_extracted/DATA_UNITS/JAVA_J2EE_OSINDEP_UT/SERVERCORE22_0.SCA
/software/sapnwas_java_export_extracted/DATA_UNITS/JAVA_J2EE_OSINDEP_UT/J2EEAPPS22_0.SCA
/software/sapnwas_java_export_extracted/DATA_UNITS/JAVA_J2EE_OSINDEP_UT/JSPM22_0.SCA
etc
```
```
/software/sap_solman_java_export_extracted/DATA_UNITS/SOLMAN72_JAVA_UT/LMSERVICE12_0.SCA
/software/sap_solman_java_export_extracted/DATA_UNITS/SOLMAN72_JAVA_UT/ADSSAP19_1.SCA
/software/sap_solman_java_export_extracted/DATA_UNITS/SOLMAN72_JAVA_UT/ISAGENTMINJ500_0.SCA
etc
```

#### Error with the Deploy Controller Runner tool

When setting inifile.params `nw_java_import.buildJEEusingExtraMileTool = false` an error will occur with the Deploy Controller Runner tool:

```log
[ LOG EXCEPTION ]  :: Exception while generating ID: [[ERROR CODE DPL.DC.3218] Deploy controller is not ready to serve yet. Probably a un/deploy operation after offline phase is in progress at the moment. DC state is Initialized]
com.sap.engine.services.dc.cm.DCNotAvailableException: [ERROR CODE DPL.DC.3218] Deploy controller is not ready to serve yet. Probably a un/deploy operation after offline phase is in progress at the moment. DC state is Initialized

[ Error ] Exception while generating ID: [[ERROR CODE DPL.DC.3218] Deploy controller is not ready to serve yet. Probably a un/deploy operation after offline phase is in progress at the moment. DC state is Initialized]

[ LOG EXCEPTION ]  :: com.sap.engine.services.dc.api.deploy.DeployException: [ERROR CODE DPL.DCAPI.1023] DCNotAvailableException.
Reason: [ERROR CODE DPL.DC.3218] Deploy controller is not ready to serve yet. Probably a un/deploy operation after offline phase is in progress at the moment. DC state is Initialized
Caused by: com.sap.engine.services.dc.cm.DCNotAvailableException: [ERROR CODE DPL.DC.3218] Deploy controller is not ready to serve yet. Probably a un/deploy operation after offline phase is in progress at the moment. DC state is Initialized

[ LOG EXCEPTION ]  :: java.lang.NullPointerException: while trying to get the length of a null array loaded from a local variable at slot 4

[ Error ]
104
Component:n/a
Status:Initial
Description:
DeployException: [ERROR CODE DPL.DCAPI.1023] DCNotAvailableException.
Reason: [ERROR CODE DPL.DC.3218] Deploy controller is not ready to serve yet. Probably a un/deploy operation after offline phase is in progress at the moment. DC state is Initialized
```
