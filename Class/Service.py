#!/usr/bin/python

import logging
import subprocess
from subprocess import call
from subprocess import Popen

logging.basicConfig(level=logging.DEBUG)


def getStatus(name):
    logging.debug("Retrieving status of service {0}".format(name))

    output = -1

    startType = _getType(name)

    # Determine how to get the status of the service
    if startType == "init.d":
        a = (Popen(["/etc/init.d/{0}".format(name), "status"],
                   stdout=subprocess.PIPE))
        (output, error) = a.communicate()
    elif startType == "service":
        a = (Popen(["service", name, "status"],
                   stdout=subprocess.PIPE))
        (output, error) = a.communicate()
    else:
        output = "Unknown error getting status for service {0}".format(name)

    return output


def doAction(name, action):
    logging.debug("Performing {0} on service {1}".format(action, name))

    startType = _getType(name)

    output = -1

    # Determine how to perform the action on the service
    if startType == "init.d":
        output = call(["/etc/init.d/{0}".format(name), action])
    elif startType == "service":
        output = call(["service", name, action])
    else:
        output = ("Unknown error performing '{0}' on service {1}"
                  .format(action, name))

    return output


def _getType(name):
    logging.debug("Getting service {0} control type".format(name))
    try:
        output = call(["/etc/init.d/{0}".format(name), "status"])

        if output == 0 or output == 1:
            logging.debug("Service control is via init.d")
            return "init.d"
    except:
        output = -1

    try:
        output = call(["service", name, "status"])

        if output == 0 or output == 1:
            logging.debug("Service control is via service")
            return "service"
    except:
        output = -1

    return -1
