#!/usr/bin/python

import argparse
import json
from logicmonitor_core.HostList import HostList


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

    parser.add_argument("-g", "--group",
                        help="Limit the results to hosts in the group path " +
                        "specified. Example: /Servers")
    args = parser.parse_args()

    params = {}
    params["group"] = None

    # Required params
    params["company"] = args.company
    params['accessid'] = args.accessid
    params['accesskey'] = args.accesskey

    # Optional params
    if args.group is not None:
        params["group"] = args.group

    host_list = HostList(params)
    hosts = host_list.get_hosts()

    print json.dumps(hosts)

    return 0

main()
