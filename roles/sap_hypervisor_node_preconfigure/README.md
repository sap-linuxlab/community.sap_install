`EXPERIMENTAL`

sap_hypervisor_node_preconfigure
=======================

This role will set and check the required settings and parameters for a hypervisor running VMs for SAP HANA.

Requirements
------------
A RHV hypervisor. 

Role Variables
--------------

`sap_hypervisor_node_preconfigure_reserved_ram (default: 100)` Reserve memory [GB] for hypervisor host. Depending in the use case should be at least 50-100GB. 

`sap_hypervisor_node_preconfigure_reserve_hugepages (default: static)` Hugepage allocation method: {static|runtime}.
static: done at kernel command line which is slow, but safe
runtime: done with hugeadm which is faster, but can in some cases not ensure all HPs are allocated.

`sap_hypervisor_node_preconfigure_kvm_nx_huge_pages (default: "auto")` Setting for the huge page shattering kvm.nx_huge_pages: {"auto"|"on"|"off"}. Note the importance of the quotes, otherwise off will be mapped to false. See https://www.kernel.org/doc/html/latest/admin-guide/kernel-parameters.html for additional information:
```
        kvm.nx_huge_pages=
                        [KVM] Controls the software workaround for the
                        X86_BUG_ITLB_MULTIHIT bug.
                        force   : Always deploy workaround.
                        off     : Never deploy workaround.
                        auto    : Deploy workaround based on the presence of
                                  X86_BUG_ITLB_MULTIHIT.

                        Default is 'auto'.

                        If the software workaround is enabled for the host,
                        guests do need not to enable it for nested guests.
```

`sap_hypervisor_node_preconfigure_tsx (default: "off")` Intel Transactional Synchronization Extensions (TSX): {"on"|"off"}. Note the importance of the quotes, otherwise off will be mapped to false.

`sap_hypervisor_node_preconfigure_assert (default: false)` In assert mode, the parameters on the system are checked if the confirm with what this role would set.

`sap_hypervisor_node_preconfigure_ignore_failed_assertion (default: no)` Fail if assertion is invalid.

`sap_hypervisor_node_preconfigure_run_grub2_mkconfig (default: yes)` Update the grub2 config.


Example Playbook
----------------

Simple example that just sets the parameters.
```
- hosts: all
  roles:
    - sap_hypervisor_node_preconfigure
```

Run in assert mode to verify that parameters have been set.
```
- hosts: all
  roles:
    - sap_hypervisor_node_preconfigure
  vars:
    - sap_hypervisor_node_preconfigure_assert: yes
```
License
-------

Apache 2.0

Author Information
------------------

Nils Koenig (nkoenig@redhat.com)
