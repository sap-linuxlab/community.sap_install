## Input Parameters for sap_maintain_etc_hosts Ansible Role
<!-- BEGIN Role Input Parameters -->

This role requires the dictionary `sap_maintain_etc_hosts_list` which contains the parameters for the `/etc/hosts` file.

The default value is the definition of the cluster nodes like in the role [sap_ha_pacemaker_cluster](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_ha_pacemaker_cluster). If the value `sap_hana_cluster_nodes`or `sap_ha_pacemaker_cluster_cluster_nodes` is not defined, then the role creates a default value from `ansible_facts`.

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
<!-- END Role Input Parameters -->