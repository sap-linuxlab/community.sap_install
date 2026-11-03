# SPDX-License-Identifier: Apache-2.0

# Shared plugin_utils for building the list of OS specific vars files.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re
from typing import Any, Dict, List

from ansible.errors import AnsibleError

# Characters outside this set are replaced, so that no fact value can
# change the directory a vars file is looked up in.
_UNSAFE_CHARACTERS = re.compile(r'[^A-Za-z0-9._-]')


def _clean(value: Any) -> str:
    """Return value as a string that is safe to use in a file name."""
    return _UNSAFE_CHARACTERS.sub('_', str(value or '').strip())


def get_sap_os_vars_files(facts: Dict[str, Any]) -> List[str]:
    """
    Return the vars file names for the OS described by facts.

    The names are ordered from least to most specific, so that loading
    them in order lets the more specific file override the less specific:
    1. OS family, e.g. Suse.yml
    2. Distribution, e.g. SLES_SAP.yml
    3. Shared SLES and SLES_SAP major release, e.g. SLES_16.yml
    4. Distribution and major release, e.g. SLES_SAP_16.yml
    5. RedHat only, every minor release up to the current one,
       e.g. RedHat_9.1.plus.yml, RedHat_9.2.plus.yml
    6. Shared SLES and SLES_SAP minor release, e.g. SLES_15.7.yml
    7. Distribution and minor release, e.g. SLES_SAP_15.7.yml

    Rolling releases, whose version has no minor part, end up with a
    single version file, e.g. openSUSE_Tumbleweed_20260806.yml.

    Raises error when the OS family or the distribution is unknown, as this
    points to disabled fact gathering or an unsupported OS. The version
    facts are optional, their files are left out when they are missing.
    """
    if not isinstance(facts, dict):
        raise AnsibleError(
            "Expected the Ansible facts as a dict, got %s"
            % type(facts).__name__
        )

    family = _clean(facts.get('os_family'))
    distribution = _clean(facts.get('distribution'))
    if not family or not distribution:
        raise AnsibleError(
            "The facts 'os_family' and 'distribution' are required, "
            "check that fact gathering is enabled and the OS is supported"
        )

    major = _clean(facts.get('distribution_major_version'))
    version = _clean(facts.get('distribution_version'))

    # Enables sharing vars between SLES and SLES_SAP. SLES_SAP is built on
    # top of SLES, so the part before the first underscore is the base
    # distribution: 'SLES' for 'SLES_SAP', unchanged for 'SLES' or 'RedHat'.
    # Its files are listed before the ones of the distribution itself, so
    # SLES_SAP can override what it shares with SLES. The raw fact is split,
    # as cleaning turns the space of 'openSUSE Tumbleweed' into an underscore.
    shared = _clean(str(facts.get('distribution')).split('_', maxsplit=1)[0])

    # File names are built by joining the parts with an underscore,
    # e.g. '%s_%s' % ('SLES_SAP', '15') results in 'SLES_SAP_15'.
    names = [family, distribution]
    if major:
        if shared != distribution:
            names.append('%s_%s' % (shared, major))
        names.append('%s_%s' % (distribution, major))

    # RedHat only: '.plus' files hold vars that are valid for a minor release
    # and all later ones. For RHEL 9.2 the files for 9.1 and 9.2 are listed,
    # so a file is picked up by every minor release from its own onwards.
    # The minor release is the part between the first and second dot of the
    # version, e.g. '2' in '9.2'. A version without a dot, such as the date
    # of a rolling release, has none.
    minor = version.partition('.')[2].partition('.')[0]
    if distribution == 'RedHat' and major and minor.isdigit():
        names.extend(
            '%s_%s.%d.plus' % (distribution, major, number)
            for number in range(1, int(minor) + 1)
        )

    if version:
        if shared != distribution:
            names.append('%s_%s' % (shared, version))
        names.append('%s_%s' % (distribution, version))

    # Drop duplicates but keep the order, as the order sets the precedence.
    return ['%s.yml' % name for name in dict.fromkeys(names)]
