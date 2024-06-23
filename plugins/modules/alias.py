#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2023, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/firewall.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import RELOAD_MOD_ARG_DEF_FALSE
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.alias import Alias
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.alias import ALIAS_MOD_ARGS

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/alias.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/alias.html'


def run_module():
    module_args = dict(
        **RELOAD_MOD_ARG_DEF_FALSE,  # default-true takes pretty long sometimes (urltables and so on)
        **ALIAS_MOD_ARGS
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

    module_wrapper(Alias(module=module, result=result))

    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
