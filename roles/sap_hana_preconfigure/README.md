<!-- BEGIN Title -->
# sap_hana_preconfigure Ansible Role
<!-- END Title -->
![Ansible Lint for sap_hana_preconfigure](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_hana_preconfigure.yml/badge.svg)

## Description
<!-- BEGIN Description -->
Ansible Role `sap_hana_preconfigure` is used to ensure that Managed nodes are configured to host SAP HANA systems according to SAP Notes after [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure) role was executed.

This role performs installation of required packages for running SAP HANA systems and configuration of Operating system parameters.
<!-- END Description -->

<!-- BEGIN Dependencies -->
## Dependencies
- `fedora.linux_system_roles`
    - Roles:
        - `selinux`

Install required collections by `ansible-galaxy install -vv -r meta/collection-requirements.yml`.
<!-- END Dependencies -->

<!-- BEGIN Prerequisites -->
## Prerequisites
Managed nodes:
- Ensure that general operating system configuration for SAP is performed by [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure). See [Recommended](#recommended) section.

<details>
  <summary><b>(Red Hat) Ensure required repositories are available</b></summary>

  Managed nodes need to be properly registered to a repository source and have at least the following Red Hat repositories accessible:

  for RHEL 7.x:
  - rhel-7-[server|for-power-le]-e4s-rpms
  - rhel-sap-hana-for-rhel-7-[server|for-power-le]-e4s-rpms

  for RHEL 8.x:
  - rhel-8-for-[x86_64|ppc64le]-baseos-e4s-rpms
  - rhel-8-for-[x86_64|ppc64le]-appstream-e4s-rpms
  - rhel-8-for-[x86_64|ppc64le]-sap-solutions-e4s-rpms

  for RHEL 9.x:
  - rhel-9-for-[x86_64|ppc64le]-baseos-e4s-rpms
  - rhel-9-for-[x86_64|ppc64le]-appstream-e4s-rpms
  - rhel-9-for-[x86_64|ppc64le]-sap-solutions-e4s-rpms

  For details on configuring Red Hat, see the knowledge base article: [How to subscribe SAP HANA systems to the Update Services for SAP Solutions](https://access.redhat.com/solutions/3075991)). If you set role parameter sap_hana_preconfigure_enable_sap_hana_repos to `yes`, the role can enable these repos.

  To install HANA on Red Hat Enterprise Linux 7, 8, or 9, you need some additional packages which are contained in one of following repositories
  - rhel-sap-hana-for-rhel-7-[server|for-power-le]-e4s-rpms
  - rhel-8-for-[x86_64|ppc64le]-sap-solutions-e4s-rpms
  - rhel-9-for-[x86_64|ppc64le]-sap-solutions-e4s-rpms

  To get this repository you need to have one of the following products:
  - [RHEL for SAP Solutions](https://access.redhat.com/solutions/3082481) (premium, standard)
  - RHEL for Business Partner NFRs
  - [RHEL Developer Subscription](https://developers.redhat.com/products/sap/download/)

  To get a personal developer edition of RHEL for SAP solutions, please register as a developer and download the developer edition.

  - [Registration Link](http://developers.redhat.com/register) :
    Here you can either register a new personal account or link it to an already existing
    **personal** Red Hat Network account.
  - [Download Link](https://access.redhat.com/downloads/content/69/ver=/rhel---7/7.2/x86_64/product-software):
    Here you can download the Installation DVD for RHEL with your previously registered
    account

  *NOTE:* This is a regular RHEL installation DVD as RHEL for SAP Solutions is no additional
  product but only a special bundling. The subscription grants you access to the additional
  packages through our content delivery network (CDN) after installation.

  For supported RHEL releases [click here](https://access.redhat.com/solutions/2479121).

  It is also important that your disks are setup according to the [SAP storage requirements for SAP HANA](https://www.sap.com/documents/2015/03/74cdb554-5a7c-0010-8F2c7-eda71af511fa.html). This [BLOG](https://blogs.sap.com/2017/03/07/the-ultimate-guide-to-effective-sizing-of-sap-hana/) is also quite helpful when sizing HANA systems.
  You can use the [storage](https://galaxy.ansible.com/linux-system-roles/storage) role to automate this process

  If you want to use this system in production, make sure that the time service is configured correctly. You can use [rhel-system-roles](https://access.redhat.com/articles/3050101) to automate this.

  Note
  ----
  For finding out which SAP notes will be used by this role for Red Hat systems, please check the contents of variable `__sap_hana_preconfigure_sapnotes` in files `vars/*.yml` (choose the file which matches your OS distribution and version). 
</details>
<!-- END Prerequisites -->

## Execution
<!-- BEGIN Execution -->
**:warning: Do not execute this Ansible Role against existing SAP systems unless you know what you are doing and you prepare inputs to avoid unintended changes caused by default inputs.**

**NOTE: It is recommended to execute `timesync` role from Ansible Collection `fedora.linux_system_roles` before or after executing this role.**

Role can be executed independently or as part of [ansible.playbooks_for_sap](https://github.com/sap-linuxlab/ansible.playbooks_for_sap) playbooks.
<!-- END Execution -->

<!-- BEGIN Execution Recommended -->
### Recommended
It is recommended to execute this role together with other roles in this collection, in the following order:</br>
1. [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure)
2. *`sap_hana_preconfigure`*
<!-- END Execution Recommended -->

### Execution Flow
<!-- BEGIN Execution Flow -->
1. Assert that required inputs were provided.
2. Install required packages and patch system if `sap_hana_preconfigure_update:true`
3. Apply configurations
  - Execute configuration tasks based on SAP Notes
  - (SUSE) Execute saptune with solution `sap_hana_preconfigure_saptune_solution` (Default: `HANA`)
4. Reboot Managed nodes if packages were installed or patched and `sap_hana_preconfigure_reboot_ok: true`
<!-- END Execution Flow -->

### Example
<!-- BEGIN Execution Example -->
Example of execution together with prerequisite role [sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_general_preconfigure)
```yaml
---
- name: Ansible Play for SAP HANA HA Scale-up preconfigure
  hosts: hana_primary, hana_secondary
  become: true
  tasks:
    - name: Execute Ansible Role sap_general_preconfigure
      ansible.builtin.include_role:
        name: community.sap_install.sap_general_preconfigure

    - name: Execute Ansible Role sap_hana_preconfigure
      ansible.builtin.include_role:
        name: community.sap_install.sap_hana_preconfigure
```
<!-- END Execution Example -->

<!-- BEGIN Role Tags -->
<!-- END Role Tags -->

<!-- BEGIN Further Information -->
<!-- END Further Information -->

## License
<!-- BEGIN License -->
Apache 2.0
<!-- END License -->

## Maintainers
<!-- BEGIN Maintainers -->
- [Bernd Finger](https://github.com/berndfinger)
<!-- END Maintainers -->

## Role Input Parameters
All input parameters used by role are described in [INPUT_PARAMETERS.md](https://github.com/sap-linuxlab/community.sap_install/blob/main/roles/sap_hana_preconfigure/INPUT_PARAMETERS.md)
