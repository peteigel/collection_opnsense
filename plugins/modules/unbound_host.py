#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2023, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/unbound.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.unbound_host import Host

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/unbound_host.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/unbound_host.html'


def run_module():
    module_args = dict(
        hostname=dict(type='str', required=True, aliases=['host', 'h']),
        domain=dict(type='str', required=True, aliases=['dom', 'd']),
        record_type=dict(
            type='str', required=False, aliases=['type', 'rr', 'rt'],
            choices=['A', 'AAAA', 'MX'], default='A',
        ),
        value=dict(type='str', required=False, aliases=['server', 'srv', 'mx']),
        prio=dict(
            type='int', required=False, aliases=['mxprio'], default=10,
            description='Priority that is only used for MX record types'
        ),
        description=dict(type='str', required=False, aliases=['desc']),
        match_fields=dict(
            type='list', required=False, elements='str',
            description='Fields that are used to match configured host-overrides with the running config - '
                        "if any of those fields are changed, the module will think it's a new entry",
            choices=[
                'hostname', 'domain', 'record_type', 'value',
                'prio', 'description'
            ],
            default=['hostname', 'domain', 'record_type', 'value', 'prio'],
        ),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
        **OPN_MOD_ARGS,
    )

    result = dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        }
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    module_wrapper(Host(module=module, result=result))

    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
