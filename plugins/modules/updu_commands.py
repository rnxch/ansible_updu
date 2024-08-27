#!/usr/bin/python
#
# Copyright (C) 2020, Riedo Networks Ltd - All Rights Reserved
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

from ansible_collections.rnx.updu.plugins.module_utils.network.updu.updu import run_commands
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six import string_types

__metaclass__ = type

DOCUMENTATION = '''
---
module: updu_commands
author: RNX
short_description: Run commands on RNX UPDU devices
description: 
  "Executing commands on a RNX UPDU device. 
  See `CLI reference manual` for command reference on https://rnx.ch/support" 
notes:
  - "Following parameters must be set:"
  - ansible_network_os=rnx.updu.updu 
  - ansible_connection=network_cli 
  - ansible_user=<DEVICE USERNAME> 
  - ansible_password=<DEVICE PASSWORD> 
options:
  commands:
    description:
      - List of commands to be send to the target device.
    required: false
    type: list
    elements: raw
  command:
    description:
      - Single command to be send to the target device.
    required: false
    type: string
'''

EXAMPLES = """
- name: Configure device hostname
  rnx.updu.updu_config:
    config:
      - system
      - hostname rnx-updu-001

- name: Configure outlet names
  rnx.updu.updu_config:
    config:
      - object Outlet1.1
      - name SRV01
      - object Outlet1.2
      - name SRV02
      - object Outlet1.3
      - name SWITCH01

# Store RNX UPDU configuration in file
- name: Get Config
  register: config_save
  rnx.updu.updu_commands:
    command: "show config all"

- name: store config file
  local_action:
    module: copy
    content: "{{config_save.stdout}}"
    dest: "{{inventory_hostname}}.txt"
"""

RETURN = """
stdout:
  description: Output of command
  returned: always
  type: list or string depends on which option was used
  sample: "['...', '...'] or '...'"
stdout_lines:
  description: Output of command
  returned: always
  type: list
  sample: "['...', '...']"
"""

def to_lines(stdout):
    for item in stdout:
        if isinstance(item, string_types):
            item = str(item).replace('\t', '    ').split('\n')
        yield item


def main():
    argument_spec = dict(
        command=dict(type='str', required=False),
        commands=dict(type='list', elements='raw', required=False),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False
    )

    result = {}

    commands = module.params["commands"]

    if commands:
        result['warnings'] = list()

        responses = run_commands(module, commands)

        result.update({
            'changed': True,
            'stdout': responses,
            'stdout_lines': list(to_lines(responses))
        })
    else:
        command = module.params["command"]
        result['warnings'] = list()
        responses = run_commands(module, command)
        result.update({
            'changed': True,
            'stdout': responses[0],
            'stdout_lines': list(responses)
        })

    module.exit_json(**result)


if __name__ == '__main__':
    main()