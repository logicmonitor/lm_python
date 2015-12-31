#!/usr/bin/python

import argparse
from Class.Collector import Collector


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

    parser.add_argument("-d", "--duration",
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

    # Optional params
    if args.duration is not None:
        params["duration"] = args.duration

    if args.starttime is not None:
        params["starttime"] = args.starttime

    col = Collector(params)

    exit_code = col.sdt()

    return exit_code

main()
