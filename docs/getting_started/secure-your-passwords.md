# Simple password security using ansible vault

- [Encrypt a secret string to be used in a variable](#encrypt-a-secret-string-to-be-used-in-a-variable)
- [Run playbook which uses vault-encrypted content](#run-playbook-which-uses-vault-encrypted-content)
- [Encrypt an entire file](#encrypt-an-entire-file)
- [More features and information](#more-features-and-information)

**Always avoid plain text passwords in files or on commandline.**

Since some Ansible automation will require using credentials for various tasks, it is recommended to secure these credentials accordingly.

Ansible vault provides an easy way to comply with security requirements to encrypt secret information.
The following describes a basic scenario.

## Encrypt a secret string to be used in a variable

_Supported since ansible 2.3._

By temporarily writing the password into a text file you avoid the secret to show up in your command history.
Enter your secret password as single string in a file and save it. Make sure there is no unwanted whitespace.

```bash
vi passfile
```

Use ansible-vault to encrypt the string, which it reads from the file. Adding the variable name using `-n` will give you the full variable definition that can be copied directly into your `vars:` section of the playbook or the desired place of your variable definition (group_vars, host_vars, etc.).

```bash
ansible-vault encrypt_string $(cat passfile) -n my_secret_var
```

Ansible-vault will ask to enter a vault password, which is required to decrypt the value during ansible runtime afterwards.  
Consider this the "master key" for your vault-encrypted credentials.

```text
New Vault password:
Confirm New Vault password:
my_secret_var: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          66623764626166333234363863356232376666656634316531363366396331393038396635373138
          6164613062353931336561393334303661363037326433330a356364613261323134323836306462
          66643766393834366232333235333563636334336235666631346532393430626665363665666234
          3431386266383464310a376433646135323663306139333934373431343631613034346235666665
          3236
Encryption successful
```

Save the `my_secret_var` and encrypted multi-line value in your variable definitions and include the definition file as usual.  
The variable can as well be referenced and used by other variables for more flexibility.

```yaml
playbook1_secret_var: "{{ my_secret_var }}"
```

This way the value is only present and managed in one place and can be used by different playbooks.

**Remove the temporary file which contains the plain-text password!**

```bash
rm passfile
```

## Run playbook which uses vault-encrypted content

As soon as a vault-encrypted value is present in your playbook, ansible will require the vault password to be entered for playbook execution.  
Add `--ask-vault` to your `ansible-playbook` command to prompt for this "master key" password and allow secure decryption.

```bash
ansible-playbook tasks_with_secrets.yml [...] --ask-vault
```

_When encrypting multiple values that will be used together, you have to make sure the vault password is the same for each encrypted string. Ansible can only ask for one vault password._

## Encrypt an entire file

You can also encrypt an entire file, e.g. containing multiple secrets.

However, if variables are defined in the file it will encrypt the variable names as well and makes it harder to identify the source definition of a referenced variable.  
Also, encrypting the entire file will require ansible-vault commands to view or edit the contents of the file. A file containing individually encrypted values can be viewed and edited as any other file without uncovering the actual secret value.

`ansible-vault` will prompt for the vault password - either to be created for a new encrypted file, or to be used for decrypting existing content (for view or edit operations).

```bash
ansible-vault encrypt file_containing_secrets.yml

ansible-vault view file_containing_secrets.yml
ansible-vault edit file_containing_secrets.yml
```

This file can be included into a playbook similar to any other file include.  
The playbook will only be usable when the correct vault password is provided to `ansible-playbook` for the runtime, see above.

## More features and information

Vault encryption can also be done through password-files, scripts or automation software which provides secure ways to manage vault credentials.
For more complex ways to use ansible vault encryption/decryption please refer to the documentation.

- [Ansible Vault User Guide](https://docs.ansible.com/ansible/latest/user_guide/vault.html)
- [Ansible Vault CLI Guide](https://docs.ansible.com/ansible/latest/cli/ansible-vault.html)
