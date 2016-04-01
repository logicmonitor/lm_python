#!/usr/bin/python

import logging
import subprocess
from subprocess import Popen


class Service(object):
    @staticmethod
    def getStatus(name):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Retrieving status of service {0}".format(name))

        ret = -1

        startType = Service._getType(name)

        # Determine how to get the status of the service
        if startType == "init.d":
            p = (Popen(["/etc/init.d/{0}".format(name), "status"],
                       stdout=subprocess.PIPE))
            ret, err = p.communicate()
        elif startType == "service":
            p = (Popen(["service", name, "status"],
                       stdout=subprocess.PIPE))
            ret, err = p.communicate()
        else:
            ret = "Unknown error getting status for service {0}".format(name)

        return ret

    @staticmethod
    def doAction(name, action):
        logging.debug("Performing {0} on service {1}".format(action, name))

        startType = Service._getType(name)

        ret = -1

        # Determine how to perform the action on the service
        if startType == "init.d":
            p = (Popen(["/etc/init.d/{0}".format(name), action],
                       stdout=subprocess.PIPE))
            msg = p.communicate()
            ret = p.returncode
        elif startType == "service":
            p = (Popen(["service", name, action],
                       stdout=subprocess.PIPE))
            msg = p.communicate()
            ret = p.returncode

        else:
            msg = ("Unknown error performing '{0}' on service {1}"
                   .format(action, name))
            ret = msg

        return (ret, msg)

    @staticmethod
    def _getType(name):
        logging.debug("Getting service {0} control type".format(name))

        try:
            p = (Popen(["/etc/init.d/{0}".format(name), "status"],
                       stdout=subprocess.PIPE))
            ret = p.communicate()
            result = p.returncode

            if result == 0 or result == 1:
                logging.debug("Service control is via init.d")
                return "init.d"
        except:
            result = -1

        try:
            p = (Popen(["service", name, "status"],
                       stdout=subprocess.PIPE))
            ret = p.communicate()
            result = p.returncode

            if result == 0 or result == 1:
                logging.debug("Service control is via service")
                return "service"
        except:
            ret = result

        return ret
