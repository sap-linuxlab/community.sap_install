#!/usr/bin/env python

"""
Tests for role sap_general_preconfigure
"""

import os
import sys
import subprocess

# output field delimiter for displaying the results:
# FIELD_DELIMITER = ';'
FIELD_DELIMITER = '\t'

if len(sys.argv) == 1:
    _managed_node = input("Provide name of managed node: ")
else:
    _managed_node = sys.argv[1]

print('Running tests for role sap_general_preconfigure...\n')
print('Managed node: ' + _managed_node)

_mn_rhel_release = subprocess.getoutput(
    "ssh root@"
    + _managed_node
    + " cat /etc/redhat-release | \
      awk 'BEGIN{FS=\"release \"}{split($2, a, \" \"); print a[1]}'")
print('Managed node Red Hat release: ' + _mn_rhel_release)
_mn_hw_arch = subprocess.getoutput("ssh root@" + _managed_node + " uname -m")
print('Managed node HW architecture: ' + _mn_hw_arch)

__tests = [
    {
        'number': '1',
        'name': 'Run in check mode on new system.',
        'command_line_parameter': '--check ',
        'ignore_error_final': True,
        'compact_assert_output': False,
        'rc': '99',
        'role_vars': [
            {
               'sap_general_preconfigure_fail_if_reboot_required': False,
            }
        ]
    },
    {
        'number': '2',
        'name': 'Run in assert mode on new system, \
                 check for enabled repos and for minor release lock, \
                 check for possible RHEL update, \
                 ignore assert errors.',
        'command_line_parameter': '',
        'ignore_error_final': False,
        'compact_assert_output': False,
        'rc': '99',
        'role_vars': [
            {
                'sap_general_preconfigure_assert': True,
                'sap_general_preconfigure_assert_ignore_errors': True,
                'sap_general_preconfigure_update': True,
                'sap_general_preconfigure_enable_repos': True,
                'sap_general_preconfigure_set_minor_release': True,
            }
        ]
    },
    {
        'number': '3',
        'name': 'Run in normal mode on new system, \
                 enable repos and set minor release lock, \
                 check for possible RHEL update, \
                 set SELinux to permisive, \
                 allow a reboot.',
        'command_line_parameter': '',
        'ignore_error_final': False,
        'compact_assert_output': False,
        'rc': '99',
        'role_vars': [
            {
                'sap_general_preconfigure_update': True,
                'sap_general_preconfigure_enable_repos': True,
                'sap_general_preconfigure_set_minor_release': True,
                'sap_general_preconfigure_selinux_state': 'permissive',
                'sap_general_preconfigure_reboot_ok': True,
            }
        ]
    },
    {
        'number': '4',
        'name': 'Idempotency check: Run in normal mode on modified system, \
                 enable repos and set minor release lock, \
                 check for possible RHEL update, \
                 set SELinux to permisive, \
                 allow a reboot.',
        'command_line_parameter': '',
        'ignore_error_final': False,
        'compact_assert_output': False,
        'rc': '99',
        'role_vars': [
            {
                'sap_general_preconfigure_update': True,
                'sap_general_preconfigure_enable_repos': True,
                'sap_general_preconfigure_set_minor_release': True,
                'sap_general_preconfigure_selinux_state': 'permissive',
                'sap_general_preconfigure_reboot_ok': True,
            }
        ]
    },
    {
        'number': '5',
        'name': 'Run in assert mode on modified system, \
                 check for repos and for the RHEL minor release lock, \
                 check for possible RHEL update, \
                 check if SELinux is permisive, \
                 ignore any assert error.',
        'command_line_parameter': '',
        'ignore_error_final': False,
        'compact_assert_output': True,
        'rc': '99',
        'role_vars': [
            {
                'sap_general_preconfigure_assert': True,
                'sap_general_preconfigure_assert_ignore_errors': True,
                'sap_general_preconfigure_update': True,
                'sap_general_preconfigure_enable_repos': True,
                'sap_general_preconfigure_set_minor_release': True,
                'sap_general_preconfigure_selinux_state': 'permissive',
            }
        ]
    },
    {
        'number': '6',
        'name': 'Run in check mode on modified system.',
        'command_line_parameter': '--check ',
        'ignore_error_final': True,
        'compact_assert_output': False,
        'rc': '99',
        'role_vars': []
    },
]

for par1 in __tests:
    print('\n' + 'Test ' + par1['number'] + ': ' + par1['name'])
    command = (
        'ansible-playbook sap_general_preconfigure-default-settings.yml '
        + par1['command_line_parameter']
        + '-l '
        + _managed_node
        + ' '
        + '-e "'
    )
    for par2 in par1['role_vars']:
        command += str(par2)
    command += '"'
    if par1['compact_assert_output']:
        command += ' | ./beautify-assert-output.sh'
    print("command: " + command)
    _py_rc = os.system(command)
    par1['rc'] = str(int(_py_rc / 256))
    if _py_rc != 0:
        if par1['ignore_error_final']:
            print('Test '
                  + par1['number']
                  + ' finished with return code '
                  + par1['rc'] + '. Continuing with the next test')
        else:
            print('Test '
                  + par1['number']
                  + ' finished with return code '
                  + par1['rc'] + '.')
            sys.exit(_py_rc)
    else:
        print('Test ' + par1['number'] + ' finished with return code ' + par1['rc'] + '.')

print('\nResults for role sap_general_preconfigure: '
      + _managed_node
      + ' - RHEL '
      + _mn_rhel_release
      + ' - '
      + _mn_hw_arch + ':')

print('\n#'
      + FIELD_DELIMITER
      + 'RC' + FIELD_DELIMITER
      + 'name' + FIELD_DELIMITER
      + 'argument' + FIELD_DELIMITER
      + 'compact' + FIELD_DELIMITER
      + 'role_vars')

for par1 in __tests:
    print(par1['number'] + FIELD_DELIMITER
          + par1['rc'] + FIELD_DELIMITER
          + par1['name'] + FIELD_DELIMITER
          + par1['command_line_parameter'] + FIELD_DELIMITER
          + str(par1['compact_assert_output']) + FIELD_DELIMITER, end='')
    if len(par1['role_vars']) == 0:
        print("")
    else:
        for par2 in par1['role_vars']:
            print(str(par2))
