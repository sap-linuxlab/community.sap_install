<!-- BEGIN Title -->
# sap_general_preconfigure Ansible Role
<!-- END Title -->
![Ansible Lint for sap_general_preconfigure](https://github.com/sap-linuxlab/community.sap_install/actions/workflows/ansible-lint-sap_general_preconfigure.yml/badge.svg)

## Description
<!-- BEGIN Description -->
Ansible Role `sap_general_preconfigure` is used to ensure that Managed nodes are configured to host SAP systems according to SAP Notes.

This role performs installation of required packages for running SAP systems and configuration of Operating system parameters.

This is general preconfigure role that used for both SAP Netweaver and SAP HANA, which have separate follow-up roles [sap_hana_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_preconfigure) and [sap_netweaver_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_netweaver_preconfigure).
<!-- END Description -->

<!-- BEGIN Dependencies -->
## Dependencies
- `fedora.linux_system_roles`
    - Roles:
        - `selinux`
- `community.sap_install` (This collection)
    - Roles:
        - `sap_maintain_etc_hosts`

Install required collections by `ansible-galaxy install -vv -r meta/collection-requirements.yml`.
<!-- END Dependencies -->

<!-- BEGIN Prerequisites -->
## Prerequisites

(Red Hat specific) Ensure system is installed according to:
- RHEL 7: SAP note 2002167, Red Hat Enterprise Linux 7.x: Installation and Upgrade, section `Installing Red Hat Enterprise Linux 7`.
- RHEL 8: SAP note 2772999, Red Hat Enterprise Linux 8.x: Installation and Configuration, section `Installing Red Hat Enterprise Linux 8`.
- RHEL 9: SAP note 3108316, Red Hat Enterprise Linux 9.x: Installation and Configuration, section `Installing Red Hat Enterprise Linux 9`.

<!-- END Prerequisites -->

## Execution
<!-- BEGIN Execution -->
**:warning: Do not execute this Ansible Role against existing SAP systems unless you know what you are doing and you prepare inputs to avoid unintended changes caused by default inputs.**

Role can be executed independently or as part of [ansible.playbooks_for_sap](https://github.com/sap-linuxlab/ansible.playbooks_for_sap) playbooks.
<!-- END Execution -->

<!-- BEGIN Execution Recommended -->
<!-- END Execution Recommended -->

### Execution Flow
<!-- BEGIN Execution Flow -->
1. Assert that required inputs were provided.
2. Install required packages and patch system if `sap_general_preconfigure_update:true`
3. Apply configurations based on SAP Notes
4. Reboot Managed nodes if packages were installed or patched and `sap_general_preconfigure_reboot_ok: true`
<!-- END Execution Flow -->

### Example
<!-- BEGIN Execution Example -->
```yaml
---
- name: Ansible Play for SAP HANA HA Scale-up preconfigure
  hosts: hana_primary, hana_secondary
  become: true
  tasks:
    - name: Execute Ansible Role sap_general_preconfigure
      ansible.builtin.include_role:
        name: community.sap_install.sap_general_preconfigure
```
Further referenced as `example.yml`
<!-- END Execution Example -->

<!-- BEGIN Role Tags -->
### Role Tags
With the following tags, the role can be called to perform certain activities only:
- tag `sap_general_preconfigure_installation`: Perform only the installation tasks
- tag `sap_general_preconfigure_configuration`: Perform only the configuration tasks
- tag `sap_general_preconfigure_3108316`: Perform only the tasks(s) related to this SAP note.
- tag `sap_general_preconfigure_2772999_03`: Perform only the tasks(s) related to step 3 of the SAP note.
- tag `sap_general_preconfigure_etc_hosts`: Perform only the tasks(s) related to this step. This step might be one of multiple
  configuration activities of a SAP note. Also this step might be valid for multiple RHEL major releases.

<details>
  <summary><b>How to run sap_general_preconfigure with tags</b></summary>

  #### Perform only installation tasks:
  ```console
  ansible-playbook sap.yml --tags=sap_general_preconfigure_installation
  ```

  #### Perform only configuration tasks:
  ```console
  ansible-playbook sap.yml --tags=sap_general_preconfigure_configuration
  ```

  #### Verify and modify /etc/hosts file:
  ```console
  ansible-playbook sap.yml --tags=sap_general_preconfigure_etc_hosts
  ```

  #### Perform all configuration steps except verifying and modifying the /etc/hosts file
  ```
  ansible-playbook sap.yml --tags=sap_general_preconfigure_configuration --skip_tags=sap_general_preconfigure_etc_hosts
  ```

  #### (Red Hat) Perform configuration activities related to SAP note 3108316 (RHEL 9)
  ```
  ansible-playbook sap.yml --tags=sap_general_preconfigure_3108316
  ```

  #### (Red Hat) Perform configuration activities related to step 2 (SELinux settings) of SAP note 3108316 (RHEL 9)
  ```
  ansible-playbook sap.yml --tags=sap_general_preconfigure_3108316_02
  ```

  #### (Red Hat) Perform all configuration activities except those related to step 2 (SELinux settings) of SAP note 3108316 (RHEL 9 specific)
  ```
  ansible-playbook sap-general-preconfigure.yml --tags=sap_general_preconfigure_configuration --skip_tags=sap_general_preconfigure_3108316_02
  ```
</details>
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
All input parameters used by role are described in [INPUT_PARAMETERS.md](https://github.com/sap-linuxlab/community.sap_install/blob/main/roles/sap_general_preconfigure/INPUT_PARAMETERS.md)

### Controlling execution with input parameters
Extended Check (assert) run, aborting for any error which has been found:
```yaml
ansible-playbook sap.yml -l remote_host -e "{sap_general_preconfigure_assert: yes}"
```

Extended Check (assert) run, not aborting even if an error has been found:
```yaml
ansible-playbook sap.yml -l remote_host -e "{sap_general_preconfigure_assert: yes,sap_general_preconfigure_assert_ignore_errors: no}"
```
