#!/usr/bin/python

import logging
import os
import subprocess
from subprocess import Popen


class Service(object):
    @staticmethod
    def getStatus(name):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Retrieving status of service " + name)

        ret = -1

        startType = Service._getType(name)

        # Determine how to get the status of the service
        if startType == "init.d":
            p = (Popen(["/etc/init.d/" + name, "status"],
                       stdout=subprocess.PIPE))
            ret, err = p.communicate()
        elif startType == "service":
            p = (Popen(["service", name, "status"],
                       stdout=subprocess.PIPE))
            ret, err = p.communicate()
        else:
            ret = "Unknown error getting status for service " + name

        return ret

    @staticmethod
    def doAction(name, action):
        logging.debug("Performing " + action + " on service " + name)

        startType = Service._getType(name)

        ret = -1

        # Determine how to perform the action on the service
        if startType == "init.d":
            p = (Popen(["/etc/init.d/" + name, action],
                       stdout=subprocess.PIPE))
            msg = p.communicate()
            ret = p.returncode
        elif startType == "service":
            p = (Popen(["service", name, action],
                       stdout=subprocess.PIPE))
            msg = p.communicate()
            ret = p.returncode

        else:
            msg = ("Unknown error performing '" + action +
                   "' on service " + name + "")
            ret = msg

        return (ret, msg)

    @staticmethod
    def _getType(name):
        logging.debug("Getting service " + name + " control type")

        if os.path.isdir("/etc/init.d"):
            logging.debug("Service control is via init.d")
            return "init.d"
        else:
            result = -1

        try:
            p = (Popen(["service", "--status-all"],
                       stdout=subprocess.PIPE))
            p.communicate()
            result = p.returncode

            if result == 0 or result == 1:
                logging.debug("Service control is via service")
                return "service"
        except:
            result = -1
        return result
