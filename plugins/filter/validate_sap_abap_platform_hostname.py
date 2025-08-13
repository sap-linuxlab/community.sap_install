from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    name: validate_sap_abap_platform_hostname
    short_description: Validate hostname and return detailed results
    description:
        - Returns detailed validation results for SAP ABAP Platform hostname criteria
        - Checks if it is a string, has 13 characters or less, does not start with a number,
          only contains alpha characters, digits and the hyphen character, and does not contain a dot character
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


def validate_sap_abap_platform_hostname(value):
    """
    Validate hostname and return detailed failure information.

    Returns a dict consisting of a 'valid' boolean and a list of 'failed_conditions'
    """
    result = {
        'valid': True,
        'failed_conditions': []
    }

    # Check if value is really a string (not a number wrapped in AnsibleUnsafeText)
    try:
        # Try to convert to int/float - if successful, it is a number
        if str(value).isdigit() or (str(value).replace('.', '', 1).isdigit() and str(value).count('.') <= 1):
            # It's a numeric value
            result['valid'] = False
            result['failed_conditions'].append(f"Value must be a string, got numeric value: {value}!")
            return result
    except (ValueError, AttributeError):
        pass

    # Check if it is a string type (including AnsibleUnsafeText)
    if not isinstance(value, str):
        result['valid'] = False
        result['failed_conditions'].append(f"Value must be a string, got {type(value).__name__}!")
        return result

    # Convert to regular string to handle AnsibleUnsafeText
    str_value = str(value)

    # String too long
    if len(str_value) > 13:
        result['valid'] = False
        result['failed_conditions'].append(f"Length must be 13 characters or less, got {len(str_value)}!")

    # String stars with a number
    if str_value and str_value[0].isdigit():
        result['valid'] = False
        result['failed_conditions'].append(f"Must not start with a number, starts with '{str_value[0]}'!")

    # String contains other characters besides alpha characters, digits and the hyphen character
    if str_value and not str_value.replace('-', 'x').isalnum():
        result['valid'] = False
        result['failed_conditions'].append(f"Must not contain any other character than alpha characters, digits, or hyphens!")

    # String contains a dot character
    if str_value and str_value.find('.') != -1:
        result['valid'] = False
        result['failed_conditions'].append(f"Must not contain a dot character, contains at least one, at position {str(value).find('.') + 1}!")

    return result


class FilterModule(object):
    def filters(self):
        return {
            'validate_sap_abap_platform_hostname': validate_sap_abap_platform_hostname
        }
