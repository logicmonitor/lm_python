#!/usr/bin/python

import argparse
from logicmonitor_core.Host import Host


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
                        help="Collector FQDN")
    parser.add_argument("-H", "--hostname",
                        help="Machine hostname")
    parser.add_argument("-d", "--displayname",
                        help="Machine display name")
    parser.add_argument("-D", "--duration",
                        help="SDT duration")
    parser.add_argument("-s", "--starttime",
                        help="SDT start time")
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
    if args.hostname is not None:
        params["hostname"] = args.hostname
    if args.displayname is not None:
        params["displayname"] = args.displayname
    if args.duration is not None:
        params["duration"] = args.duration
    if args.starttime is not None:
        params["starttime"] = args.starttime

    h = Host(params)

    exit_code = h.sdt()

    return exit_code

main()
