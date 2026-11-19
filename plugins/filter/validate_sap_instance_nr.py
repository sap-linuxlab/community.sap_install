# SPDX-License-Identifier: Apache-2.0

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.community.sap_install.plugins.plugin_utils.sap_instance_nr import (
    validate_sap_instance_nr,
)

DOCUMENTATION = """
    name: validate_sap_instance_nr
    short_description: Validate an SAP instance number and return detailed results
    description:
        - Returns detailed validation results for SAP instance number criteria.
        - Checks if it is a string, has no leading or trailing whitespace, is exactly 2 characters,
          and consists of digits only.
        - When an installer is given, the instance number is also checked against the range that
          installer permits. SWPM does not restrict the instance number, hdblcm requires it to be
          between 00 and 97.
    options:
        _input:
            description: The value to validate
            type: any
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
# Get detailed validation results
- set_fact:
    validation: "{{ my_instance_nr | community.sap_install.validate_sap_instance_nr }}"

# Include the instance number range permitted by hdblcm
- set_fact:
    validation: "{{ my_instance_nr | community.sap_install.validate_sap_instance_nr('hdblcm') }}"

# Use in assert with detailed error message
- assert:
    that:
      - my_instance_nr is community.sap_install.valid_sap_instance_nr('hdblcm')
    fail_msg: |
      Validation failed:
      {% for condition in (my_instance_nr | community.sap_install.validate_sap_instance_nr('hdblcm')).failed_conditions %}
      - {{ condition }}
      {% endfor %}
"""

RETURN = """
_result:
    description: Dictionary with validation results
    type: dict
    contains:
        valid:
            description: True if the instance number is valid, False otherwise
            type: bool
        failed_conditions:
            description: List of failed validation conditions
            type: list
            elements: str
"""


class FilterModule(object):
    def filters(self):
        return {
            'validate_sap_instance_nr': validate_sap_instance_nr
        }
