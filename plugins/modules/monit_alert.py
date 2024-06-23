#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2023, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/monit.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
        diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.monit_alert import Alert

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/monit.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/monit.html'


def run_module():
    module_args = dict(
        recipient=dict(
            type='str', required=True, aliases=['email', 'mail'],
            description='The email address to send alerts to',
        ),
        not_on=dict(
            type='bool', required=False, default=False, aliases=['not'],
            description='Do not send alerts for the following events but on all others',
        ),
        events=dict(
            type='list', elements='str', required=False, default=[],
            choices=[
                'action', 'checksum', 'bytein', 'byteout', 'connection', 'content',
                'data', 'exec', 'fsflags', 'gid', 'icmp', 'instance', 'invalid',
                'link', 'nonexist', 'packetin', 'packetout', 'permission', 'pid',
                'ppid', 'resource', 'saturation', 'size',  'speed', 'status',
                'timeout', 'timestamp', 'uid', 'uptime'
            ],
            description="Values: "
                        "'action' = 'Action done', "
                        "'checksum' = 'Checksum failed', "
                        "'bytein' = 'Download bytes exceeded', "
                        "'byteout' = 'Upload bytes exceeded', "
                        "'connection' = 'Connection failed', "
                        "'content' = 'Content failed', "
                        "'data' = 'Data access error', "
                        "'exec' = 'Execution failed', "
                        "'fsflags' = 'Filesystem flags failed', "
                        "'gid' = 'GID failed', "
                        "'icmp' = 'Ping failed', "
                        "'instance' = 'Monit instance changed', "
                        "'invalid' = 'Invalid type', "
                        "'link' = 'Link down', "
                        "'nonexist' = 'Does not exist', "
                        "'packetin' = 'Download packets exceeded', "
                        "'packetout' = 'Upload packets exceeded', "
                        "'permission' = 'Permission failed', "
                        "'pid' = 'PID failed', "
                        "'ppid' = 'PPID failed', "
                        "'resource' = 'Resource limit matched', "
                        "'saturation' = 'Saturation exceeded', "
                        "'size' = 'Size failed', "
                        "'speed' = 'Speed failed', "
                        "'status' = 'Status failed', "
                        "'timestamp' = 'Timestamp failed', "
                        "'uid' = 'UID failed', "
                        "'uptime' = 'Uptime failed'"
        ),
        format=dict(
            type='str', required=False,
            description='The email format for alerts. Subject: $SERVICE on $HOST failed'
        ),
        reminder=dict(
            type='int', required=False, default=10,
            description='Send a reminder after some cycles',
        ),
        description=dict(type='str', required=False, aliases=['desc']),
        match_fields=dict(
            type='list', required=False, elements='str',
            description='Fields that are used to match configured alerts with the running config - '
                        "if any of those fields are changed, the module will think it's a new entry",
            choices=['recipient', 'not_on', 'events', 'reminder', 'description'],
            default=['recipient'],
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

    module_wrapper(Alert(module=module, result=result))

    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
