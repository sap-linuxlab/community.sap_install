# SPDX-License-Identifier: Apache-2.0

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.community.sap_install.plugins.plugin_utils.sap_sid import (
    validate_sap_sid,
)

DOCUMENTATION = """
    name: valid_sap_sid
    short_description: Test if a string is a valid SAP System ID
    description:
        - Tests if a string meets SAP System ID validation criteria.
        - Checks if it is a string, has no leading or trailing whitespace, is exactly 3 characters,
          does not start with a number, and does not contain any characters other than
          alpha characters and digits.
        - When an installer is given, the SAP System ID is also checked against the list of
          SAP System IDs reserved by that installer. The comparison is made on the uppercased
          value, so a lowercase SAP System ID is matched against the list as well.
        - Use the P(community.sap_install.validate_sap_sid#filter) filter to report why a value failed.
    options:
        _input:
            description: The string to test
            type: string
            required: true
        installer:
            description:
                - The SAP installer whose reserved SAP System IDs are checked in addition to the
                  generic criteria.
                - When omitted, only the generic criteria are applied.
            type: str
            choices: [hdblcm, swpm]
            required: false
"""

EXAMPLES = """
# Test if variable is a valid SAP System ID
- assert:
    that:
      - my_sid is community.sap_install.valid_sap_sid
    fail_msg: "{{ my_sid }} is not a valid SAP System ID"

# Also reject the SAP System IDs reserved by hdblcm
- assert:
    that:
      - my_sid is community.sap_install.valid_sap_sid('hdblcm')
    fail_msg: "{{ my_sid }} is not a valid SAP System ID for hdblcm"

# In a conditional
- debug:
    msg: "Valid SAP System ID"
  when: my_sid is community.sap_install.valid_sap_sid
"""

RETURN = """
_result:
    description: True if the string meets all SAP System ID criteria, False otherwise
    type: bool
"""


def valid_sap_sid(value, installer=None):
    """
    Test if value is a valid SAP System ID.

    Shares its criteria with the 'validate_sap_sid' filter, which reports
    which of them failed.

    Returns True if valid, False if invalid
    """
    return validate_sap_sid(value, installer)['valid']


class TestModule(object):
    def tests(self):
        return {
            'valid_sap_sid': valid_sap_sid,
        }
