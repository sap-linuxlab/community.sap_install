
# Ansible Collection Playbooks

The playbooks in this directory can be used as templates for your own playbooks
(starting with sample-) and some can be called directly with interactive variable collection
or included in your own playbooks or workflows.

## Usage of playbooks

### Prepare System for SAP HANA installation (sap_hana_prepare.yml/sap_hana_prepare_exec.yml)

This playbook collects information for preparing an SAP system for an SAP HANA installation.
Run the following command:

```[bash]
ansible-playbook community.sap_install.sap_hana_preconfigure.yml
```

This playbook runs against localhost and/or remote hosts.
Remote hosts can be defined in an inventory file, or with -i on the commandline e.g. `-i inventoryfile` or `-i host1,host2,host3,` and execution can be limited with -l.
You need to confirm the hosts in the interactive dialog.
When you call this playbook against a remote host make sure the user can connect and assume root without a password or pass the following parameters if necessary

```[bash]
 -u <connection user>: User that establishes the ssh connection
 -k: asks for password or passphrase of the connection user, if required for ssh
 -K: asks for the privilige escalation password of the connection user to become root on the target host
```

If you want to embed this playbook or run a non-interactive version, you need to prepare an ansible inventory that contains a group for the hosts you want to install, e.g. my_hanas (see also <https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html>).

Create the file `my_inventory` similar to:

```[yaml]
[my_hanas]
hana1
hana2
```

Prepare a variable config file with the following parameters (adapt to your needs):
Create a parameter file `my_vars.yml` with similar content:

```[yaml]
    # sap_playbook_parameter_confirm: false 
    sap_hana_group: 'my_hanas'
    sap_domain: my.sap.domain
    sap_general_preconfigure_modify_etc_hosts: true
    sap_general_preconfigure_update: true
    sap_general_preconfigure_fail_if_reboot_required: false
    sap_hana_preconfigure_update: true
    sap_hana_preconfigure_fail_if_reboot_required: false
    sap_hana_preconfigure_reboot_ok: true
```

Now you can run the playbook non-interactively with

```[bash]
ansible-playbook community.sap_install.sap_hana_preconfigure_exec.yml -i my_inventory -e @my_vars.yml
```

NOTE: If you do not define the parameter `sap_hana_group` the playbook will run against all hosts in the inventory unless limited with `-l hostname' or localhost if no inventory is defined.
