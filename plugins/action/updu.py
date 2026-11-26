#!/usr/bin/python
#
# Copyright (C) 2020, Riedo Networks Ltd - All Rights Reserved
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible.plugins.action.normal import ActionModule as _NormalAction

class ActionModule(_NormalAction):
    def run(self, tmp=None, task_vars=None):
        connection = (self._play_context.connection or "").split(".")[-1]
        if connection != "network_cli":
            return {
                "failed": True,
                "msg": 'rnx.updu modules expects "ansible_connection: network_cli"',
            }

        return super(ActionModule, self).run(tmp, task_vars)