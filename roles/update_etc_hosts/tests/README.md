# Some testing guidelines

for testing the role without mangling around with a real /etc/hosts file it is possible
to create a test file in the host file format, like the following:

```[file]
127.0.0.1 localhost host1
1.2.3.5 thishost.to.be.deleteted
1.2.3.6 host2
```

Then you can run the role with

```[bash]
ansible-playbook test.yml -e _update_etc_hosts_file=./test.hosts
```
