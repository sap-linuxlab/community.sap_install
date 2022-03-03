#!/usr/bin/python3

import os
import sys
import subprocess

# output field delimiter for displaying the results:
_field_delimiter = '\t'

if (len(sys.argv) == 1):
    _managed_node=input("Provide name of managed node: ")
else:
    _managed_node=sys.argv[1]

print('Running tests for role sap_general_preconfigure...\n')
print('Managed node: ' + _managed_node)

_mn_rhel_release = subprocess.getoutput("ssh root@" + _managed_node + " cat /etc/redhat-release | awk 'BEGIN{FS=\"release \"}{split ($2, a, \" \"); print a[1]}'")
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
        'role_vars': []
    },
    {
        'number': '2',
        'name': 'Run in assert mode on new system, check for enabled repos and for minor release lock, check for possible RHEL update, ignore any assert error.',
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
                'sap_general_preconfigure_set_minor_release': True
            }
        ]
    },
    {
        'number': '3',
        'name': 'Run in normal mode on new system, no reboot.',
        'command_line_parameter': '',
        'ignore_error_final': False,
        'compact_assert_output': False,
        'rc': '99',
        'role_vars': [
            {
                'sap_general_preconfigure_fail_if_reboot_required': False
            }
        ]
    },
    {
        'number': '4',
        'name': 'Run in normal mode on modified system, enable repos and set minor release lock, check for possible RHEL update, set SELinux to permisive, allow a reboot.',
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
                'sap_general_preconfigure_reboot_ok': True
            }
        ]
    },
    {
        'number': '5',
        'name': 'Run in assert mode on modified system, enable repos and set minor release lock, check for possible RHEL update, set SELinux to permisive, ignore any assert errors.',
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
                'sap_general_preconfigure_selinux_state': 'permissive'
            }
        ]
    },
    {
        'number': '6',
        'name': 'Run in assert mode on modified system, enable repos and set minor release lock, check for possible RHEL update, set SELinux to permisive, ignore any assert errors.',
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
                'sap_general_preconfigure_selinux_state': 'permissive'
            }
        ]
    },
]

for par1 in __tests:
    print ('\n' + 'Test ' + par1['number'] + ': ' + par1['name'])
    command = ('ansible-playbook sap_general_preconfigure-default-settings.yml '
               + par1['command_line_parameter']
               + '-l '
               + _managed_node
               + ' '
               + '-e "')
    for par2 in par1['role_vars']:
        command += str(par2)
    command += '"'
    if (par1['compact_assert_output'] == True):
        command += ' | ../tools/beautify-assert-output.sh'
    print ("command: " + command)
    _py_rc = os.system(command)
    par1['rc'] = str(int(_py_rc/256))
    if (_py_rc != 0):
        if (par1['ignore_error_final'] == True):
            print('Test ' + par1['number'] + ' finished with return code ' + par1['rc'] + '. Continuing with the next test')
        else:
            print('Test ' + par1['number'] + ' finished with return code ' + par1['rc'] + '.')
            exit(_py_rc)
    else:
        print('Test ' + par1['number'] + ' finished with return code ' + par1['rc'] + '.')

print ('\nResults for role sap_general_preconfigure: ' + _managed_node + ' - RHEL ' + _mn_rhel_release + ' - ' + _mn_hw_arch + ':')

print ('\n#'
       + _field_delimiter
       + 'RC' + _field_delimiter
       + 'name' + _field_delimiter
       + 'argument' + _field_delimiter
       + 'compact' + _field_delimiter
       + 'role_vars')

for par1 in __tests:
    print (par1['number'] + _field_delimiter
           + par1['rc'] + _field_delimiter
           + par1['name'] + _field_delimiter
           + par1['command_line_parameter'] + _field_delimiter
           + str(par1['compact_assert_output']) + _field_delimiter, end='')
    if (len(par1['role_vars']) == 0):
        print ("")
    else:
        for par2 in par1['role_vars']:
            print (str(par2))
