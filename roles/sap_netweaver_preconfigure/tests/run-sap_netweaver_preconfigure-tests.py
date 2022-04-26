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

print('Running tests for role sap_netweaver_preconfigure...\n')
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
        'name': 'Run in assert mode on new system. Ignore a final error.',
        'command_line_parameter': '',
        'ignore_error_final': True,
        'compact_assert_output': False,
        'rc': '99',
        'role_vars': [
            {
                'sap_netweaver_preconfigure_assert': True
            }
        ]
    },
    {
        'number': '3',
        'name': 'Run in assert mode on new system, ignore any assert error.',
        'command_line_parameter': '',
        'ignore_error_final': False,
        'compact_assert_output': False,
        'rc': '99',
        'role_vars': [
            {
                'sap_netweaver_preconfigure_assert': True,
                'sap_netweaver_preconfigure_assert_ignore_errors': True
            }
        ]
    },
    {
        'number': '4',
        'name': 'Run in assert mode on new system, compact output, ignore any assert or final error.',
        'command_line_parameter': '',
        'ignore_error_final': True,
        'compact_assert_output': True,
        'rc': '99',
        'role_vars': [
            {
                'sap_netweaver_preconfigure_assert': True,
                'sap_netweaver_preconfigure_assert_ignore_errors': True
            }
        ]
    },
    {
        'number': '5',
        'name': 'Run in normal mode on new system. Do not fail in case not enough swap space is configured.',
        'command_line_parameter': '',
        'ignore_error_final': False,
        'compact_assert_output': False,
        'rc': '99',
        'role_vars': [
            {
                'sap_netweaver_preconfigure_fail_if_not_enough_swap_space_configured': False
            }
        ]
    },
    {
        'number': '6',
        'name': 'Run in check mode on configured system. Ignore a final error.',
        'command_line_parameter': '--check ',
        'ignore_error_final': True,
        'compact_assert_output': False,
        'rc': '99',
        'role_vars': []
    },
    {
        'number': '7',
        'name': 'Run in assert mode on modified system. Ignore a final error.',
        'command_line_parameter': '',
        'ignore_error_final': True,
        'compact_assert_output': False,
        'rc': '99',
        'role_vars': [
            {
                'sap_netweaver_preconfigure_assert': True
            }
        ]
    },
    {
        'number': '8',
        'name': 'Run in assert mode on modified system, compact output, ignore any assert error.',
        'command_line_parameter': '',
        'ignore_error_final': True,
        'compact_assert_output': True,
        'rc': '99',
        'role_vars': [
            {
                'sap_netweaver_preconfigure_assert': True,
                'sap_netweaver_preconfigure_assert_ignore_errors': True
            }
        ]
    }
]

for par1 in __tests:
    print ('\n' + 'Test ' + par1['number'] + ': ' + par1['name'])
    command = ('ansible-playbook sap_netweaver_preconfigure-default-settings.yml '
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

print ('\nResults for role sap_netweaver_preconfigure: ' + _managed_node + ' - RHEL ' + _mn_rhel_release + ' - ' + _mn_hw_arch + ':')

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
