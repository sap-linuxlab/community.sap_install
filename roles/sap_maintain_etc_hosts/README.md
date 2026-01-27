<!-- BEGIN Title -->
# sap_maintain_etc_hosts Ansible Role
<!-- END Title -->

## Description
<!-- BEGIN Description -->
The Ansible role `sap_maintain_etc_hosts` is used to maintain the `/etc/hosts` file..
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
1. Assert that required inputs were provided.
2. Verify duplicate entries and conflicts;
3. Update `/etc/hosts` file.
<!-- END Execution Flow -->

### Example
<!-- BEGIN Execution Example -->
Example playbook will update `/etc/hosts`:

- Remove node with IP `10.10.10.10`.
- Remove node with name `host2`.
- Add node with IP `10.10.10.11`, name `host1`, aliases `alias1, alias2` and comment `host1 comment`.
```yaml
- name: Ansible Play for add entry in /etc/hosts
  hosts: all
  become: true
  tasks:
    - name: Execute Ansible Role sap_sap_maintain_etc_hosts
      ansible.builtin.include_role:
        name: community.sap_install.sap_sap_maintain_etc_hosts
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
          node_comment: "host1 comment"  # Comment is created after hash sign (defaults to hana_site)
          state: present
```

Example playbook when executed together with [sap_ha_pacemaker_cluster](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_pacemaker_cluster) role which uses either `sap_ha_pacemaker_cluster_cluster_nodes` or `sap_hana_cluster_nodes`.
```yaml
- name: Ansible Play for add entry in /etc/hosts
  hosts: all
  become: true
  tasks:
    - name: Execute Ansible Role sap_sap_maintain_etc_hosts
      ansible.builtin.include_role:
        name: community.sap_install.sap_sap_maintain_etc_hosts
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
<!-- END Maintainers -->

## Role Variables
<!-- BEGIN Role Variables -->

This role requires the dictionary `sap_maintain_etc_hosts_list` which contains the parameters for the `/etc/hosts` file.

The default value is the definition of the cluster nodes like in the role [sap_ha_pacemaker_cluster](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_pacemaker_cluster).</br>
If the value `sap_hana_cluster_nodes`or `sap_ha_pacemaker_cluster_cluster_nodes` is not defined, then the role creates a default value from `ansible_facts`.

**NOTE: If you want to use this role to remove entries from /etc/hosts it is a good practice to do this before adding entries. The adding/removal is done in the order the entries are listed.**

### sap_maintain_etc_hosts_list

- _Type:_ `list` with elements of type `dict`

Mandatory list of nodes in form of dictionaries to be added or removed in `/etc/hosts` file.

Following dictionary keys can be defined:

- **node_ip**<br>
    IP address of the managed node.<br>
    **Required** for adding new entries to `/etc/hosts`.</br>
    _Optional_ for removing entries, where `node_name` and `node_domain` can be used instead.

    - _Type:_ `string`

- **node_name**<br>
    Hostname of the managed node.<br>
    **Required** for adding new entries to `/etc/hosts`.</br>
    _Optional_ for removing entries, when `node_ip` is not used.

    - _Type:_ `string`

- **node_domain**<br>
    Domain name of the managed node. Defaults to `sap_domain` if set or `ansible_domain`.<br>
    **Required** for adding new entries to `/etc/hosts`.</br>
    _Optional_ for removing entries, when `node_name` is used.

    - _Type:_ `string`
    - _Default:_ `sap_domain`

- **aliases**<br>
    List of aliases for the managed node.<br>
    _Optional_ for adding new entries to `/etc/hosts`.

    - _Type:_ `list` with elements of type `string`

- **alias_mode**<br>
    Select method of updating `/etc/hosts` file:<br>
        - `merge` : merges the list of aliases with the exiting aliases of the node.<br>
        - `overwrite` : overwrites the aliases of the node. 
    _Optional_ for adding new entries to `/etc/hosts`.

    - _Type:_ `string`
    - _Default:_ `merge`

- **node_comment**<br>
    Node comment is appended at end of line of managed node.<br>
    _Optional_ for adding new entries to `/etc/hosts`.

    - _Type:_ `string`
    - _Default:_ `managed by ansible sap_maintain_etc_hosts role`

- **hana_site**<br>
    Used by [sap_ha_pacemaker_cluster](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_pacemaker_cluster) and it is appended to `node_comment`<br>
    _Optional_ for adding new entries to `/etc/hosts`.

    - _Type:_ `string`

- **node_role**<br>
    Not used, but mentioned for compatibility reasons for [sap_ha_pacemaker_cluster](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_pacemaker_cluster) role.<br>

    - _Type:_ `string`

- **state**<br>
    Select `present` for adding new entries, `absent` for removing them.<br>
    **Required** for removing entries, otherwise default `present` is used.

    - _Type:_ `string`
    - _Default:_ `present`
<!-- END Role Variables -->