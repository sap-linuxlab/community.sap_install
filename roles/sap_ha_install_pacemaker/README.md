# sap_ha_install_pacemaker Ansible Role

Ansible role for SAP Pacemaker Setup

## Scope

- **RedHat Enterprise Linux**
    - Tested on RHEL 8.2

- **Azure** 
    - Tested
    - Followed the steps based on the guide published in
        - [Azure Pacemaker Setup Guide](https://docs.microsoft.com/en-us/azure/virtual-machines/workloads/sap/high-availability-guide-rhel-pacemaker)

- **AWS**
    - Future plans

## Overview

### Execution Design
- Update to be able to run the sap_ha_install_pacemaker role once you need to run sap_ha_prepare_pacemaker first.

- This Ansible role is designed to be executed using an external handler such `Terraform` or a separate `bash` script
- Limitations of doing an SAP installation where scripts and Ansible playbooks have to be executed locally and not thru the usual `ansible command` -> `inventory of hosts` scenario

    Sample execution:

    ```bash
    ansible-playbook --connection=local --limit localhost -i "localhost," sap-pacemaker.yml -e "@input_file.yml"
    ```

- This role must be ran in 2 parts on both the `primary` / `node1` and the `secondary` / `node2`
- Tasks marked with `[A]` are executed for both `primary` / `node1` and `secondary` / `node2`
- Tasks marked with `[1]` are only executed for `primary` / `node1`
- Tasks marked with `[2]` are only executed for `secondary` / `node2`

### Sample Execution Steps

- Run 1 - part 1 - primary:
    ```bash
    ansible-playbook --connection=local --limit localhost -i "localhost," sap-pacemaker.yml -e "@input_file1.yml"
    ```
    ```yaml
    # input_file1.yml contents
    sap_ha_install_pacemaker_part: "1"
    sap_ha_install_pacemaker_role: "primary"
    <other variables>
    ```

- Run 2 - part 1 - secondary:
    ```bash
    ansible-playbook --connection=local --limit localhost -i "localhost," sap-pacemaker.yml -e "@input_file2.yml"
    ```
    ```yaml
    # input_file2.yml contents
    sap_ha_install_pacemaker_part: "1"
    sap_ha_install_pacemaker_role: "secondary"
    ```

- Run 3 - part 2 - primary:
    ```bash
    ansible-playbook --connection=local --limit localhost -i "localhost," sap-pacemaker.yml -e "@input_file3.yml"
    ```
    ```yaml
    # input_file3.yml contents
    sap_ha_install_pacemaker_part: "2"
    sap_ha_install_pacemaker_role: "primary"
    ```

- Run 4 - part 2 - secondary:
    ```bash
    ansible-playbook --connection=local --limit localhost -i "localhost," sap-pacemaker.yml -e "@input_file4.yml"
    ```
    ```yaml
    # input_file4.yml contents
    sap_ha_install_pacemaker_part: "2"
    sap_ha_install_pacemaker_role: "secondary"
    ```

## Variables / Inputs

### Inputs

| **Variable**                                  | **Info**                                  | **Default** | **Required** |
| :---                                          | :---                                      | :---        | :---         |
| sap_ha_install_pacemaker_type                            | Cloud type - `az` for Azure               | <none>      | yes          |
| sap_ha_install_pacemaker_part                            | `1` or `2                 `               | <none>      | yes          |
| sap_ha_install_pacemaker_role                            | `primary` or `secondary`                  | <none>      | yes          |
| sap_ha_install_pacemaker_cluster_name                    | Cluster name                              | <none>      | yes          |
| sap_ha_install_pacemaker_hacluster_password              | Cluster password                          | <none>      | yes          |
| sap_ha_install_pacemaker_node1_ip                        | IP address of the `primary` node          | <none>      | yes          |
| sap_ha_install_pacemaker_node1_hostname                  | Hostname of the `primary` node            | <none>      | yes          |
| sap_ha_install_pacemaker_node2_ip                        | IP address of the `secondary` node        | <none>      | yes          |
| sap_ha_install_pacemaker_node2_hostname                  | Hostname of the `secondary` node          | <none>      | yes          |
| sap_ha_install_pacemaker_fqdn                            | Fully qualified domain name               | <none>      | yes          |
| sap_ha_install_pacemaker_client_id                       | test                                      | <none>      | yes          |
| sap_ha_install_pacemaker_client_secret                   | test                                      | <none>      | yes          |
| sap_ha_install_pacemaker_resource_group                  | test                                      | <none>      | yes          |
| sap_ha_install_pacemaker_subscription_id                 | test                                      | <none>      | yes          |

### RedHat Subscription Manager Repos and Packages

General Pacemaker repo
```
sap_ha_install_pacemaker_rhsm_repos:
  - rhel-8-for-x86_64-highavailability-e4s-rpms
```

Pacemaker repos for `Azure`
```
sap_ha_install_pacemaker_rhsm_repos_az:
  - rhel-7-server-rpms
  - rhel-ha-for-rhel-7-server-rpms
  - rhel-sap-for-rhel-7-server-rpms
  - rhel-ha-for-rhel-7-server-eus-rpms
```

General Pacemaker packages
```
sap_ha_install_pacemaker_packages:
  - pcs
  - pacemaker
  - yum-utils
  - nfs-utils
  - resource-agents
  - resource-agents-sap
```

Pacemaker packages for `Azure`
```
sap_ha_install_pacemaker_packages_az:
  - fence-agents-azure-arm
  - nmap-ncat
```

## License

Apache license 2.0

## Author Information

IBM Lab for SAP Solutions, Red Hat for SAP Community of Practice, Jason Masipiquena, Sherard Guico, Markus Moster
