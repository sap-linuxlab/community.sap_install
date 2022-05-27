
# Developer Guide Lines

## Directory Structure

```
tree command output tbd
```

The deployment of this role follows the style guide from Adfinis Sygroup. [Click Here](https://docs.adfinis-sygroup.ch/public/ansible-guide/styling_guide.html) for more info

## Where/How to make change/additions

The following documentention is taking into account

[SAP NOTE 2130510](https://launchpad.support.sap.com/#/notes/2130510) - SAP Host Agent 7.21
The Software comes as part of an installation bundle and can be downloaded as sapcar or rpm. RedHat recommends rpm as it is the easiest way to upgrade.
According to SAP Note the command is: saphostexec -upgrade

[SAP NOTE 1907566](https://launchpad.support.sap.com/#/notes/1907566) - Accessing the Latest SAP Host Agent Documentation

### Algorithm

- make sure user sapdm, group sapsys exists
- get the current installed version
- get the installable Version
- install/upgrade if required

### Important Steps from the documention:

 - requires root
 - Optional Paramter: `-pf <ProfilePath>` defaults to /usr/sap/exe

1. Install Host agent (from unpacked directory)
```
/usr/sap/hostctrl/exe/saphostexec -install -verify
```

2. Upgrade hostagent
```
/usr/sap/hostctrl/exe/hostexecstart -upgrade <path to new version.sar>
/usr/sap/hostctrl/exe/saphostexec -upgrade -verify -archive  <path to new version.sar>
```

3.  Version Information
```
/usr/sap/hostctrl/exe/saphostexec -version
```

4. function test
```
```
