#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2023, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/firmware.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import OPN_MOD_ARGS
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.system import wait_for_response, \
        wait_for_update

except MODULE_EXCEPTIONS:
    module_dependency_error()

# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/package.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/package.html'


def run_module():
    module_args = dict(
        action=dict(
            type='str', required=True,
            choices=['poweroff', 'reboot', 'update', 'upgrade', 'audit']
        ),
        wait=dict(type='bool', required=False, default=True),
        wait_timeout=dict(type='int', required=False, default=90),
        poll_interval=dict(type='int', required=False, default=2),
        **OPN_MOD_ARGS
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    result = {
        'changed': True,
        'failed': False,
        'timeout_exceeded': False,
    }

    if not module.check_mode:
        with Session(module=module) as s:
            s.post({
                'command': module.params['action'],
                'module': 'core',
                'controller': 'firmware',
            })

            if module.params['wait']:
                if module.params['debug']:
                    module.warn(f"Waiting for firewall to complete '{module.params['action']}'!")

                try:
                    if module.params['action'] in ['upgrade', 'update']:
                        result['failed'] = not wait_for_update(module=module, s=s)

                    elif module.params['action'] == 'reboot':
                        result['failed'] = not wait_for_response(module=module)

                except TimeoutError:
                    result['timeout_exceeded'] = True

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
