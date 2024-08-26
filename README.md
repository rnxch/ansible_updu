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
      ansible_host: 10.0.0.1
      location: "Rack 15 Row 4"
      outlets:
        - key: Outlet1.1
          name: "srv001_A"
          description: "Server 001 PSU A"
          state: off
        - key: Outlet1.2
          name: "srv001_B"
          description: "Server 001 PSU B"
          state: on

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

    - name: "Schedule reboot in one minute if misconfiguring should loose connection"
      rnx.updu.updu_commands:
        commands:
          - reboot in 60

    - name: Configure device hostname
      rnx.updu.updu_config:
        write: yes
        config:
          - system
          - hostname {{inventory_hostname}}
          - snmp
          - syslocation "{{location}}"

    - name: Disable Outlets 1 to 3
      rnx.updu.updu_commands:
        commands:
          - outlet off Outlet1.1
          - outlet off Outlet1.2
          - outlet off Outlet1.3

    - name: Configure Outlet names/descriptions
      rnx.updu.updu_config:
        write: yes
        config:
          - object "{{ item.key }}"
          - name "{{ item.name }}"
          - description "{{ item.description }}"
      with_items: "{{ outlets }}"

    - name: Force Outlets state
      rnx.updu.updu_commands:
        command: outlet {{ 'on' if item.state else 'off' }} {{ item.key }}
      with_items: "{{ outlets }}"


    - name: Cancel scheduled reboot
      rnx.updu.updu_commands:
        command: reboot cancel
```
