# sap_detect_cloud_provider

Ansible role to detect where (what cloud provider) host is running in.
Tested on Azure and AWS and Virtualbox virtual machine.

Role is designed to run only on RHEL.

## Requirements

## Role Variables

Role does not have any input variables.

As a result of role execution on a host variable

```bash
sap_detect_cloud_provider_cloud_provider
```

Is set to one of the following values (pay attention to lowercase):

* azure
* aws

If this variable is not set as result of applying the role, this means that neither Azure nor AWS were detected from the instance.

Other cloud providers will follow.

## Dependencies

Role does not have any dependencies to other roles.

## Example Playbook

Here is an example of the playbook for the role.:

```yaml
    - hosts: servers
      roles:
         - { role: sap_detect_cloud_provider_cloud_provider }
```

## License

Apache-2.0

## Author Information

kksat
