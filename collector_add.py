#!/usr/bin/python

import argparse
import logging
from Class.Collector import Collector


def main():
    logging.basicConfig(level=logging.DEBUG)

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
    params["user"] = args.user
    params["password"] = args.password

    col = Collector(params)

    exit_code = col.create()

    return exit_code

main()
