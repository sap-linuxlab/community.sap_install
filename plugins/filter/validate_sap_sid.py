# SPDX-License-Identifier: Apache-2.0

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.community.sap_install.plugins.plugin_utils.sap_sid import (
    validate_sap_sid,
)

DOCUMENTATION = """
    name: validate_sap_sid
    short_description: Validate an SAP System ID and return detailed results
    description:
        - Returns detailed validation results for SAP System ID criteria.
        - Checks if it is a string, has no leading or trailing whitespace, is exactly 3 characters,
          does not start with a number, and does not contain any characters other than
          alpha characters and digits.
        - When an installer is given, the SAP System ID is also checked against the list of
          SAP System IDs reserved by that installer. The comparison is made on the uppercased
          value, so a lowercase SAP System ID is matched against the list as well.
    options:
        _input:
            description: The value to validate
            type: any
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
# Get detailed validation results
- set_fact:
    validation: "{{ my_sid | community.sap_install.validate_sap_sid }}"

# Include the SAP System IDs reserved by hdblcm
- set_fact:
    validation: "{{ my_sid | community.sap_install.validate_sap_sid('hdblcm') }}"

# Use in assert with detailed error message
- assert:
    that:
      - my_sid is community.sap_install.valid_sap_sid('hdblcm')
    fail_msg: |
      Validation failed:
      {% for condition in (my_sid | community.sap_install.validate_sap_sid('hdblcm')).failed_conditions %}
      - {{ condition }}
      {% endfor %}
"""

RETURN = """
_result:
    description: Dictionary with validation results
    type: dict
    contains:
        valid:
            description: True if the SAP System ID is valid, False otherwise
            type: bool
        failed_conditions:
            description: List of failed validation conditions
            type: list
            elements: str
"""


class FilterModule(object):
    def filters(self):
        return {
            'validate_sap_sid': validate_sap_sid
        }
