#!/usr/bin/python

import json
import logging
from LogicMonitor import LogicMonitor


class HostList(LogicMonitor):

    def __init__(self, params):
        """Initializor for the LogicMonitor host list object"""
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Instantiating HostList")
        self.params = params
        self.groupId = None

        LogicMonitor.__init__(self, **self.params)

        if self.params["group"]:
            logging.debug("Group is " + self.params["group"])
            self.group = self.params['group']

            # Attempt to get group id
            logging.debug("Attempting to find group " + self.group)
            group = self.get_group(self.group)

            if "id" in group:
                self.groupId = group["id"]
            else:
                self.fail(msg="Group " + self.group + " not found.")

    def get_hosts(self):
        """Returns a hash of the hosts
        associated with this LogicMonitor account"""
        logging.debug("Running HostList.get_hosts...")

        logging.debug("Making RPC call to 'getHosts'")
        properties_json = (json.loads(self.rpc("getHosts",
                                               {"hostGroupId":
                                                self.groupId or 1})))

        if properties_json["status"] == 200:
            logging.debug("RPC call succeeded")
            return properties_json["data"]
        else:
            logging.debug("Error: there was an issue retrieving the " +
                          "host list")
            logging.debug(properties_json["errmsg"])

            self.fail(msg=properties_json["status"])

        return None
