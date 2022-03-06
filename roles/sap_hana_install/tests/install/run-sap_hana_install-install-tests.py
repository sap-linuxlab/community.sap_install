#!/usr/bin/python3

import os
import sys
import datetime
import subprocess
import re
import shlex
import yaml

# output field delimiter for displaying the results:
_field_delimiter = '\t'

if (len(sys.argv) != 3):
    print('Please provide the name of the managed node and the user name for logging in.')
    __managed_node=input('Name of managed node: ')
    __username=input('User name for connecting to managed node: ')
else:
    __managed_node=sys.argv[1]
    __username=sys.argv[2]

__datestr=datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
__logfile_prefix = 'hana-install-test-'

print('Running HANA install tests for role sap_hana_install...\n')
print('Managed node: ' + __managed_node)
print('Username: ' + __username)

with open("install-vars.yml", 'r') as _file:
  __yml_data = yaml.safe_load(_file)

print(__yml_data)
#print('sap_hana_install_sapcar_filename: ' + __yml_data.get('sap_hana_install_sapcar_filename'))
#print('sap_hana_install_sarfiles: ' + str(__yml_data.get('sap_hana_install_sarfiles')[0]))
#print('sap_hana_install_sarfiles: ' + str(__yml_data.get('sap_hana_install_sarfiles')[1]))

#input('Press RETURN to continue: ')

__mn_rhel_release = subprocess.getoutput("ssh " + __username + "@" + __managed_node + " cat /etc/redhat-release | awk 'BEGIN{FS=\"release \"}{split ($2, a, \" \"); print a[1]}'")
__mn_hw_arch = subprocess.getoutput("ssh " + __username + "@" + __managed_node + " uname -m")
print('Managed node Red Hat release: ' + __mn_rhel_release)
print('Managed node HW architecture: ' + __mn_hw_arch)

__logdir = 'hana-install-test-logs-' + __mn_rhel_release + '_' + __mn_hw_arch + '_' + __datestr
print('Logdir: ' + __logdir)
if not os.path.exists(__logdir):
    os.mkdir(__logdir)

__tests = [
    {
        'number': '01',
        'name': 'install test, rev 59.01, default parameters',
        'command_line_parameter': '',
        'expected_output_string': 'SAP HANA deployment successfully completed:',
        'rc': '99',
        'role_vars': [
            {
            }
        ]
    },
    {
        'number': '02',
        'name': 'install test, rev 59.01, check installation, checksum and signature verification',
        'command_line_parameter': '',
        'expected_output_string': 'SAP HANA deployment successfully completed:',
        'rc': '99',
        'role_vars': [
            {
               'sap_hana_install_check_installation': True,
               'sap_hana_install_verify_checksums': True,
               'sap_hana_install_verify_signature': True
            }
        ]
    },
]

# Loop over tests:
for par1 in __tests[0:2]:
    print ('\n' + 'Test ' + par1['number'] + ': ' + par1['name'])
    command = ('ansible-playbook prepare-install-test-'
               + par1['number']
               + '.yml '
               + '-l '
               + __managed_node)
    args = shlex.split(command)
#    _py_rc = os.system(command)
    __logfile=__logdir + '/' + __logfile_prefix + __datestr + '-prepare-' + par1['number'] + '.log'
    with open(__logfile, 'wb') as f:
        process = subprocess.Popen(args, stdout=subprocess.PIPE)
        for line in iter(process.stdout.readline, b''):
            sys.stdout.write(line.decode(sys.stdout.encoding))
            f.write(line)
            f.flush()
    command = ('ansible-playbook run-install-test-'
               + par1['number']
               + '.yml '
               + par1['command_line_parameter']
               + '-l '
               + __managed_node
               + ' '
               + '-e "')
# add all role vars for this test:
    for par2 in par1['role_vars']:
        command += str(par2)
    command += '"'
    print ("command: " + command)
    args = shlex.split(command)
#    _output = subprocess.getoutput(command)
    __logfile=__logdir + '/' + __logfile_prefix + __datestr + '-run-' + par1['number'] + '.log'
    with open(__logfile, 'wb') as f:
        process = subprocess.Popen(args, stdout=subprocess.PIPE)
        for line in iter(process.stdout.readline, b''):
            sys.stdout.write(line.decode(sys.stdout.encoding))
            f.write(line)
            f.flush()
    print('Expected output string: \'' + par1['expected_output_string'] + '\'')
    __match = open(__logfile, 'r').read().find(par1['expected_output_string'])
    print('__match: ' + str(__match))
#    __match = re.search(par1['expected_output_string'], _output)
    if __match >= 0:
       par1['rc'] = '0'
       print('Test ' + par1['number'] + ' passed!!!')
    else:
       print('Test ' + par1['number'] + ' FAILED!!!')

    command = ('ansible-playbook hana-uninstall.yml '
               + '-l '
               + __managed_node)
    args = shlex.split(command)
    __logfile=__logdir + '/' + __logfile_prefix + __datestr + '-uninstall-' + par1['number'] + '.log'
    with open(__logfile, 'wb') as f:
        process = subprocess.Popen(args, stdout=subprocess.PIPE)
        for line in iter(process.stdout.readline, b''):
            sys.stdout.write(line.decode(sys.stdout.encoding))
            f.write(line)
            f.flush()

print ('\nResults for role sap_hana_install preinstall: ' + __managed_node + ' - RHEL ' + __mn_rhel_release + ' - ' + __mn_hw_arch + ':')

print ('\n#'
       + _field_delimiter
       + 'RC' + _field_delimiter
       + 'name' + _field_delimiter
       + 'argument' + _field_delimiter
       + 'expected output string' + _field_delimiter
       + 'role_vars')

for par1 in __tests[0:2]:
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

