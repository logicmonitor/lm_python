#!/usr/bin/python

import argparse
import json
from logicmonitor_core.HostList import HostList


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--company",
                        help="LogicMonitor account",
                        required=True)
    parser.add_argument("-u", "--user",
                        help="LogicMonitor user name",
                        required=True)
    parser.add_argument("-p", "--password",
                        help="LogicMonitor password",
                        required=True)

    parser.add_argument("-g", "--group",
                        help="Machine hostname")
    args = parser.parse_args()

    params = {}
    params["group"] = None

    # Required params
    params["company"] = args.company
    params["user"] = args.user
    params["password"] = args.password

    # Optional params
    if args.group is not None:
        params["group"] = args.group

    host_list = HostList(params)
    hosts = host_list.get_hosts()

    print json.dumps(hosts)

    return 0

main()
