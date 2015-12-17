#!/usr/bin/python

DOCUMENTATION = '''
---
module: logicmonitor
short_description: Manage your LogicMonitor account
 through Ansible Playbooks
description:
    - LogicMonitor is a hosted, full-stack, infrastructure
     monitoring platform.

    - This module manages hosts, host groups, and collectors
    within your LogicMonitor account.
version_added: "1.4"
author: Ethan Culler-Mayeno
notes: You must have an existing LogicMonitor account
 for this module to function.
requirements:
    - An existing LogicMonitor account
    - Currently supported operating systems:
        - Linux
options:
    target:
        description:
            - The LogicMonitor object you wish to manage.
        required: true
        default: null
        choices: ['collector', 'host', 'hostgroup']
    action:
        description:
            - The action you wish to perform on target
        required: true
        default: null
        choices: ['add', 'remove', 'sdt']
    company:
        description:
            - The LogicMonitor account company name. If you would
             log in to your account at
             "superheroes.logicmonitor.com"
             you would use "superheroes"
        required: true
        default: null
        choices: null
    user:
        description:
            - A LogicMonitor user name. The module will
             authenticate and perform actions on
             behalf of this user
        required: true
        default: null
        choices: null
    password:
        description:
            - The password for the chosen LogicMonitor User
            - If an md5 hash is used, the digest flag
             must be set to true
        required: true
        default: null
        choices: null
    collector:
        description:
            - The fully qualified domain name of a collector
            in your LogicMonitor account.

            - This is required for the creation of a
             LogicMonitor host (target=host action=add)
        required: false
        default: null
        choices: null
    hostname:
        description:
            - The hostname of a host in your LogicMonitor account,
            or the desired hostname of a device to
            add into monitoring.

            - Required for managing hosts (target=host)
        required: false
        default: 'hostname -f'
        choices: null
    displayname:
        description:
            - the display name of a host in your LogicMonitor
             account or the desired display name of a device to
             add into monitoring.
        required: false
        default: 'hostname -f'
        choices: null
    description:
        description:
            - The long text description of the object in your
             LogicMonitor account

            - Used when managing hosts and host groups
             (target=host or target=hostgroup)
        required: false
        default: ""
        choices: null
    properties:
        description:
            - A dictionary of properties to set on the
             LogicMonitor host or hostgroup.

            - Used when managing hosts and host groups
             (target=host or target=hostgroup)

            - This module will overwrite existing properties in
             your LogicMonitor account
        required: false
        default: {}
        choices: null
    groups:
        description:
            - The set of groups that the host should be a
             member of.

            - Used when managing LogicMonitor hosts (target=host)
        required: false
        default: []
        choices: null
    fullpath:
        description:
            - The fullpath of the hostgroup object you would
             like to manage

            - Recommend running on a single ansible host

            - Required for management of LogicMonitor
             host groups (target=hostgroup)
        required: false
        default: null
        choices: null
    alertenable:
        description:
            - A boolean flag to turn on and off alerting
             for an object
        required: false
        default: true
        choices: [true, false]
    starttime:
        description:
            - The starttime for putting an object into
             Scheduled Down Time (maintenance mode)

            - Required for putting an object into SDT (action=sdt)
        required: false
        default: null
        choices: null
    duration:
        description:
            - The duration (minutes) an object should remain in
             Scheduled Down Time (maintenance mode)

            - Required for putting an object into SDT (action=sdt)
        required: false
        default: 30
        choices: null
'''

EXAMPLES = '''
#example of adding a new LogicMonitor collector to these devices
---

- hosts: collectors
  user: root
  vars:
    company: 'yourcompany'
    user: 'mario'
    password: 'itsame.Mario!'
    digest: False
  tasks:
  - name: Deploy/verify LogicMonitor collectors
    logicmonitor: target=collector action=add
     company={{ company }} user={{ user }} password={{ password }}

#example of adding a host into monitoring
---

- hosts: collectors
  user: root
  vars:
    company: 'yourcompany'
    user: 'mario'
    password: 'itsame.Mario!'
    digest: False
  tasks:
  - name: Deploy LogicMonitor Host
    local_action:
      logicmonitor:
        target: host
        action: add
        collector: agent1.ethandev.com
        company: '{{ company }}'
        user: '{{ user }}'
        password: '{{ password }}'
        properties: {snmp.community: 'communitystr1'}
        groups: ['/test/asdf', '/ans/ible']

#example of creating a hostgroup
---

- hosts: somemachine.superheroes.com
  user: root
  vars:
    company: 'yourcompany'
    user: 'mario'
    password: 'itsame.Mario!'
    digest: False
  tasks:
  - name: Create a host group
    logicmonitor:
      target: hostgroup
      action: add
      fullpath: '/worst/name/ever'
      company: '{{ company }}'
      user: '{{ user }}'
      password: '{{ password }}'
      properties: {snmp.community: 'communitystr2',
       mysql.user: 'superman'}
'''
