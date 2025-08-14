# SPDX-License-Identifier: Apache-2.0

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    name: valid_sap_abap_platform_hostname
    short_description: Test if a string is a valid SAP hostname
    description:
        - Tests if a string meets hostname validation criteria
        - Checks if it is a string, has 13 characters or less, does not start with a number,
          does not contain any characters other than alpha characters, digits and the hyphen character,
          and does not contain a dot character
    options:
        _input:
            description: The string to test
            type: string
            required: true
"""

EXAMPLES = """
# Test if variable is a valid SAP hostname
- assert:
    that:
      - my_hostname is community.sap_install.valid_sap_abap_platform_hostname
    fail_msg: "{{ my_hostname }} is not a valid hostname"

# In a conditional
- debug:
    msg: "Valid hostname"
  when: server_name is community.sap_install.valid_sap_abap_platform_hostname
"""

RETURN = """
_result:
    description: True if the string meets all hostname criteria, False otherwise
    type: bool
"""


def valid_sap_abap_platform_hostname(value):
    """
    Test if value is a valid hostname according to specified criteria:
    1. Must be a string
    2. Must be 13 characters or less
    3. Must not start with a number
    4. Does not contain any characters other than alpha characters, digits and the hyphen character,
    5. Must not contain a dot

    Returns True if valid, False if invalid
    """
    if not isinstance(value, str):
        return False

    if len(value) > 13:
        return False

    if value and value[0].isdigit():
        return False

    if value and not value.replace('-', 'x').isalnum():
        return False

    if value and str(value).find('.') != -1:
        return False

    return True


class TestModule(object):
    def tests(self):
        return {
            'valid_sap_abap_platform_hostname': valid_sap_abap_platform_hostname,
        }
