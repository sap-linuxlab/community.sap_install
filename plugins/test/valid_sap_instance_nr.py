# SPDX-License-Identifier: Apache-2.0

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.community.sap_install.plugins.plugin_utils.sap_instance_nr import (
    validate_sap_instance_nr,
)

DOCUMENTATION = """
    name: valid_sap_instance_nr
    short_description: Test if a string is a valid SAP instance number
    description:
        - Tests if a string meets SAP instance number validation criteria.
        - Checks if it is a string, has no leading or trailing whitespace, is exactly 2 characters,
          and consists of digits only.
        - When an installer is given, the instance number is also checked against the range that
          installer permits. SWPM does not restrict the instance number, hdblcm requires it to be
          between 00 and 97.
        - Use the P(community.sap_install.validate_sap_instance_nr#filter) filter to report why a
          value failed.
    options:
        _input:
            description: The string to test
            type: string
            required: true
        installer:
            description:
                - The SAP installer whose permitted instance number range is checked in addition
                  to the generic criteria.
                - When omitted, only the generic criteria are applied.
            type: str
            choices: [hdblcm, swpm]
            required: false
"""

EXAMPLES = """
# Test if variable is a valid SAP instance number
- assert:
    that:
      - my_instance_nr is community.sap_install.valid_sap_instance_nr
    fail_msg: "{{ my_instance_nr }} is not a valid SAP instance number"

# Also enforce the instance number range permitted by hdblcm
- assert:
    that:
      - my_instance_nr is community.sap_install.valid_sap_instance_nr('hdblcm')
    fail_msg: "{{ my_instance_nr }} is not a valid SAP instance number for hdblcm"

# In a conditional
- debug:
    msg: "Valid SAP instance number"
  when: my_instance_nr is community.sap_install.valid_sap_instance_nr
"""

RETURN = """
_result:
    description: True if the string meets all SAP instance number criteria, False otherwise
    type: bool
"""


def valid_sap_instance_nr(value, installer=None):
    """
    Test if value is a valid SAP instance number.

    Shares its criteria with the 'validate_sap_instance_nr' filter, which
    reports which of them failed.

    Returns True if valid, False if invalid
    """
    return validate_sap_instance_nr(value, installer)['valid']


class TestModule(object):
    def tests(self):
        return {
            'valid_sap_instance_nr': valid_sap_instance_nr,
        }
