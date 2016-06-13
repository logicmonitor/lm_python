#!/usr/bin/python

import json
import logging
from datetime import datetime, timedelta
from LogicMonitor import LogicMonitor


class Hostgroup(LogicMonitor):

    def __init__(self, params):
        """Initializor for the LogicMonitor host object"""
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Instantiating Hostgroup object")
        self.change = False
        self.params = params

        LogicMonitor.__init__(self, **self.params)

        self.fullpath = self.params["fullpath"]
        self.info = self.get_group(self.fullpath)
        self.properties = self.params["properties"]
        self.description = self.params["description"]
        self.starttime = self.params["starttime"]
        self.duration = self.params["duration"]
        self.alertenable = self.params["alertenable"]

    def create(self):
        """Wrapper for self.update()"""
        logging.debug("Running Hostgroup.create...")
        self.update()

    def get_properties(self, final=False):
        """Returns a hash of the properties
        associated with this LogicMonitor host"""
        logging.debug("Running Hostgroup.get_properties...")

        if self.info:
            logging.debug("Group found")

            logging.debug("Making RPC call to 'getHostGroupProperties'")
            properties_json = json.loads(self.rpc(
                "getHostGroupProperties",
                {'hostGroupId': self.info["id"],
                 "finalResult": final}))

            if properties_json["status"] == 200:
                logging.debug("RPC call succeeded")
                return properties_json["data"]
            else:
                logging.debug("RPC call failed")
                self.fail(msg=properties_json["status"])
        else:
            logging.debug("Group not found")
            return None

    def set_properties(self, propertyhash):
        """Update the host to have the properties
        contained in the property hash"""
        logging.debug("Running Hostgroup.set_properties")

        logging.debug("System changed")
        self.change = True

        if self.check_mode:
            self.exit(changed=True)

        logging.debug("Assigning property has to host object")
        self.properties = propertyhash

    def add(self):
        """Idempotent function to ensure that the host
        group exists in your LogicMonitor account"""
        logging.debug("Running Hostgroup.add")

        if self.info is None:
            logging.debug("Group doesn't exist. Creating.")
            logging.debug("System changed")
            self.change = True

            if self.check_mode:
                self.exit(changed=True)

            self.create_group(self.fullpath)
            self.info = self.get_group(self.fullpath)

            logging.debug("Group created")
            return self.info
        else:
            logging.debug("Group already exists")

    def update(self):
        """Idempotent function to ensure the device group settings
        (alertenable, properties, etc) in the
        LogicMonitor account match the current object."""
        logging.debug("Running Hostgroup.update")

        if self.info:
            if self.is_changed():
                logging.debug("System changed")
                self.change = True

                if self.check_mode:
                    self.exit(changed=True)

                h = self._build_host_group_hash(
                    self.fullpath,
                    self.description,
                    self.properties,
                    self.alertenable)
                h["opType"] = "replace"

                if self.fullpath != "/":
                    h["id"] = self.info["id"]

                logging.debug("Making RPC call to 'updateHostGroup'")
                resp = json.loads(self.rpc("updateHostGroup", h))

                if resp["status"] == 200:
                    logging.debug("RPC call succeeded")
                    return resp["data"]
                else:
                    logging.debug("RPC call failed")
                    self.fail(
                        msg="Error: Unable to update the " +
                            "host.\n" + resp["errmsg"])
            else:
                logging.debug("Group properties match supplied properties. " +
                              "No changes to make")
                return self.info
        else:
            logging.debug("Group doesn't exist. Creating.")

            logging.debug("System changed")
            self.change = True

            if self.check_mode:
                self.exit(changed=True)

            return self.add()

    def remove(self):
        """Idempotent function to ensure the device group
        does not exist in your LogicMonitor account"""
        logging.debug("Running Hostgroup.remove...")

        if self.info:
            logging.debug("Group exists")
            logging.debug("System changed")
            self.change = True

            if self.check_mode:
                self.exit(changed=True)

            logging.debug("Making RPC call to 'deleteHostGroup'")
            resp = json.loads(self.rpc("deleteHostGroup",
                                       {"hgId": self.info["id"]}))

            if resp["status"] == 200:
                logging.debug(resp)
                logging.debug("RPC call succeeded")
                return resp
            elif resp["errmsg"] == "No such group":
                logging.debug("Group doesn't exist")
            else:
                logging.debug("RPC call failed")
                logging.debug(resp)
                self.fail(msg=resp["errmsg"])
        else:
            logging.debug("Group doesn't exist")

    def is_changed(self):
        """Return true if the host doesn't match
        the LogicMonitor account"""
        logging.debug("Running Hostgroup.is_changed...")

        ignore = []
        group = self.get_group(self.fullpath)
        properties = self.get_properties()

        if properties is not None and group is not None:
            logging.debug("Comparing simple group properties")
            if (group["alertEnable"] != self.alertenable or
               group["description"] != self.description):

                return True

            p = {}

            logging.debug("Creating list of properties")
            for prop in properties:
                if prop["name"] not in ignore:
                    if ("*******" in prop["value"] and
                       self._verify_property(prop["name"])):

                        p[prop["name"]] = (
                            self.properties[prop["name"]])
                    else:
                        p[prop["name"]] = prop["value"]

            logging.debug("Comparing properties")
            if set(p) != set(self.properties):
                return True
        else:
            logging.debug("No property information received")
            return False

    def sdt(self, duration=30, starttime=None):
        """Create a scheduled down time
        (maintenance window) for this host"""
        logging.debug("Running Hostgroup.sdt")

        logging.debug("System changed")
        self.change = True

        if self.check_mode:
            self.exit(changed=True)

        duration = self.duration
        starttime = self.starttime
        offset = starttime

        if starttime:
            logging.debug("Start time specified")
            start = datetime.strptime(starttime, '%Y-%m-%d %H:%M')
            offsetstart = start
        else:
            logging.debug("No start time specified. Using default.")
            start = datetime.utcnow()

            # Use user UTC offset
            logging.debug("Making RPC call to 'getTimeZoneSetting'")
            accountresp = json.loads(self.rpc("getTimeZoneSetting", {}))

            if accountresp["status"] == 200:
                logging.debug("RPC call succeeded")

                offset = accountresp["data"]["offset"]
                offsetstart = start + timedelta(0, offset)
            else:
                self.fail(
                    msg="Error: Unable to retrieve timezone offset")

        offsetend = offsetstart + timedelta(0, int(duration)*60)

        h = {"hostGroupId": self.info["id"],
             "type": 1,
             "year": offsetstart.year,
             "month": offsetstart.month-1,
             "day": offsetstart.day,
             "hour": offsetstart.hour,
             "minute": offsetstart.minute,
             "endYear": offsetend.year,
             "endMonth": offsetend.month-1,
             "endDay": offsetend.day,
             "endHour": offsetend.hour,
             "endMinute": offsetend.minute}

        logging.debug("Making RPC call to setHostGroupSDT")
        resp = json.loads(self.rpc("setHostGroupSDT", h))

        if resp["status"] == 200:
            logging.debug("RPC call succeeded")
            return resp["data"]
        else:
            logging.debug("RPC call failed")
            self.fail(msg=resp["errmsg"])

    def site_facts(self):
        """Output current properties information for the Hostgroup"""
        logging.debug("Running Hostgroup.site_facts...")

        if self.info:
            logging.debug("Group exists")
            props = self.get_properties(True)

            self.output_info(props)
        else:
            self.fail(msg="Error: Group doesn't exit.")

    def _build_host_group_hash(self,
                               fullpath,
                               description,
                               properties,
                               alertenable):
        """Return a property formated hash for the
        creation of a hostgroup using the rpc function"""
        logging.debug("Running Hostgroup._build_host_hash")

        h = {}
        h["alertEnable"] = alertenable

        if fullpath == "/":
            logging.debug("Group is root")
            h["id"] = 1
        else:
            logging.debug("Determining group path")
            parentpath, name = fullpath.rsplit('/', 1)
            parent = self.get_group(parentpath)

            h["name"] = name

            if parent:
                logging.debug("Parent group " + parent["id"] + " found.")
                h["parentID"] = parent["id"]
            else:
                logging.debug("No parent group found. Using root.")
                h["parentID"] = 1

        if description:
            logging.debug("Description property exists")
            h["description"] = description

        if properties != {}:
            logging.debug("Properties hash exists")
            propnum = 0
            for key, value in properties.iteritems():
                h["propName" + str(propnum)] = key
                h["propValue" + str(propnum)] = value
                propnum = propnum + 1

        return h

    def _verify_property(self, propname):
        """Check with LogicMonitor server
        to verify property is unchanged"""
        logging.debug("Running Hostgroup._verify_property")

        if self.info:
            logging.debug("Group exists")
            if propname not in self.properties:
                logging.debug("Property " + propname + " does not exist")
                return False
            else:
                logging.debug("Property " + propname + " exists")
                h = {"hostGroupId": self.info["id"],
                     "propName0": propname,
                     "propValue0": self.properties[propname]}

                logging.debug("Making RCP call to 'verifyProperties'")
                resp = json.loads(self.rpc('verifyProperties', h))

                if resp["status"] == 200:
                    logging.debug("RPC call succeeded")
                    return resp["data"]["match"]
                else:
                    self.fail(
                        msg="Error: unable to get verification " +
                            "from server.\n%s" % resp["errmsg"])
        else:
            self.fail(
                msg="Error: Group doesn't exist. Unable to verify properties")
