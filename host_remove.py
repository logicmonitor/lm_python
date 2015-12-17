#!/usr/bin/python

import argparse
from Class.Host import Host


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
    parser.add_argument("-C", "--collector",
                        help="Collector FQDN",
                        required=True)

    parser.add_argument("-H", "--hostname",
                        help="Machine hostname")
    parser.add_argument("-d", "--displayname",
                        help="Machine display name")
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

    # Required params
    params["company"] = args.company
    params["user"] = args.user
    params["password"] = args.password
    params["collector"] = args.collector

    # Optional params
    if args.displayname is not None:
        params["hostname"] = args.displayname
    if args.displayname is not None:
        params["displayname"] = args.displayname

    h = Host(params)

    exit_code = h.remove()

    return exit_code

main()
