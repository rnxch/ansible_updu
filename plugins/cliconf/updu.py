#!/usr/bin/python
#
# Copyright (C) 2020, Riedo Networks Ltd - All Rights Reserved
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
author: RNX
cliconf: updu
short_description: Use updu cliconf to run commands on RNX UPDUs
description:
- Send/receive CLI commands to RNX UPDU devices.
"""

import re
import json

from itertools import chain

from ansible.module_utils._text import to_bytes, to_text
from ansible.module_utils.common._collections_compat import Mapping
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import to_list
from ansible.plugins.cliconf import CliconfBase, enable_mode

class Cliconf(CliconfBase):
    def get_device_info(self):
        device_info = {}

        device_info["network_os"] = "updu"

        data = to_text(self.get(b"show config | section hostname"), errors="surrogate_or_strict").strip()
        match = re.search(r"hostname\s(\S+)", data, re.M)
        if match:
            device_info["network_os_hostname"] = match.group(1)

        reply = self.get(b"show version")
        data = to_text(reply, errors="surrogate_or_strict").strip()

        match = re.search(r"^PDU model:\s+(\S+)", data, re.M)
        if match:
            device_info["network_os_model"] = match.group(1)

        match = re.search(r"^Running UPDU firmware:\s+(\S+)", data, re.M)
        if match:
            device_info["network_os_version"] = match.group(1)

        return device_info

    # @enable_mode
    def get_config(self, source="running", format="text", flags=None):
        cmd = "show config"
        return self.send_command(cmd)

    # @enable_mode
    def edit_config(self,candidate=None, commit=True, replace=None, diff=False, comment=None):
        resp = {}
        results = []
        requests = []

        if commit:
            self.send_command(b'configure')
            for line in to_list(candidate):
                if not isinstance(line, Mapping):
                    line = {"command": line}

                cmd = line["command"]
                if cmd != "end" and cmd[0] != "#":
                    res = self.send_command(**line)
                    if res and "ERR:" in res:
                        raise Exception(f"[{cmd}] {res}")
                    results.append(res)
                    requests.append(cmd)

            self.send_command(b'end')
        else:
            raise ValueError("check mode is not supported")

        resp["request"] = requests
        resp["response"] = results
        return resp

    def get(self, command, prompt=None, answer=None, sendonly=False, newline=True, check_all=False):
        res = self.send_command(command=command, prompt=prompt, answer=answer, sendonly=sendonly, newline=newline, check_all=check_all)
        if res and "ERR:" in res:
            raise Exception(f"[{command}] {res}")
        return res

    def get_device_operations(self):
        return {
            "supports_diff_replace": False,
            "supports_commit": False,
            "supports_rollback": False,
            "supports_defaults": False,
            "supports_onbox_diff": True,
            "supports_commit_comment": False,
            "supports_multiline_delimiter": False,
            "supports_diff_match": False,
            "supports_diff_ignore_lines": False,
            "supports_generate_diff": False,
            "supports_replace": False,
        }

    def get_option_values(self):
        return {
            "format": ["text"],
            "diff_match": ["line", "strict", "exact", "none"],
            "diff_replace": ["line", "block"],
            "output": [],
        }

    def get_capabilities(self):
        result = super(Cliconf, self).get_capabilities()
        result["rpc"] += ["run_commands"]
        result["device_operations"] = self.get_device_operations()
        result.update(self.get_option_values())
        return json.dumps(result)

    def run_commands(self, commands=None, check_rc=True):
        if commands is None:
            raise ValueError("'commands' value is required")

        responses = list()
        for cmd in to_list(commands):
            if not isinstance(cmd, Mapping):
                cmd = {"command": cmd}

            output = cmd.pop("output", None)
            if output:
                raise ValueError(
                    "'output' value %s is not supported for run_commands"
                    % output
                )

            try:
                out = self.send_command(**cmd)
            except AnsibleConnectionFailure as e:
                if check_rc:
                    raise
                out = getattr(e, "err", to_text(e))

            if out and "ERR:" in out:
                raise Exception(f"[{cmd}] {out}")

            responses.append(out)

        return responses
