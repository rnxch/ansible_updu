#!/usr/bin/python
#
# Copyright (C) 2020, Riedo Networks Ltd - All Rights Reserved
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.rnx.updu.plugins.module_utils.network.updu.updu import load_config, write_config

DOCUMENTATION = '''
---
module: updu_config
author: RNX
short_description: Run config commands on RNX UPDU devices
description: 
  Executing commands in the configuration context of a RNX UPDU device. 
  See `CLI reference manual` for command reference on [rnx.ch/support](https://rnx.ch/support) 
notes:
  Following parameters must be set:
  - ansible_network_os=rnx.updu.updu 
  - ansible_connection=network_cli 
  - ansible_user=<DEVICE USERNAME> 
  - ansible_password=<DEVICE PASSWORD> 
options:
  config:
    description:
      - List of commands to be send in the configuration context of the target device.
    required: true
    type: list
    elements: raw
  write:
    description:
      - Whether to save active configuration after config is applied or not.   
    required: false
    default: False
'''

EXAMPLES = """
tasks:
- name: Configure device hostname
  rnx.updu.updu_config:
    config:
      - system
      - hostname rnx-updu-001

- name: Configure outlet names
  rnx.updu.updu_config:
    write: true
    config:
      - object Outlet1.1
      - name SRV01
      - object Outlet1.2
      - name SRV02
      - object Outlet1.3
      - name SWITCH01
"""

RETURN = """
commands:
  description: Executed configuration commands
  returned: always
  type: list
  sample: ['...', '...']
"""

def main():
    argument_spec = dict(
        config=dict(type='list', elements='raw', required=True),
        write=dict(type='bool', default=False),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False
    )

    warnings = list()

    result = {'changed': True}

    if warnings:
        result['warnings'] = warnings

    commands = module.params["config"]
    wr_config: bool = module.params["write"]

    result['commands'] = commands

    if commands:
        if not module.check_mode:
            load_config(module, commands)

    if wr_config:
        write_config(module)

    module.exit_json(**result)


if __name__ == '__main__':
    main()