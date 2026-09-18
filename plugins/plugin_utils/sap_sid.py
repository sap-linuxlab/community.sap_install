# SPDX-License-Identifier: Apache-2.0

# Shared plugin_utils for SAP System ID validation.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.community.sap_install.plugins.plugin_utils.sap_installers import (
    HDBLCM,
    SWPM,
    assert_known_installer,
)

# List of reserved SIDs for 'hdblcm'.
# Source is not SAP Note, but installation guide:
# 'SAP HANA Cockpit Installation and Update Guide'
# This is separate list from SWPM, because they are not identical.
SAP_SID_RESERVED_HDBLCM = [
    'ADD', 'ALL', 'AMD', 'AND', 'ANY', 'ARE', 'ASC', 'AUX', 'AVG', 'BIT',
    'CDC', 'COM', 'CON', 'DBA', 'END', 'EPS', 'FOR', 'GET', 'GID', 'IBM',
    'INT', 'KEY', 'LOG', 'LPT', 'MAP', 'MAX', 'MIN', 'MON', 'NIX', 'NOT',
    'NUL', 'OFF', 'OLD', 'OMS', 'OUT', 'PAD', 'PRN', 'RAW', 'REF', 'ROW',
    'SAP', 'SET', 'SGA', 'SHG', 'SID', 'SQL', 'SUM', 'SYS', 'TMP', 'TOP',
    'UID', 'USE', 'USR', 'VAR',
]

# List of reserved SIDs for 'SWPM'.
# Source: SAP Note 1979280 version 24 (2026/01/08)
SAP_SID_RESERVED_SWPM = [
    'ADD', 'ADM', 'ALL', 'AMD', 'AND', 'ANY', 'ARE', 'ASC', 'AUX', 'AVG',
    'BIN', 'BIT', 'CDC', 'COM', 'CON', 'DAA', 'DBA', 'DBM', 'DBO', 'DTD',
    'ECO', 'END', 'EPS', 'EXE', 'FOR', 'GET', 'GID', 'IBM', 'INT', 'KEY',
    'LIB', 'LOG', 'LPT', 'MAP', 'MAX', 'MEM', 'MIG', 'MIN', 'MON', 'NET',
    'NIX', 'NOT', 'NUL', 'OFF', 'OLD', 'OMS', 'OUT', 'PAD', 'PRN', 'RAW',
    'REF', 'ROW', 'SAP', 'SET', 'SGA', 'SHG', 'SID', 'SQL', 'SUM', 'SYS',
    'TMP', 'TOP', 'TRC', 'UID', 'USE', 'USR', 'VAR',
]

SAP_SID_RESERVED = {
    HDBLCM: SAP_SID_RESERVED_HDBLCM,
    SWPM: SAP_SID_RESERVED_SWPM,
}


def validate_sap_sid(value, installer=None):
    """
    Validate an SAP System ID and return detailed failure information.

    Installer independent criteria, always applied:
    1. Must be a string
    2. Must not have leading or trailing whitespace
    3. Must be exactly 3 characters
    4. Must not start with a digit
    5. Must consist of alpha characters and digits only

    When installer is given, the SAP System ID is additionally checked against
    that installer's list of reserved SAP System IDs. The comparison is made on
    the uppercased value, so a lowercase SAP System ID is matched against the
    list as well.

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
            f"Must be a string, got {type(value).__name__} '{value}'!"
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
    if len(stripped) != 3:
        result['valid'] = False
        result['failed_conditions'].append(
            f"Length must be exactly 3 characters, got {len(stripped)}!"
        )

    # Starts with a digit
    if stripped and stripped[0].isdigit():
        result['valid'] = False
        result['failed_conditions'].append(
            f"Must not start with a number, starts with '{stripped[0]}'!"
        )

    # Contains characters other than alpha characters and digits
    if stripped and not stripped.isalnum():
        result['valid'] = False
        result['failed_conditions'].append(
            "Must not contain any characters other than alpha characters or digits!"
        )

    # Reserved by the installer
    if installer is not None and stripped.upper() in SAP_SID_RESERVED[installer]:
        result['valid'] = False
        result['failed_conditions'].append(
            f"Must not be a SAP System ID reserved by {installer}, "
            f"but '{stripped}' is reserved!"
        )

    return result
