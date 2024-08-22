#!/usr/bin/python
#
# Copyright (C) 2020, Riedo Networks Ltd - All Rights Reserved
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re
from ansible.plugins.terminal import TerminalBase

class TerminalModule(TerminalBase):

    terminal_stdout_re = [
        re.compile(br'>\ |#\ |\$\ ')
    ]

    terminal_stderr_re = [
        re.compile(br"connection timed out", re.I),
    ]

