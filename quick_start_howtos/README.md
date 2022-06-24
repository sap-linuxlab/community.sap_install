# Collection of samples and tips

In this folder you find sample files, a few additional tips for using the provided ansible roles, as well as references to further information.

1. [How to run playbooks](#how-to-run-playbooks)
1.1 [Basic inventory parameters](#basic-inventory-parameters)
1.2 [Security parameters](#security-parameters)
1.3 [Other useful options](#other-useful-options)

## How to run playbooks

Playbook execution requires a minimum set of parameters, depending on the ansible configuration settings and the environment to be used in.

The parameters shown in the below examples can all be combined according to the respective needs. The examples are kept short for readability.

### Basic inventory parameters

Examples with different ways to use inventory and target system parameters:
```text
ansible-playbook sap_hana_cluster_deploy.yml 

ansible-playbook -i /path/to/inventory-file -l node1,node2 sap_hana_cluster_deploy.yml 
ansible-playbook -l ~node[12] sap_hana_cluster_deploy.yml 
```

### Security parameters

Examples showing some typical privilege escalation options:
```text
ansible-playbook [...] -k
ansible-playbook [...] -k -K
ansible-playbook [...] -u target-user -k -K
```

`-u` is used to target a different remote user than the current user on the ansible control node.
`-k` will prompt for the remote user's login password.
`-K` will prompt for the remote user's sudo password. This is needed when `become` is used to run tasks as another user or root. Instead of sudo the privilege escalation method can also be changed (please see official ansible documentation).

Example if encrypted files or variables are used in a play:
```text
ansible-playbook sap_hana_cluster_deploy.yml --ask-vault
```

This will prompt for the vault password, which was provided during creation of the ansible-vault encrypted contents.

Please see **secure-your-passwords.md** for more information.

### Other useful options

There are also other very useful parameters for individual use cases.

```text
ansible-playbook [...] --list-hosts

ansible-playbook [...] --list-tasks

ansible-playbook [...] -t tasks-tagged-name-a
ansible-playbook [...] -t tasks-tagged-name-a,tasks-tagged-name-b

ansible-playbook [...] --start-at-task "Name of task to start with and proceed"

ansible-playbook [...] -C
ansible-playbook [...] --step
```

These are not all available options, but ones that may help getting familiar with the tasks and changes the playbook would execute. Especially for a collection of complex roles this could help keeping an overview and defining steps, if desired.

* `--list-hosts` helps verifying the hosts that are going to be targeted. The playbook is not run.
* `--list-tasks` displays the tasks the playbook is going to run. Tasks from dynamically included files will not be visible and only accessed during runtime.
* `-t` or `--tags` limits the tasks to be executed to those with the tag name(s) provided. Tags are displayed in square brackets in the `--list-tasks` overview.
* `--start-at-task` will re-run the playbook starting with this named task. If there are duplicate task names it will start at the first in the list (see `--list-tasks`). 
Be careful to choose a task which covers pre-requisites, i.e. tasks that discover information which is used in subsequent tasks have to be run again to fulfill conditionals.
* `-C` attempts a dry-run of the playbook without applying actual changes. This is limited to simple tasks that do not require other changes already been done in previous tasks. 
* `--step` this executes the playbook but will prompt for every task to be run or skipped. At the prompt it can also be told to continue and not ask again, however. Useful to slow down execution and review each tasks result before proceeding with the next task.
