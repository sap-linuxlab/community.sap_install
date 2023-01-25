# sap_swpm Ansible Role DEVELOPER NOTES

## Errors with missing signature files for installation media

After SWPM 1.0 SP22 and SAP SWPM 2.0 SP00, all SAP Software installation media requires a seperate signature file (SIGNATURE.SMF). The signature file is missing in older installation media.

For example, IDES for SAP ECC 6.0 EhP8. See the following error message and SAP Note 2622019 - "EXPORT_1 is not signed" error during IDES installation.
```shell
INFO
DU at '/software_path/51052029_1/EXP1' is not signed.

WARNING
Data unit '/software_path/51052029_1/EXP1' is not signed.
DETAILS: The found data unit must not be used.
SOLUTION: Ensure that you use the latest available version of Installation Export 1 ECC 6.0 EhP8 downloaded from the SAP Support Portal and ensure that its content is unchanged.
Not accepted
```


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
