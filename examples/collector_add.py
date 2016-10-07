#!/usr/bin/python

import argparse
import logging
from Collector import Collector


def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--company',
                        help='LogicMonitor account',
                        required=True)
    parser.add_argument('-t', '--accessid',
                        help='API Token Access Id',
                        required=True)
    parser.add_argument('-k', '--accesskey',
                        help='API Token Access Key',
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
    params['collector_id'] = args.collector_id

    # Require params
    params['company'] = args.company
    params['accessid'] = args.accessid
    params['accesskey'] = args.accesskey

    col = Collector(params)

    exit_code = col.create()

    return exit_code

main()
