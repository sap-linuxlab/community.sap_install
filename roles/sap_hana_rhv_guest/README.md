sap_hana_rhv_guest
==================

This role will check the required settings and parameters for a guest (VM) running on RHV/KVM for SAP HANA. 


Requirements
------------

VM with at least RHEL 8.2 installed.
The roles sap_preconfigure and sap_hana_preconfigure have been run on that system.


Role Variables
--------------

`sap_hana_rhv_guest_tsx (default: "on")` Intel Transactional Synchronization Extensions (TSX): {"on"|"off"}.
Note the importance of the quotes, otherwise off will be mapped to false.

`sap_hana_rhv_guest_assert (default: false)` In assert mode, the parameters on the system are checked if the confirm with what this role would set.

`sap_hana_rhv_guest_ignore_failed_assertion (default: no)` Fail if assertion is invalid.

`sap_hana_rhv_guest_run_grub2_mkconfig (default: yes)` Update the grub2 config.


Dependencies
------------

The roles [sap_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_preconfigure) and [sap_hana_preconfigure](https://github.com/sap-linuxlab/community.sap_install/tree/main/roles/sap_hana_preconfigure).


Example Playbook
----------------

Simple example that just sets the parameters.
```
- hosts: all
  roles:
    - sap_hana_rhv_guest
```

Run in assert mode to verify that parameters have been set.
```
- hosts: all
  roles:
    - sap_hana_rhv_guest
  vars:
    - sap_hana_rhv_guest_assert: yes
```

License
-------

Apache-2.0

Author Information
------------------

Nils Koenig (nkoenig@redhat.com)
