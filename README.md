# Ansible Collection - rnx.updu

This collection allows configuration of RNX UPDU devices running firmware 2.4 or greater.

# Requirements

The Python package [Paramiko](https://www.paramiko.org/) is required for successful ssh connection.

# Usage

To install the collection from galaxy use the `ansible-galaxy collection` command:

```
ansible-galaxy collection install rnx.updu
```

# Examples

### Inventory file

Example inventory file

```yml
---
all:
  hosts:
    pdu-rack15-row4:
      ansible_host: 10.2.18.80
  vars:
    ansible_ssh_user: admin
    ansible_ssh_pass: admin
    ansible_network_os: rnx.updu.updu
    ansible_connection: network_cli
```

### Playbook

Example Playbook file

```yml
---
- hosts: all
  tasks:
  - name: Gather facts
    rnx.updu.updu_facts:

  - name: Configure device hostname
    rnx.updu.updu_config:
      config:
        - system
        - hostname {{inventory_hostname}}

  - name: Disable Outlet 1
    rnx.updu.updu_commands:
      commands:
        - outlet off Outlet1.1
```


# Development

## Developing and Testing

Developing and Testing this collection may be done without building and installing
by cloning this repository inside following directory structure:

./collections/ansible_collections/rnx/updu/

```
mkdir -p ./collections/ansible_collections/rnx
cd ./collections/ansible_collections/rnx
git clone [repo url] updu
```

## Building

Building the collection may be done using following `ansible-galaxy` command:

```
ansible-galaxy collection build
```

## Deployment on Galaxy

On every new deployment, the version in the `galaxy.yml` file must be increased.
see [ansible doc on versioning](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_distributing.html#understanding-collection-versioning).


```
ansible-galaxy collection publish rnx-udpu-X.X.X.tar.gz --token <api-token>
```
