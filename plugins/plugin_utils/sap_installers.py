# SPDX-License-Identifier: Apache-2.0

# Shared validation for SAP installers.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleError

# SAP HANA database lifecycle manager
HDBLCM = 'hdblcm'

# Software Provisioning Manager
SWPM = 'swpm'

SAP_INSTALLERS = [HDBLCM, SWPM]


def assert_known_installer(installer):
    """
    Raise unless installer is None or one of the supported SAP installers.

    None means that only the installer independent criteria are applied, so it
    is always accepted.
    """
    if installer is not None and installer not in SAP_INSTALLERS:
        raise AnsibleError(
            "Unknown installer '%s', expected one of: %s"
            % (installer, ', '.join(SAP_INSTALLERS))
        )
