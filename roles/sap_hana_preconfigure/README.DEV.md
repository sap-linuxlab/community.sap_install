# Developer Guide Lines

## Directory Structure

```
.
├── defaults
│   └── main.yml
├── example.yml
├── files
│   └── etc
│       └── tmpfiles.d
│           └── sap.conf
├── handlers
│   └── main.yml
├── LICENSE
├── meta
│   └── main.yml
├── README.DEV.md
├── README.md
├── tasks
│   ├── configuration.yml
│   ├── installation.yml
│   ├── main.yml
│   ├── RedHat6
│   │   └── recommendations.yml
│   ├── RedHat7
│   │   └── recommendations.yml
│   └── sapnotes
│       ├── 2009879_7.yml
│       ├── 2009879.yml
│       ├── 2013638.yml
│       ├── 2055470.yml
│       ├── 2136965.yml
│       ├── 2235581.yml
│       ├── 2247020.yml
│       ├── 2292690.yml
│       ├── 2382421.yml
│       └── 2455582.yml
└── vars
    ├── main.yml
    ├── RedHat_6.5.yml
    ├── RedHat_6.6.yml
    ├── RedHat_6.7.yml
    └── RedHat_7.yml

11 directories, 28 files
```

The deployment of this role follows the style guide from Adfinis Sygroup. [Click Here](https://docs.adfinis-sygroup.ch/public/ansible-guide/styling_guide.html) for more info

## Where/How to make change/additions

All required packages are installed by installation.yml, all configuration required in SAP Notes is done by configuration.yml.

The configuration is then done and commented in the sapnotes subdirectory.
If you want to add content from a particular SAP note, e.g. for certain hardware vendor, please make your changes in `vars/OS_Release.yml`

- Add the packages required by a sapnote to the packages section and make a comment to which SAP Note it belongs
- add the sapnote number to the the sapnotes list
- Add the configuration that needs to be done to a separate file in the sapnotes subdirectory with the name of the SAP Note.
- If you figure out certain requirements that are not documented in a SAP note but mentioned in knowledge base articles or other sources, add them with a proper comment to `OS_release/recommendations.yml`
