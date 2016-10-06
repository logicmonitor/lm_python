#!/usr/bin/python

import argparse
from logicmonitor_core.Collector import Collector


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
    args = parser.parse_args()

    params = {}
    params["alertenable"] = True
    params["collector"] = None
    params["description"] = ""
    params["displayname"] = None
    params["duration"] = 30
    params["fullpath"] = None
    params["groups"] = []
    params["hostname"] = None
    params["properties"] = {}
    params["starttime"] = None

    # Require params
    params["company"] = args.company
    params['accessid'] = args.accessid
    params['accesskey'] = args.accesskey

    col = Collector(params)

    exit_code = col.remove()

    return exit_code

main()
