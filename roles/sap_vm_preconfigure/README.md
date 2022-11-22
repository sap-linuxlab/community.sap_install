`EXPERIMENTAL`

sap_vm_preconfigure
==================

This role will set and check the required settings and parameters for a guest (VM) running on RHV/KVM for SAP HANA.


Requirements
------------

VM with at least RHEL 8.2 installed.
The roles sap_preconfigure and sap_hana_preconfigure have been run on that system.


Role Variables
--------------

### Run the role in assert mode
```yaml
sap_vm_preconfigure_assert (default: no)
```
If the following variable is set to `yes`, the role will only check if the configuration of the managed mmachines is according to this role. Default is `no`.


### Behavior of the role in assert mode
```yaml
sap_vm_preconfigure_assert_ignore_errors (default: no)
```
If the role is run in assert mode and the following variable is set to `yes`, assertion errors will not cause the role to fail. This can be useful for creating reports.
Default is `no`, meaning that the role will fail for any assertion error which is discovered. This variable has no meaning if the role is not run in assert mode.



Dependencies
------------

The roles [sap_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_preconfigure) and [sap_hana_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_preconfigure).


Example Playbook
----------------

Simple example that just sets the parameters.
```
- hosts: all
  roles:
    - sap_preconfigure
    - sap_hana_preconfigure
    - sap_vm_preconfigure
```

Run in assert mode to verify that parameters have been set.
```
- hosts: all
  roles:
    - sap_vm_preconfigure
  vars:
    - sap_vm_preconfigure_assert: yes
```

License
-------

Apache-2.0

Author Information
------------------

Nils Koenig (nkoenig@redhat.com)
