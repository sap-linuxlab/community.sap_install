`EXPERIMENTAL`

# sap_hypervisor_node_preconfigure

This role will configure the following hypervisors in order to run SAP workloads:
* Red Hat OpenShift Virtualization (OCPV)
* Red Hat Enterprise Virtualization (RHV) 

## Platform: Red Hat OpenShift Virtualization

This role will configure a plain vanilla OpenShift cluster so it can be used for SAP workloads. 

### Requirements
* A freshly installed OpenShift cluster. 
* The worker nodes should have > 96GB of memory. 
* Storage is required, e.g. via NFS, OpenShift Data Foundation  or local storage. This role can setup access to a Netapp Filer via Trident storage connector. 
* `kubeconfig` Point the `KUBECONFIG` environment variable to you `kubeconfig`.
* Required packages: Install the packages stated in `requirements.txt` on the host where the role runs.
The required packages are:
```
httpd-tools
ansible-collection-kubernetes-core
```


* Make the role available in case you didn't install it already in an ansible roles directory, e.g.

```
mkdir -p ~/.ansible/roles/
ln -sf ~/community.sap_install/roles/sap_hypervisor_node_preconfigure ~/.ansible/roles/
```

### Role Variables
General variables are defined in sap_hypervisor_node_preconfigure/vars/platform_defaults_redhat_ocp_virt.yml
```
# Install the trident NFS storage provider
sap_hypervisor_node_preconfigure_install_trident: False
# URL of the trident installer package to use
sap_hypervisor_node_preconfigure_install_trident_url: https://github.com/NetApp/trident/releases/download/v23.01.0/trident-installer-23.01.0.tar.gz

# should SRIOV be enabled for unsupported NICs
sap_hypervisor_node_preconfigure_sriov_enable_unsupported_nics: True

# Amount of memory [GB] to be reserved for the hypervisor on hosts >= 512GB
sap_hypervisor_node_preconfigure_hypervisor_reserved_ram_host_ge_512: 64 #GB
# Amount of memory [GB] to be reserved for the hypervisor on hosts < 512GB
sap_hypervisor_node_preconfigure_hypervisor_reserved_ram_host_lt_512: 32 #GB

# Should the check for the minimal amount of be ignored? Minimal amount is 96 GB
# If ignored, the amount of $hostmemory - $reserved is allocated with a lower bound of 0 in case $reserved > $hostmemory
sap_hypervisor_node_preconfigure_ignore_minimal_memory_check: False
```

The following variables are describing the nodes and networks to be used. It can make sense to have them in a seperate file, e.g. see `playbooks/vars/sample-variables-sap-hypervisor-node-preconfigure-rh_ocp_virt.yml` for an example. 
```
sap_hypervisor_node_preconfigure_cluster_config:
  # URL under which the OCP cluster is reachable
  cluster_url: ocpcluster.domain.org

  # namespace under which the VMs are created, note this has to be
  # openshift-sriov-network-operator in case of using SRIOV network
  # devices 
  vm_namespace: sap

  # Optional, configuration for trident driver for Netapp NFS filer
  trident:
    management: management.domain.org
    data: datalif.netapp.domain.org
    svm: sap_svm
    backend: nas_backend
    aggregate: aggregate_Name
    username: admin
    password: xxxxx
    storage_driver: ontap-nas
    storage_prefix: ocpv_sap_

  # detailed configuration for every worker that should be configured
  workers:
      kubernetes_reserved_cpus: "0,1"   # CPU cores reserved for
                                         # kubernetes

      - name: worker-0                   # name must match the node name
        networks:                        # Example network config
          - name: sapbridge              # using a bridge
            description: SAP bridge
            state: up
            type: linux-bridge
            ipv4:
              enabled: false
              auto-gateway: false
              auto-dns: false
            bridge:
              options:
                stp:
                  enabled: false
              port:
                - name: ens1f0           # network IF name
          - name: storage                # an SRIOV device        
            interface: ens2f0            # network IF name
            type: sriov

          - bridge:                      # another bridge
              options:
                stp:
                  enabled: false
              port:
              - name: ens2f0             # network IF name
            description: storage
            mtu: 9000
            ipv4:
              address:
              - ip: 192.168.1.51         # IP config
                prefix-length: 24
              auto-dns: false
              auto-gateway: false
            enabled: true
            name: storagebridge
            state: up
            type: linux-bridge
          - name: multi                  # another SRIOV device
            interface: ens2f1            # network IF name
            type: sriov

      - name: worker-1                   # second worker configuration
        networks:                        # Example network config
          - name: sapbridge              # using a bridge
            description: SAP bridge
            state: up
            type: linux-bridge
            ipv4:
              enabled: false
              auto-gateway: false
              auto-dns: false
            bridge:
              options:
                stp:
                  enabled: false
              port:
                - name: ens1f0           # network IF name
          - name: storage                # an SRIOV device        
            interface: ens2f0            # network IF name
            type: sriov                        
```

### Dependencies
A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

### Example Playbook
See `playbooks/sample-sap-hypervisor-redhat_ocp_virt-preconfigure.yml` for an example.

### Example Usage
Make sure to set the `KUBECONFIG` environment variable, e.g.
```
export KUBECONFIG=~/.kubeconfig
```
To invoke the example playbook with the example configuration using your localhost as ansible host use the following command line:
```
ansible-playbook --connection=local -i localhost,  playbooks/sample-sap-hypervisor-redhat_ocp_virt-preconfigure.yml -e @s/sample-sap-hypervisor-redhat_ocp_virt-preconfigure.yml
```


## Platform: RHEL KVM
This Ansible Role allows preconfigure of Red Hat Virtualization (RHV), formerly called Red Hat Enterprise Virtualization (RHEV) prior to version 4.4 release. Red Hat Virtualization (RHV) consists of 'Red Hat Virtualization Manager (RHV-M)' and the 'Red Hat Virtualization Host (RHV-H)' hypervisor nodes that this Ansible Role preconfigures. Please note, Red Hat Virtualization is discontinued and available until mid-2024 in Maintenance support or mid-2026 in Extended Life support.
This Ansible Role does not preconfigure RHEL KVM (RHEL-KVM) hypervisor nodes. Please note that RHEL KVM is standalone, and does not have Management tooling (previously provided by RHV-M).

### Requirements
* A RHV hypervisor. 

### Role Variables
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


### Example Playbook
Simple example that just sets the parameters.
```
---
- hosts: all
  gather_facts: true
  serial: 1
  vars:
    sap_hypervisor_node_platform: redhat_rhel_kvm
  tasks:
    - name: Include Role
      ansible.builtin.include_role:
        name: sap_hypervisor_node_preconfigure
```

Run in assert mode to verify that parameters have been set.
```
---
- hosts: all
  gather_facts: true
  serial: 1
  vars:
    sap_hypervisor_node_platform: redhat_rhel_kvm
    sap_hypervisor_node_preconfigure_assert: yes
  tasks:
    - name: Include Role
      ansible.builtin.include_role:
        name: sap_hypervisor_node_preconfigure
```
### License
Apache 2.0

### Author Information
Nils Koenig (nkoenig@redhat.com)
