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