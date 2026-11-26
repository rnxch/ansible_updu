#!/usr/bin/python
#
# Copyright (C) 2020, Riedo Networks Ltd - All Rights Reserved
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
from ansible.errors import AnsibleConnectionFailure
__metaclass__ = type

import re
from ansible.plugins.terminal import TerminalBase

class TerminalModule(TerminalBase):

    INITIAL_DIALOG_RE = re.compile(
        br'Press ENTER to start an initial configuration dialog',
        re.I
    )

    terminal_stdout_re = [
        re.compile(br'(\S+>|\S+\([^)]+\)#) '),
        INITIAL_DIALOG_RE
    ]

    terminal_stderr_re = [
        re.compile(br"connection timed out", re.I),
    ]

    def on_open_shell(self):
        prompt = self._get_prompt()
        if prompt and self.INITIAL_DIALOG_RE.search(prompt):
            raise AnsibleConnectionFailure(
                "The device has not been configured yet. Connect to it directly "
                "and complete the initial configuration dialog, then run the playbook again."
            )
