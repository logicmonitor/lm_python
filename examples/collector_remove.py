#!/usr/bin/python

import argparse
from logicmonitor_core.Collector import Collector


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--company',
                        help='LogicMonitor account',
                        required=True)
    parser.add_argument('-u', '--user',
                        help='LogicMonitor user name',
                        required=True)
    parser.add_argument('-p', '--password',
                        help='LogicMonitor password',
                        required=True)
    parser.add_argument('-i', '--collector_id',
                        help='ID of an existing collector to add')
    args = parser.parse_args()

    params = {}
    params['alertenable'] = True
    params['collector'] = None
    params['description'] = ''
    params['displayname'] = None
    params['duration'] = 30
    params['fullpath'] = None
    params['groups'] = []
    params['hostname'] = None
    params['properties'] = {}
    params['starttime'] = None

    # Require params
    params['company'] = args.company
    params['accessid'] = args.accessid
    params['accesskey'] = args.accesskey

    if args.collector_id is not None:
        params['collector_id'] = args.collector_id

    if args.description is not None:
        params['description'] = args.description

    col = Collector(params)

    exit_code = col.remove()

    return exit_code

main()
