
# Ansible Collection Playbooks

The playbooks starting with `sample-` in this directory can be used as examples for your own playbooksi and cannot be called directly from the commandline.
The other playbooks can be called directly with a prepared variable file or imported in your own playbooks or workflows.
The playbooks can run against localhost, all hosts or defined group.

## Usage of playbooks

### Prepare System for SAP HANA installation: `sap_hana_prepare_exec.yml`

This playbook runs against localhost and/or remote hosts.
You need to define the variable `sap_hana_group`to run this playbook against a particular group of hosts which is defined in your inventory.
If you do not define the parameter `sap_hana_group` the playbook will run against all hosts in the inventory unless limited with `-l hostname' or localhost if no inventory is defined.

To run this playbook you need to prepare a variable file with a minimum viable set of variables.

#### Example: 

Create a parameter file `my_vars.yml` with similar content:

```[yaml]
    # sap_playbook_parameter_confirm: false   # Set to true if you want to list parameters and confirm execution
    sap_domain: my.sap.domain
    sap_general_preconfigure_modify_etc_hosts: true
    sap_general_preconfigure_update: true
    sap_general_preconfigure_fail_if_reboot_required: false
    sap_hana_preconfigure_update: true
    sap_hana_preconfigure_fail_if_reboot_required: false
    sap_hana_preconfigure_reboot_ok: true
```

Create the file `my_inventory` similar to:

```[yaml]
[my_hanas]
hana1
hana2
```

Now you can run the playbook with

```[bash]
ansible-playbook community.sap_install.sap_hana_preconfigure_exec.yml -i my_inventory -e @my_vars.yml -e sap_hana_group=my_hanas
```

When you call this playbook against a remote host make sure the user can connect and assume root without a password or pass the following parameters if necessary

```[bash]
 -u <connection user>: User that establishes the ssh connection
 -k: asks for password or passphrase of the connection user, if required for ssh
 -K: asks for the privilege escalation password of the connection user to become root on the target host
```

You can also call the playbook inside another playbook with:

```
- name: Include HANA preparation from collection for group my_hanas
  ansible.builtin.import_playbook: community.sap_install.sap_hana_prepare_exec.yml
  vars:
    sap_hana_group: my_hanas
    # add other vars here, or define somewhere else
```

