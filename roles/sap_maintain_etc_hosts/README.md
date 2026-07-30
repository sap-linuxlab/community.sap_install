<!-- BEGIN Title -->
# sap_maintain_etc_hosts Ansible Role
<!-- END Title -->

## Description
<!-- BEGIN Description -->
The Ansible role `sap_maintain_etc_hosts` is used to maintain the `/etc/hosts` file.
<!-- END Description -->

<!-- BEGIN Dependencies -->
<!-- END Dependencies -->

<!-- BEGIN Prerequisites -->
<!-- END Prerequisites -->

## Execution
<!-- BEGIN Execution -->
<!-- END Execution -->

<!-- BEGIN Execution Recommended -->
<!-- END Execution Recommended -->

### Execution Flow
<!-- BEGIN Execution Flow -->
1. Assert and validate input variables.
2. Verify duplicate entries and conflicts.
3. Update `/etc/hosts` file.
<!-- END Execution Flow -->

### Example
<!-- BEGIN Execution Example -->
The example playbook will update `/etc/hosts`:

- Remove node with IP `10.10.10.10`.
- Remove node with name `host2`.
- Add node with IP `10.10.10.11`, name `host1`, aliases `alias1, alias2` and comment `host1 comment`.
```yaml
- name: Ansible Play to manage entries in /etc/hosts
  hosts: all
  become: true
  tasks:
    - name: Execute Ansible Role sap_maintain_etc_hosts
      ansible.builtin.include_role:
        name: community.sap_install.sap_maintain_etc_hosts
      vars:
        sap_maintain_etc_hosts_list:
        - node_ip: 10.10.10.10
          state: absent

        - node_name: host2
          state: absent

        - node_ip: 10.10.10.11
          node_name: host1
          aliases:
            - alias1
            - alias2
          node_comment: "host1 comment"
          state: present
```

Example playbook when executed together with [sap_ha_pacemaker_cluster](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_pacemaker_cluster) role which uses either `sap_ha_pacemaker_cluster_cluster_nodes` or `sap_hana_cluster_nodes`.
```yaml
- name: Ansible Play for add entry in /etc/hosts
  hosts: all
  become: true
  tasks:
    - name: Execute Ansible Role sap_maintain_etc_hosts
      ansible.builtin.include_role:
        name: community.sap_install.sap_maintain_etc_hosts
      vars:
        sap_maintain_etc_hosts_list: "{{ sap_ha_pacemaker_cluster_cluster_nodes }}"
```
<!-- END Execution Example -->

<!-- BEGIN Role Tags -->
<!-- END Role Tags -->

<!-- BEGIN Further Information -->
## Further Information
For more examples on how to use this role in different installation scenarios, refer to the [ansible.playbooks_for_sap](https://github.com/sap-linuxlab/ansible.playbooks_for_sap) playbooks.
<!-- END Further Information -->

## License
<!-- BEGIN License -->
Apache 2.0
<!-- END License -->

## Maintainers
<!-- BEGIN Maintainers -->
- [Markus Koch](https://github.com/rhmk)
- [Bernd Finger](https://github.com/berndfinger)
- [Marcel Mamula](https://github.com/marcelmamula)
<!-- END Maintainers -->

## Role Variables
<!-- BEGIN Role Variables -->

This role requires the dictionary `sap_maintain_etc_hosts_list` which contains the parameters for the `/etc/hosts` file.

The default value is the definition of the cluster nodes like in the role [sap_ha_pacemaker_cluster](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_pacemaker_cluster).</br>
If the value `sap_hana_cluster_nodes` or `sap_ha_pacemaker_cluster_cluster_nodes` is not defined, then the role expects valid `sap_maintain_etc_hosts_list`.

**NOTE: If you want to use this role to remove entries from /etc/hosts it is a good practice to do this before adding entries.**<br>
**The adding/removal is done in the order the entries are listed.**

### sap_maintain_etc_hosts_list
- _Type:_ `list` with elements of type `dict`

Mandatory list of nodes in form of dictionaries to be added or removed in `/etc/hosts` file.

Following dictionary keys can be defined:

- **node_ip**<br>
    - _Type:_ `string`

    IP address of the host to manage, depending on `state`.<br>
    **Required** for `state: present`.</br>
    _Optional_ for `state: absent`, where `node_name` and `node_domain` can be used instead.

- **node_name**<br>
    - _Type:_ `string`

    Hostname of the host to manage.<br>
    **Required** for `state: present`.</br>
    _Optional_ for `state: absent`, where `node_ip` can be used instead.

- **node_domain**<br>
    - _Type:_ `string`
    - _Default:_ `{{ sap_maintain_etc_hosts_domain }}`

    Domain name of the host to manage.<br>
    Defaults to `sap_maintain_etc_hosts_domain` or `ansible_facts['domain']`.<br>
    **Required** for `state: present`.</br>
    _Optional_ for `state: absent` with `node_name`, where `node_ip` can be used instead.

- **aliases**<br>
    - _Type:_ `list` with elements of type `string`

    List of aliases of the host to manage.<br>
    _Optional_ for `state: present`.<br>
    Not used in `state: absent`.

- **alias_mode**<br>
    - _Type:_ `string`
    - _Default:_ `merge`

    Select method of managing aliases of the host.

    - `merge` - merges the list of aliases with the exiting aliases of the host.
    - `overwrite` - overwrites the aliases of the host.

    _Optional_ for `state: present`.<br>
    Not used in `state: absent`.

- **node_comment**<br>
    - _Type:_ `string`
    - _Default:_ `managed by ansible sap_maintain_etc_hosts role`

    String which is appended at end of line of the host to manage.<br>
    Replaces existing comment, if present.<br>
    _Optional_ for `state: present`.<br>
    Not used in `state: absent`.

- **hana_site**<br>
    - _Type:_ `string`

    Used by [sap_ha_pacemaker_cluster](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_pacemaker_cluster) role and it is appended to `node_comment`<br>
    _Optional_ for `state: present`.<br>
    Not used in `state: absent`.

- **node_role**<br>
    - _Type:_ `string`

    Not used, but mentioned for compatibility reasons with [sap_ha_pacemaker_cluster](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_pacemaker_cluster) role.<br>

- **state**<br>
    - _Type:_ `string`
    - _Default:_ `present`

    Select desired state of host item.

    - `present` - Add new hosts entry.
    - `absent` - Remove existing hosts entry.

    _Optional_ for `state: present`.<br>
    **Required** for `state: absent`, because it defaults to `present`.</br>

### sap_maintain_etc_hosts_delimiter
- _Type:_ `str`
- _Default:_ `' '`
- _Choices:_ `' ', '/t'`

Delimiter for `/etc/hosts` used to separate all elements on a line.</br>
Changing delimiter will report as change, even if actual content did not change.</br>

### sap_maintain_etc_hosts_comment
- _Type:_ `str`
- _Default:_ `managed by Ansible role sap_maintain_etc_hosts`

Comment to be appended, if comment is not defined in `sap_maintain_etc_hosts_list`.
Replaces existing comment, if present.<br>
<!-- END Role Variables -->