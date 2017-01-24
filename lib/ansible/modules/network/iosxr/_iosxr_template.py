#!/usr/bin/python
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
ANSIBLE_METADATA = {'status': ['deprecated'],
                    'supported_by': 'community',
                    'version': '1.0'}


DOCUMENTATION = """
---
module: iosxr_template
version_added: "2.1"
author: "Ricardo Carrillo Cruz (@rcarrillocruz)"
short_description: Manage Cisco IOSXR device configurations over SSH
description:
  - Manages network device configurations over SSH.  This module
    allows implementers to work with the device running-config.  It
    provides a way to push a set of commands onto a network device
    by evaluating the current running-config and only pushing configuration
    commands that are not already configured.  The config source can
    be a set of commands or a template.
deprecated: Deprecated in 2.2. Use M(iosxr_config) instead.
extends_documentation_fragment: iosxr
options:
  src:
    description:
      - The path to the config source.  The source can be either a
        file with config or a template that will be merged during
        runtime.  By default the task will first search for the source
        file in role or playbook root folder in templates unless a full
        path to the file is given.
    required: false
    default: null
  force:
    description:
      - The force argument instructs the module not to consider the
        current device running-config.  When set to true, this will
        cause the module to push the contents of I(src) into the device
        without first checking if already configured.
    required: false
    default: false
    choices: [ "true", "false" ]
  backup:
    description:
      - When this argument is configured true, the module will backup
        the running-config from the node prior to making any changes.
        The backup file will be written to backup_{{ hostname }} in
        the root of the playbook directory.
    required: false
    default: false
    choices: [ "true", "false" ]
  config:
    description:
      - The module, by default, will connect to the remote device and
        retrieve the current running-config to use as a base for comparing
        against the contents of source.  There are times when it is not
        desirable to have the task get the current running-config for
        every task.  The I(config) argument allows the implementer to
        pass in the configuration to use as the base config for
        comparison.
    required: false
    default: null
"""

EXAMPLES = """

- name: push a configuration onto the device
  iosxr_template:
    src: config.j2

- name: forceable push a configuration onto the device
  iosxr_template:
    src: config.j2
    force: yes

- name: provide the base configuration for comparison
  iosxr_template:
    src: candidate_config.txt
    config: current_config.txt
"""

RETURN = """
updates:
  description: The set of commands that will be pushed to the remote device
  returned: always
  type: list
  sample: ['...', '...']

start:
  description: The time the job started
  returned: always
  type: str
  sample: "2016-11-16 10:38:15.126146"
end:
  description: The time the job ended
  returned: always
  type: str
  sample: "2016-11-16 10:38:25.595612"
delta:
  description: The time elapsed to perform all operations
  returned: always
  type: str
  sample: "0:00:10.469466"
"""
from ansible.module_utils.local import LocalAnsibleModule
from ansible.module_utils.netcfg import NetworkConfig, dumps
from ansible.module_utils.iosxr import get_config, load_config
from ansible.module_utils.network import NET_TRANSPORT_ARGS, _transitional_argument_spec


def check_args(module):
    warnings = list()
    for key in NET_TRANSPORT_ARGS:
        if module.params[key]:
            warnings.append(
                'network provider arguments are no longer supported.  Please '
                'use connection: network_cli for the task'
            )
            break
    return warnings


def main():
    """ main entry point for module execution
    """

    argument_spec = dict(
        src=dict(),
        force=dict(default=False, type='bool'),
        backup=dict(default=False, type='bool'),
        config=dict(),
    )

    # Removed the use of provider arguments in 2.3 due to network_cli
    # connection plugin.  To be removed in 2.5
    argument_spec.update(_transitional_argument_spec())

    mutually_exclusive = [('config', 'backup'), ('config', 'force')]

    module = LocalAnsibleModule(argument_spec=argument_spec,
                           mutually_exclusive=mutually_exclusive,
                           supports_check_mode=True)

    warnings = check_args(module)

    result = dict(changed=False, warnings=warnings)

    candidate = NetworkConfig(contents=module.params['src'], indent=1)

    if module.params['backup']:
        result['__backup__'] = get_config(module)

    if not module.params['force']:
        contents = get_config(module)
        configobj = NetworkConfig(contents=contents, indent=1)
        commands = candidate.difference(configobj)
        commands = dumps(commands, 'commands').split('\n')
        commands = [str(c).strip() for c in commands if c]
    else:
        commands = [c.strip() for c in str(candidate).split('\n')]

    if commands:
        load_config(module, commands, not module.check_mode)
        result['changed'] = not module.check_mode

    result['updates'] = commands
    module.exit_json(**result)


if __name__ == '__main__':
    main()
