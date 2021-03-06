#!/usr/bin/python

import argparse
from logicmonitor_core.Datasource import Datasource


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
    parser.add_argument("-i", "--id",
                        help="Object ID")

    parser.add_argument("-D", "--duration",
                        help="SDT duration")
    parser.add_argument("-s", "--starttime",
                        help="SDT start time")
    args = parser.parse_args()

    params = {}
    params["duration"] = 30
    params["starttime"] = None

    # Required params
    params["company"] = args.company
    params["user"] = args.user
    params["password"] = args.password
    params["id"] = args.id

    # Optional params
    if args.duration is not None:
        params["duration"] = args.duration
    if args.starttime is not None:
        params["starttime"] = args.starttime

    d = Datasource(params)

    exit_code = d.sdt()

    return exit_code

main()
