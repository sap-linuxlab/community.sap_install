# Some testing guidelines

for testing the role without mangling around with a real /etc/hosts file it is possible
to create a test file in the host file format, like the following:

```[bash]
$ cat ./test.hostsfile
127.0.0.1 localhost host1 localhost.localdomain host1.abc.de
1.2.3.5 thishost.to.be.deleted
1.2.3.6 host2
```

Then you can run the role with

```[bash]
ansible-playbook -K test.yml -e __sap_maintain_etc_hosts_file=./test.hostsfile
```

The result should look like:

```[bash]
127.0.0.1 localhost localhost.localdomain
1.2.3.4 host1.abc.de host1  alias1 anotheralias2 # Here comes text after hashsign
```

Please feel free to test with other example host files and report errors accordingly
