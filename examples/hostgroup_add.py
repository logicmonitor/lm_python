#!/usr/bin/python

import argparse
import json
from logicmonitor_core.Hostgroup import Hostgroup


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
    parser.add_argument("-f", "--fullpath",
                        help="Full path of the device group",
                        required=True)

    parser.add_argument("--description",
                        help="Text description of the host")
    parser.add_argument("-P", "--properties",
                        help="A dictionary of properties to set for the host",
                        type=json.loads)
    parser.add_argument("-a", "--alertenable",
                        help="Turn alerting on or off")
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
    params["fullpath"] = args.fullpath

    # Optional params
    if args.description is not None:
        params["description"] = args.description
    if args.properties is not None:
        params["properties"] = args.properties
    if args.alertenable is not None:
        params["alertenable"] = args.alertenable

    hg = Hostgroup(params)

    exit_code = hg.add()

    return exit_code

main()
