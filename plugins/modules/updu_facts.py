#!/usr/bin/python
#
# Copyright (C) 2020, Riedo Networks Ltd - All Rights Reserved
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = '''
---
module: updu_facts
author: RNX
short_description: Collects facts from remote UPDU devices.
description:
  - Collects device facts
notes:
  Following parameters must be set:
  - ansible_network_os=rnx.updu.updu 
  - ansible_connection=network_cli 
  - ansible_user=<DEVICE USERNAME> 
  - ansible_password=<DEVICE PASSWORD> 
'''

EXAMPLES = '''
# Facts are gathered explicitly using rnx.updu.updu_facts
gather_facts: false

tasks:
  - name: Gather facts
    rnx.updu.updu_facts:
  
  - name: Show facts
    debug:
      var: ansible_facts
'''

RETURN = '''
net_hostname:
  description: Hostname of device
  returned: always
  type: string
net_model:
  description: UPDU model name
  returned: always
  type: string
net_version:
  description: Running firmware version
  returned: failed
  type: string
'''

import platform
import re

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six import iteritems
from ansible_collections.rnx.updu.plugins.module_utils.network.updu.updu import (
    run_commands,
    get_capabilities,
)


class FactsBase(object):

    COMMANDS = list()

    def __init__(self, module):
        self.module = module
        self.facts = dict()
        self.responses = None
        self._capabilities = get_capabilities(self.module)

    def populate(self):
        self.responses = run_commands(
            self.module, commands=self.COMMANDS, check_rc=False
        )

    def run(self, cmd):
        return run_commands(commands=cmd, check_rc=False)

    def parse_facts(self, pattern, data):
        value = None
        match = re.search(pattern, data, re.M)
        if match:
            value = match.group(1)
        return value


class Default(FactsBase):

    COMMANDS = ["show version"]

    def populate(self):
        super(Default, self).populate()
        self.facts.update(self.platform_facts())

    def platform_facts(self):
        platform_facts = {}

        resp = self._capabilities
        device_info = resp["device_info"]

        platform_facts["system"] = device_info["network_os"]

        for item in ("model", "version", "hostname"):
            val = device_info.get("network_os_%s" % item)
            if val:
                platform_facts[item] = val

        platform_facts["api"] = resp["network_api"]
        platform_facts["python_version"] = platform.python_version()

        return platform_facts


FACT_SUBSETS = dict(
    default=Default
)

VALID_SUBSETS = frozenset(FACT_SUBSETS.keys())


def main():
    """main entry point for module execution"""
    argument_spec = dict(
        gather_subset=dict(default=["default"], type="list", elements="str")
    )

    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )

    gather_subset = module.params["gather_subset"]

    runable_subsets = set()
    exclude_subsets = set()

    for subset in gather_subset:
        if subset == "all":
            runable_subsets.update(VALID_SUBSETS)
            continue

        if subset.startswith("!"):
            subset = subset[1:]
            if subset == "all":
                exclude_subsets.update(VALID_SUBSETS)
                continue
            exclude = True
        else:
            exclude = False

        if subset not in VALID_SUBSETS:
            module.fail_json(
                msg="Subset must be one of [%s], got %s"
                % (", ".join(VALID_SUBSETS), subset)
            )

        if exclude:
            exclude_subsets.add(subset)
        else:
            runable_subsets.add(subset)

    if not runable_subsets:
        runable_subsets.update(VALID_SUBSETS)

    runable_subsets.difference_update(exclude_subsets)
    runable_subsets.add("default")

    facts = dict()
    facts["gather_subset"] = list(runable_subsets)

    instances = list()
    for key in runable_subsets:
        instances.append(FACT_SUBSETS[key](module))

    for inst in instances:
        inst.populate()
        facts.update(inst.facts)

    ansible_facts = dict()
    for key, value in iteritems(facts):
        key = "ansible_net_%s" % key
        ansible_facts[key] = value

    module.exit_json(ansible_facts=ansible_facts)


if __name__ == "__main__":
    main()
