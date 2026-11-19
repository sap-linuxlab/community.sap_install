# SPDX-License-Identifier: Apache-2.0

# Shared plugin_utils for SAP ABAP Platform hostname validation.
# Applies to SAP ABAP Platform (SAP note 611361)
# and SAP JAVA (SAP note 3216549).

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

SAP_HOSTNAME_MAX_LENGTH = 13


def validate_sap_abap_platform_hostname(value):
    """
    Validate a hostname and return detailed failure information.

    Criteria:
    1. Must be a string and must not be a number in string form
    2. Must be 13 characters or less
    3. Must not start with a digit
    4. Must consist of alpha characters, digits and the hyphen character only
    5. Must not contain a dot character

    Returns a dict consisting of a 'valid' boolean and a list of
    'failed_conditions'.
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
    if len(str_value) > SAP_HOSTNAME_MAX_LENGTH:
        result['valid'] = False
        result['failed_conditions'].append(
            f"Length must be {SAP_HOSTNAME_MAX_LENGTH} characters or less, got {len(str_value)}!"
        )

    # String starts with a number
    if str_value and str_value[0].isdigit():
        result['valid'] = False
        result['failed_conditions'].append(f"Must not start with a number, starts with '{str_value[0]}'!")

    # String contains characters other than alpha characters, digits and the hyphen character
    if str_value and not str_value.replace('-', 'x').isalnum():
        result['valid'] = False
        result['failed_conditions'].append("Must not contain any characters other than alpha characters, digits, or hyphens!")

    # String contains a dot character
    if str_value and str_value.find('.') != -1:
        result['valid'] = False
        result['failed_conditions'].append(
            f"Must not contain a dot character, contains at least one, at position {str_value.find('.') + 1}!"
        )

    return result
