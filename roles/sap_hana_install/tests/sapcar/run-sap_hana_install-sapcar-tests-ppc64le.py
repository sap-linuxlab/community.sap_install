#!/usr/bin/python3

import os
import sys
import subprocess
import re

# output field delimiter for displaying the results:
_field_delimiter = '\t'

if (len(sys.argv) != 3):
    _managed_node=input("Provide name of managed node: ")
    _username=input("Provide username for connecting to managed node: ")
else:
    _managed_node=sys.argv[1]
    _username=sys.argv[2]

print('Running preinstall tests for role sap_hana_install...\n')
print('Managed node: ' + _managed_node)
print('Username: ' + _username)

_mn_rhel_release = subprocess.getoutput("ssh " + _username + "@" + _managed_node + " cat /etc/redhat-release | awk 'BEGIN{FS=\"release \"}{split ($2, a, \" \"); print a[1]}'")
print('Managed node Red Hat release: ' + _mn_rhel_release)
_mn_hw_arch = subprocess.getoutput("ssh " + _username + "@" + _managed_node + " uname -m")
print('Managed node HW architecture: ' + _mn_hw_arch)

__tests = [
    {
        'number': '01',
        'name': 'SAPCAR checksum test, missing sha256 file',
        'command_line_parameter': '--tags=sap_hana_install_prepare_sapcar ',
        'expected_output_string': 'FAIL: Missing checksum file \'/software/sap_hana_install_test/SAPCAR_1115-70006238.EXE.sha256\'!',
        'rc': '99',
        'role_vars': [
            {
                'sap_hana_install_enforce_checksum_verification': True
            }
        ]
    },
    {
        'number': '02',
        'name': 'SAPCAR checksum test, sha256 file exists but checksum is not correct',
        'command_line_parameter': '--tags=sap_hana_install_prepare_sapcar ',
        'expected_output_string': ' does not match the checksum stored in file \'/software/sap_hana_install_test/SAPCAR_1115-70006238.EXE.sha256\'!',
        'rc': '99',
        'role_vars': [
            {
                'sap_hana_install_enforce_checksum_verification': True
            }
        ]
    },
    {
        'number': '03',
        'name': 'SAPCAR checksum test, sha256 file exists with correct checksum',
        'command_line_parameter': '--tags=sap_hana_install_prepare_sapcar ',
        'expected_output_string': ' matches the checksum stored in file \'/software/sap_hana_install_test/SAPCAR_1115-70006238.EXE.sha256\'.',
        'rc': '99',
        'role_vars': [
            {
                'sap_hana_install_enforce_checksum_verification': True
            }
        ]
    },
    {
        'number': '04',
        'name': 'SAPCAR checksum test, SHA256 file exists but checksum is not correct',
        'command_line_parameter': '--tags=sap_hana_install_prepare_sapcar ',
        'expected_output_string': ' does not match the checksum stored in file \'/software/sap_hana_install_test/SHA256\'!',
        'rc': '99',
        'role_vars': [
            {
                'sap_hana_install_enforce_checksum_verification': True,
                'sap_hana_install_global_checksum_file': "{{ sap_hana_install_software_directory }}/SHA256"
            }
        ]
    },
    {
        'number': '05',
        'name': 'SAPCAR checksum test, SHA256 file exists with correct checksum',
        'command_line_parameter': '--tags=sap_hana_install_prepare_sapcar ',
        'expected_output_string': ' matches the checksum stored in file \'/software/sap_hana_install_test/SHA256\'.',
        'rc': '99',
        'role_vars': [
            {
                'sap_hana_install_enforce_checksum_verification': True,
                'sap_hana_install_global_checksum_file': "{{ sap_hana_install_software_directory }}/SHA256"
            }
        ]
    },
]

#command = ('ansible-playbook prepare-sapcar-tests.yml '
#           + '-l '
#           + _managed_node)
#_py_rc = os.system(command)

for par1 in __tests:
    print ('\n' + 'Test ' + par1['number'] + ': ' + par1['name'])
    command = ('ansible-playbook prepare-test-'
               + par1['number']
               + '-'
               + _mn_hw_arch
               + '.yml '
               + '-l '
               + _managed_node)
    _py_rc = os.system(command)
    command = ('ansible-playbook run-sapcar-test-'
               + _mn_hw_arch
               + '.yml '
               + par1['command_line_parameter']
               + '-l '
               + _managed_node
               + ' '
               + '-e "')
    for par2 in par1['role_vars']:
        command += str(par2)
    command += '"'
    print ("command: " + command)
#    _py_rc = os.system(command)
#    _py_rc = os.popen(command).read()
#    _output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    _output = subprocess.getoutput(command)
    print('Output of test: ' + _output)
    _match = re.search(par1['expected_output_string'], _output)
    if _match:
       par1['rc'] = '0'
       print('Test ' + par1['number'] + ' passed!!!')
#    par1['rc'] = str(int(_py_rc/256))
#    if (_py_rc != 0):
#        if (par1['ignore_error_final'] == True):
#            print('Test ' + par1['number'] + ' finished with return code ' + par1['rc'] + '. Continuing with the next test')
#        else:
#            print('Test ' + par1['number'] + ' finished with return code ' + par1['rc'] + '.')
#            exit(_py_rc)
#    else:
#        print('Test ' + par1['number'] + ' finished with return code ' + par1['rc'] + '.')

print ('\nResults for role sap_hana_install preinstall: ' + _managed_node + ' - RHEL ' + _mn_rhel_release + ' - ' + _mn_hw_arch + ':')

print ('\n#'
       + _field_delimiter
       + 'RC' + _field_delimiter
       + 'name' + _field_delimiter
       + 'argument' + _field_delimiter
       + 'expected error string' + _field_delimiter
       + 'role_vars')

for par1 in __tests:
    print (par1['number'] + _field_delimiter
           + par1['rc'] + _field_delimiter
           + par1['name'] + _field_delimiter
           + '\'' + par1['command_line_parameter'] + '\'' + _field_delimiter
           + '\'' + par1['expected_output_string'] + '\'' + _field_delimiter, end='')
    if (len(par1['role_vars']) == 0):
        print ("")
    else:
        for par2 in par1['role_vars']:
            print (str(par2))

