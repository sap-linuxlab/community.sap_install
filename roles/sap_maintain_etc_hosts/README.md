<!-- BEGIN Title -->
# sap_maintain_etc_hosts Ansible Role
<!-- END Title -->

## Description
<!-- BEGIN Description -->
Ansible Role `sap_maintain_etc_hosts` is used to maintain `/etc/hosts` file.
<!-- END Description -->

<!-- BEGIN Dependencies -->
<!-- END Dependencies -->

<!-- BEGIN Prerequisites -->
<!-- END Prerequisites -->

## Execution
<!-- BEGIN Execution -->
Role can be executed independently or as part of [ansible.playbooks_for_sap](https://github.com/sap-linuxlab/ansible.playbooks_for_sap) playbooks.
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

## Role Input Parameters
All input parameters used by role are described in [INPUT_PARAMETERS.md](https://github.com/sap-linuxlab/community.sap_install/blob/main/roles/sap_sap_maintain_etc_hosts/INPUT_PARAMETERS.md)
