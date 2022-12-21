# sap_hana_install Installation testing

Installation testing is done by running:
`# run-sap_hana_install-install-tests.py <managed_node> <username>`
where `managed_node` is the hostname of the host on which SAP HANA installation testing will take place,
and `username` is the name of a user for accessing the managed node. Some basic information is retrieved
from the managed node via `ssh`, for which we need a user name.

The following steps have to be performed to prepare the tests:
- The files mentioned in the tasks `Copy ... to software directory` (e.g. `SAPCAR_1115-70006178.EXE`),
  as well as their sha256 checksum files (e.g. `SAPCAR_1115-70006178.EXE.sha256`), need to be available
  in the directory specified by variable `sap_hana_install_software_directory` in file
  `install-vars.yml`, e.g. `/software/sap_hana_install_test`.
- You can either download or copy these files manually or via Ansible with yml file
  `prepare-install-tests-x86_64.yml` or `prepare-install-tests-ppc64le.yml`.
  In that case, the required files need to be in a directory specified by variable `software_host_directory`,
  followed by the output of `uname -m` (e.g. `/software/hana_store/x86_64`), on a server
  specified by variable `software_host`.

For a SAP HANA scale-out test, the server(s) specified by variable `sap_hana_install_addhosts` in file
`run-install-test-03.yml` (e.g. `node02`) need(s) to have the following file systems mounted from the node on
which the test is run:
- `/hana/data`
- `/hana/log`
- `/hana/shared`

Note: There should be no group named `sapsys` in file `/etc/group` on any of the test system(s), or if
there is one, its group id should match the value of `sap_hana_install_groupid` (default `79`) in file
install-vars.yml.

Each test cycle is running the following steps:
- `ansible-playbook prepare-install-test-NN.yml -l managed_node`
- `ansible-playbook run-install-test-NN.yml [...] -l managed_node -e [...]`
- `ansible-playbook hana-uninstall.yml -l managed_node`

All screen outputs are saved in a newly created directory with the following name pattern:
`hana-install-test-logs-` + rhel_release + `_` + hardware_architecture + `_` + date_time_string

Example:
`hana-install-test-logs-8.4_x86_64_2022-03-06_23:29:34`

For each of the tests, there will be three output files in the log directory (shown with
example file names for the directory mentioned above):
- `hana-install-test-2022-03-06_23:29:34-prepare-01.log`
- `hana-install-test-2022-03-06_23:29:34-run-01.log`
- `hana-install-test-2022-03-06_23:29:34-uninstall-01.log`

and an additional file name at the end of all tests, named
- `hana-install-test-2022-03-06_23:29:34-result.log`

If the return code of a test is `0`, the test has succeeded. If it is not `0` (default is `99`),
the test has failed.

A test succeeds if the string specified in variable `expected_output_string` for each test is found
in the output of the test run.
