# SPDX-License-Identifier: Apache-2.0

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.community.sap_install.plugins.plugin_utils.sap_abap_platform_hostname import (
    validate_sap_abap_platform_hostname,
)

DOCUMENTATION = """
    name: validate_sap_abap_platform_hostname
    short_description: Validate hostname and return detailed results
    description:
        - Returns detailed validation results for SAP ABAP Platform hostname criteria.
        - Applies to SAP ABAP Platform (SAP note 611361) and SAP JAVA (SAP note 3216549).
        - Checks if it is a string, has 13 characters or less, does not start with a number,
          does not contain any characters other than alpha characters, digits and the hyphen character,
          and does not contain a dot character.
    options:
        _input:
            description: The value to validate
            type: any
            required: true
"""

EXAMPLES = """
# Get detailed validation results
- set_fact:
    validation: "{{ my_hostname | community.sap_install.validate_sap_abap_platform_hostname }}"

# Use in assert with detailed error message
- assert:
    that:
      - validation.valid
    fail_msg: |
      Validation failed:
      {% for condition in validation.failed_conditions %}
      - {{ condition }}
      {% endfor %}
"""

RETURN = """
_result:
    description: Dictionary with validation results
    type: dict
    contains:
        valid:
            description: True if hostname is valid, False otherwise
            type: bool
        failed_conditions:
            description: List of failed validation conditions
            type: list
            elements: str
"""


class FilterModule(object):
    def filters(self):
        return {
            'validate_sap_abap_platform_hostname': validate_sap_abap_platform_hostname
        }
