# SPDX-License-Identifier: Apache-2.0

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.community.sap_install.plugins.plugin_utils.sap_os_vars_files import (
    get_sap_os_vars_files,
)

DOCUMENTATION = """
    name: get_sap_os_vars_files
    short_description: List the OS specific vars files of a role
    description:
        - Returns the names of the vars files that apply to the OS described by the Ansible facts.
        - The names are ordered from least to most specific, so loading them in order lets the
          more specific file override the less specific one.
        - The files are, where they apply, the OS family, the distribution, the major release,
          the minor release and, for C(SLES_SAP), the same major and minor release files named
          after C(SLES), which lets both distributions share variables.
        - On C(RedHat) a file is added for every minor release up to the current one, such as
          C(RedHat_9.1.plus.yml) and C(RedHat_9.2.plus.yml) on RHEL 9.2. These files hold
          variables that are valid for the named minor release and all later ones.
        - The filter does not check that a file exists, skip the missing ones when loading.
        - Characters in the facts other than letters, digits, dot, underscore and hyphen are
          replaced by an underscore, so C(openSUSE Tumbleweed) results in C(openSUSE_Tumbleweed).
        - A rolling release without a minor version, such as C(openSUSE Tumbleweed), results in
          a single version file.
        - Fails when the C(os_family) or C(distribution) fact is missing, which points to
          disabled fact gathering or an unsupported OS.
    options:
        _input:
            description: The Ansible facts, usually C(ansible_facts).
            type: dict
            required: true
"""

EXAMPLES = """
# Load the vars files of the role that apply to the OS
- name: Include OS specific vars
  ansible.builtin.include_vars: "{{ __vars_file }}"
  loop: "{{ ansible_facts | community.sap_install.get_sap_os_vars_files }}"
  vars:
    __vars_file: "{{ role_path }}/vars/{{ item }}"
  when: __vars_file is file

# Example result on SLES_SAP 15.7
# - Suse.yml
# - SLES_SAP.yml
# - SLES_15.yml
# - SLES_SAP_15.yml
# - SLES_15.7.yml
# - SLES_SAP_15.7.yml
"""

RETURN = """
_value:
    description: The vars file names, ordered from least to most specific.
    type: list
    elements: str
"""


class FilterModule(object):
    def filters(self):
        return {
            'get_sap_os_vars_files': get_sap_os_vars_files
        }
