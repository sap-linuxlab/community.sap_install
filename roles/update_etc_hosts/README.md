Role Name
=========

This role can be used to reliably update teh /etc/hosts file

<!---
Requirements
------------

 Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.
--->

Role Variables
--------------

This role needs a a dictonary `update_etc_hosts_list` which contains the parameters for the hostfile

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
  include_role: sap_update_etc_hosts
  var:
        update_etc_hosts_list:
                - node_ip: 1.2.3.4
                  node_name: host1
                  aliases:
                    - alias1
                    - anotheralias2
                  comment: "Here comes text after hashsign" (defaults to hana_site)
                  state: present
                - node_ip: 1.2.3.5
                  node_name: host2
                  state: absent
```
If you have defined a cluster and the variable `sap_ha_pacemaker_cluster_cluster_nodes` or `sap_hana_cluster_nodes` is set, you can use the follwoing play:

```[yaml]
- name: ensure all cluster nodes are in /etc/hosts
  include_role: update_etc_hosts
  var:
        update_etc_hosts_list: "{{ sap_hana_cluster_nodes }}
```

License
-------

Apache-2.0

Author Information
------------------

@rhmk 10/10/23
