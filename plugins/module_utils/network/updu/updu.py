#!/usr/bin/python
#
# Copyright (C) 2020, Riedo Networks Ltd - All Rights Reserved
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import platform
import re
import json

from ansible.module_utils.connection import Connection, ConnectionError
from ansible.module_utils._text import to_text

def load_config(module, commands):
    connection = get_connection(module)
    connection.edit_config(commands)

def write_config(module):
    connection = get_connection(module)
    try:
        return connection.run_commands(commands=["write"], check_rc=True)
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))


def get_capabilities(module):
    if hasattr(module, "_updu_capabilities"):
        return module._updu_capabilities
    try:
        capabilities = Connection(module._socket_path).get_capabilities()
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc, errors="surrogate_then_replace"))
    module._updu_capabilities = json.loads(capabilities)
    return module._updu_capabilities


def run_commands(module, commands, check_rc=True):
    connection = get_connection(module)
    try:
        return connection.run_commands(commands=commands, check_rc=check_rc)
    except ConnectionError as exc:
        module.fail_json(msg=to_text(exc))


def get_connection(module):
    if hasattr(module, "_updu_connection"):
        return module._updu_connection

    capabilities = get_capabilities(module)
    network_api = capabilities.get("network_api")
    if network_api == "cliconf":
        module._updu_connection = Connection(module._socket_path)
    else:
        module.fail_json(msg="Invalid connection type %s" % network_api)

    return module._updu_connection
