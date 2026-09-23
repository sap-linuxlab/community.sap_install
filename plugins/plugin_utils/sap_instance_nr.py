# SPDX-License-Identifier: Apache-2.0

# Shared plugin_utils for SAP instance number validation.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.community.sap_install.plugins.plugin_utils.sap_installers import (
    HDBLCM,
    assert_known_installer,
)

# Minimum and maximum accepted instance numbers for 'hdblcm'.
# Source is not SAP Note, but installation guide:
# 'SAP HANA Cockpit Installation and Update Guide'
#
# SWPM does not restrict the instance number beyond it being two digits.
SAP_INSTANCE_NR_RANGE = {
    HDBLCM: (0, 97),
}


def validate_sap_instance_nr(value, installer=None):
    """
    Validate an SAP instance number and return detailed failure information.

    Installer independent criteria, always applied:
    1. Must be a string
    2. Must not have leading or trailing whitespace
    3. Must be exactly 2 characters
    4. Must consist of digits only

    When installer is given, the instance number is additionally checked
    against the range that installer permits, where one applies.

    Returns a dict consisting of a 'valid' boolean and a list of
    'failed_conditions'.
    """
    assert_known_installer(installer)

    result = {
        'valid': True,
        'failed_conditions': []
    }

    if not isinstance(value, str):
        result['valid'] = False
        result['failed_conditions'].append(
            f"Must be a string, got {type(value).__name__} '{value}'. "
            f"Quote the value to keep it a string and to preserve a leading zero!"
        )
        return result

    # Convert to regular string to handle AnsibleUnsafeText
    str_value = str(value)

    # Leading or trailing whitespace
    if str_value != str_value.strip():
        result['valid'] = False
        result['failed_conditions'].append(
            f"Must not have leading or trailing whitespace, got '{str_value}'!"
        )

    stripped = str_value.strip()

    # Wrong length
    if len(stripped) != 2:
        result['valid'] = False
        result['failed_conditions'].append(
            f"Length must be exactly 2 characters, got {len(stripped)}!"
        )

    # Contains characters other than digits.
    # isdigit() accepts superscripts and other numeric characters that int()
    # rejects, so the permitted characters are spelled out instead.
    if stripped and not all(char in '0123456789' for char in stripped):
        result['valid'] = False
        result['failed_conditions'].append(
            f"Must consist of digits only, got '{stripped}'!"
        )
        return result

    # Outside the range permitted by the installer
    installer_range = SAP_INSTANCE_NR_RANGE.get(installer)
    if installer_range is not None and stripped:
        minimum, maximum = installer_range
        if not minimum <= int(stripped) <= maximum:
            result['valid'] = False
            result['failed_conditions'].append(
                f"Must be between {minimum:02d} and {maximum:02d} for {installer}, "
                f"got '{stripped}'!"
            )

    return result
