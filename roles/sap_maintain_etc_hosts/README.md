# Role Name: sap_maintain_etc_hosts

This role can be used to reliably update the /etc/hosts file.

<!---
Requirements
------------

 Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.
--->

## Role Input Parameters

This role requires the dictionary `sap_maintain_etc_hosts_list` which contains the parameters for the hostfile. The default value is the definition of the cluster nodes like in the role `sap_ha_pacemaker_cluster`. If the value `sap_hana_cluster_nodes`or `sap_ha_pacemaker_cluster_cluster_nodes` is not defined the role creates a default value from `ansible_facts`.

Caution: If you want to use this role to remove entries from /etc/hosts it is a good practise to do this before adding entries. The adding/removal is done in the order the entries are listed.

### sap_maintain_etc_hosts_list

- _Type:_ `list`

  List of nodes to be added or removed in /etc/hosts
  possible list options:

#### node_ip

- _Type:_ `string`

  IP address of the node.
  It is required for adding a node.
  When deleting a node use only when node_name and node_domain are not defined

#### node_name

- _Type:_ `string`

  Hostname of the node
  It is required for adding a node.
  When deleting a node use only when node_ip is not defined

#### node_domain

- _Type:_ `string`

  Domainname of the node
  Defaults to sap_domain, if set, otherwise ansible_domain is the default
  When deleting a node use only when node_name is defined

#### aliases

- _Type:_ `list`

  List of aliases for the node
  Not used when state is absent

#### alias_mode

- _Type:_ `string`

  Options:

  - `merge` : merges the list of aliases with the exiting aliases of the node. (default)
  - `overwrite` : overwrites the aliases of the node.

  Not used when state is absent

#### node_comment

- _Type:_ `string`
  
    default: managed by ansible sap_maintain_etc_hosts role`
    String which is appended to line in hosts after comment string
    Not used when state is absent

#### hana_site

- _Type:_ `string`

  if set (e.g. for configuring cluster) it is appended to the comment
  Not used when state is absent

#### node_role

   Not used. For compatibility reason only.

#### state

- _Type:_ `string`

  Options:

  - `present` : creates a host entry (default)`
  - `absent` : removes a host entry by ip or hostname

<!---
Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.
--->

Example Playbook
----------------

If you want to setup/add entries your etc hosts you can use this snippet

```[yaml]
- name: Ensure /etc/hosts is updated
  include_role: sap_sap_maintain_etc_hosts
  var:
        sap_maintain_etc_hosts_list:
                - node_ip: 1.2.3.5
                  state: absent
                - node_name: host2
                  state: absent
                - node_ip: 1.2.3.4
                  node_name: host1
                  aliases:
                    - alias1
                    - anotheralias2
                  node_comment: "Here comes text after hashsign" (defaults to hana_site)
                  state: present
```

If you have defined a cluster and the variable `sap_ha_pacemaker_cluster_cluster_nodes` or `sap_hana_cluster_nodes` is set, you can use the following play:

```[yaml]
- name: ensure all cluster nodes are in /etc/hosts
  include_role: sap_maintain_etc_hosts
  var:
        sap_maintain_etc_hosts_list: "{{ sap_hana_cluster_nodes }}"
```

License
-------

Apache-2.0

Author Information
------------------

@rhmk 10/10/23
