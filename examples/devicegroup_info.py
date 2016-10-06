#!/usr/bin/python

import argparse
from logicmonitor_core.Hostgroup import Hostgroup


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--company",
                        help="LogicMonitor account",
                        required=True)
    parser.add_argument('-i', '--accessid',
                        help="API Token Access Id",
                        required=True)
    parser.add_argument('-k', '--accesskey',
                        help="API Token Access Key",
                        required=True)
    parser.add_argument("-f", "--fullpath",
                        help="Full path of the device group",
                        required=True)
    args = parser.parse_args()

    params = {}
    params["alertenable"] = True
    params["collector"] = None
    params["description"] = ""
    params["displayname"] = None
    params["duration"] = 30
    params["fullpath"] = None
    params["groups"] = []
    params["properties"] = {}
    params["starttime"] = None

    # Required params
    params["company"] = args.company
    params['accessid'] = args.accessid
    params['accesskey'] = args.accesskey
    params["fullpath"] = args.fullpath

    hg = Hostgroup(params)

    exit_code = hg.site_facts()

    return exit_code

main()
