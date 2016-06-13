#!/usr/bin/python

import json
import logging
from datetime import datetime, timedelta
from LogicMonitor import LogicMonitor


class Host(LogicMonitor):

    def __init__(self, params):
        """Initializor for the LogicMonitor host object"""
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Instantiating Host object")
        self.change = False
        self.params = params
        self.collector = None

        LogicMonitor.__init__(self, **self.params)

        if self.params["hostname"]:
            logging.debug("Hostname is " + self.params["hostname"])
            self.hostname = self.params['hostname']
        else:
            logging.debug("No hostname specified. Using " + self.fqdn)
            self.hostname = self.fqdn

        if self.params["displayname"]:
            logging.debug("Display name is " + self.params["displayname"])
            self.displayname = self.params['displayname']
        else:
            logging.debug("No display name specified. Using " + self.fqdn)
            self.displayname = self.fqdn

        # Attempt to host information via display name of host name
        logging.debug("Attempting to find host by displayname " +
                      self.displayname)
        info = self.get_host_by_displayname(self.displayname)

        if info is not None:
            logging.debug("Host found by displayname")
            # Used the host information to grab the collector description
            # if not provided
            if (not hasattr(self.params, "collector") and
               "agentDescription" in info):
                logging.debug("Setting collector from host response. " +
                              "Collector " + info["agentDescription"])
                self.params["collector"] = info["agentDescription"]
        else:
            logging.debug("Host not found by displayname")

        # At this point, a valid collector description is required for success
        # Check that the description exists or fail
        if self.params["collector"]:
            logging.debug("Collector specified is " +
                          self.params["collector"])
            self.collector = (self.get_collector_by_description(
                              self.params["collector"]))
        else:
            self.fail(msg="No collector specified.")

        # If the host wasn't found via displayname, attempt by hostname
        if info is None:
            logging.debug("Attempting to find host by hostname " +
                          self.hostname)
            info = self.get_host_by_hostname(self.hostname, self.collector)

        self.info = info
        self.properties = self.params["properties"]
        self.description = self.params["description"]
        self.starttime = self.params["starttime"]
        self.duration = self.params["duration"]
        self.alertenable = self.params["alertenable"]
        if self.params["groups"] is not None:
            self.groups = self._strip_groups(self.params["groups"])
        else:
            self.groups = None

    def create(self):
        """Idemopotent function to create if missing,
        update if changed, or skip"""
        logging.debug("Running Host.create...")

        self.update()

    def get_properties(self):
        """Returns a hash of the properties
        associated with this LogicMonitor host"""
        logging.debug("Running Host.get_properties...")

        if self.info:
            logging.debug("Making RPC call to 'getHostProperties'")
            properties_json = (json.loads(self.rpc("getHostProperties",
                                          {'hostId': self.info["id"],
                                           "filterSystemProperties": True})))

            if properties_json["status"] == 200:
                logging.debug("RPC call succeeded")
                return properties_json["data"]
            else:
                logging.debug("Error: there was an issue retrieving the " +
                              "host properties")
                logging.debug(properties_json["errmsg"])

                self.fail(msg=properties_json["status"])
        else:
            logging.debug("Unable to find LogicMonitor host which " +
                          "matches " + self.displayname +
                          " (" + self.hostname + ")")
            return None

    def set_properties(self, propertyhash):
        """update the host to have the properties
        contained in the property hash"""
        logging.debug("Running Host.set_properties...")
        logging.debug("System changed")
        self.change = True

        if self.check_mode:
            self.exit(changed=True)

        logging.debug("Assigning property hash to host object")
        self.properties = propertyhash

    def add(self):
        """Add this device to monitoring
        in your LogicMonitor account"""
        logging.debug("Running Host.add...")

        if self.collector and not self.info:
            logging.debug("Host not registered. Registering.")
            logging.debug("System changed")
            self.change = True

            if self.check_mode:
                self.exit(changed=True)

            h = self._build_host_hash(
                self.hostname,
                self.displayname,
                self.collector,
                self.description,
                self.groups,
                self.properties,
                self.alertenable)

            logging.debug("Making RPC call to 'addHost'")
            resp = json.loads(self.rpc("addHost", h))

            if resp["status"] == 200:
                logging.debug("RPC call succeeded")
                return resp["data"]
            else:
                logging.debug("RPC call failed")
                logging.debug(resp)
                return resp["errmsg"]
        elif self.collector is None:
            self.fail(msg="Specified collector doesn't exist")
        else:
            logging.debug("Host already registered")

    def update(self):
        """This method takes changes made to this host
        and applies them to the corresponding host
        in your LogicMonitor account."""
        logging.debug("Running Host.update...")

        if self.info:
            logging.debug("Host already registed")
            if self.is_changed():
                logging.debug("System changed")
                self.change = True

                if self.check_mode:
                    self.exit(changed=True)

                h = (self._build_host_hash(
                     self.hostname,
                     self.displayname,
                     self.collector,
                     self.description,
                     self.groups,
                     self.properties,
                     self.alertenable))
                h["id"] = self.info["id"]
                h["opType"] = "replace"

                logging.debug("Making RPC call to 'updateHost'")
                resp = json.loads(self.rpc("updateHost", h))

                if resp["status"] == 200:
                    logging.debug("RPC call succeeded")
                else:
                    logging.debug("RPC call failed")
                    self.fail(msg="Error: unable to update the host.")
            else:
                logging.debug("Host properties match supplied properties. " +
                              "No changes to make.")
                return self.info
        else:
            logging.debug("Host not registed. Registering")
            logging.debug("System changed")
            self.change = True

            if self.check_mode:
                self.exit(changed=True)

            return self.add()

    def remove(self):
        """Remove this host from your LogicMonitor account"""
        logging.debug("Running Host.remove...")

        if self.info:
            logging.debug("Host registered")
            logging.debug("System changed")
            self.change = True

            if self.check_mode:
                self.exit(changed=True)

            logging.debug("Making RPC call to 'deleteHost'")
            resp = json.loads(self.rpc("deleteHost",
                                       {"hostId": self.info["id"],
                                        "deleteFromSystem": True,
                                        "hostGroupId": 1}))

            if resp["status"] == 200:
                logging.debug(resp)
                logging.debug("RPC call succeeded")
                return resp
            else:
                logging.debug("RPC call failed")
                logging.debug(resp)
                self.fail(msg=resp["errmsg"])

        else:
            logging.debug("Host not registered")

    def is_changed(self):
        """Return true if the host doesn't
        match the LogicMonitor account"""
        logging.debug("Running Host.is_changed")

        ignore = ['system.categories', 'snmp.version']

        hostresp = self.get_host_by_displayname(self.displayname)

        if hostresp is None:
            hostresp = self.get_host_by_hostname(self.hostname, self.collector)

        if hostresp:
            logging.debug("Comparing simple host properties")
            if hostresp["alertEnable"] != self.alertenable:
                return True

            if hostresp["description"] != self.description:
                return True

            if hostresp["displayedAs"] != self.displayname:
                return True

            if (self.collector and
               hasattr(self.collector, "id") and
               hostresp["agentId"] != self.collector["id"]):
                return True

            logging.debug("Comparing groups.")
            if self._compare_groups(hostresp) is True:
                return True

            propresp = self.get_properties()

            if propresp:
                logging.debug("Comparing properties.")
                if self._compare_props(propresp, ignore) is True:
                    return True
            else:
                self.fail(
                    msg="Error: Unknown error retrieving host properties")

            return False
        else:
            self.fail(msg="Error: Unknown error retrieving host information")

    def sdt(self):
        """Create a scheduled down time
        (maintenance window) for this host"""
        logging.debug("Running Host.sdt...")

        if self.info:
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
                accountresp = (json.loads(self.rpc("getTimeZoneSetting", {})))

                if accountresp["status"] == 200:
                    logging.debug("RPC call succeeded")

                    offset = accountresp["data"]["offset"]
                    offsetstart = start + timedelta(0, offset)
                else:
                    self.fail(
                        msg="Error: Unable to retrieve timezone offset")

            offsetend = offsetstart + timedelta(0, int(duration)*60)

            h = {"hostId": self.info["id"],
                 "type": 1,
                 "year": offsetstart.year,
                 "month": offsetstart.month - 1,
                 "day": offsetstart.day,
                 "hour": offsetstart.hour,
                 "minute": offsetstart.minute,
                 "endYear": offsetend.year,
                 "endMonth": offsetend.month - 1,
                 "endDay": offsetend.day,
                 "endHour": offsetend.hour,
                 "endMinute": offsetend.minute}

            logging.debug("Making RPC call to 'setHostSDT'")
            resp = (json.loads(self.rpc("setHostSDT", h)))

            if resp["status"] == 200:
                logging.debug("RPC call succeeded")
                return resp["data"]
            else:
                logging.debug("RPC call failed")
                self.fail(msg=resp["errmsg"])
        else:
            self.fail(msg="Error: Host doesn't exit.")

    def site_facts(self):
        """Output current properties information for the Host"""
        logging.debug("Running Host.site_facts...")

        if self.info:
            logging.debug("Host exists")
            props = self.get_properties()

            self.output_info(props)
        else:
            self.fail(msg="Error: Host doesn't exit.")

    def _build_host_hash(self,
                         hostname,
                         displayname,
                         collector,
                         description,
                         groups,
                         properties,
                         alertenable):
        """Return a property formated hash for the
        creation of a host using the rpc function"""
        logging.debug("Running Host._build_host_hash...")

        h = {}
        h["hostName"] = hostname
        h["displayedAs"] = displayname
        h["alertEnable"] = alertenable

        if collector:
            logging.debug("Collector property exists")
            h["agentId"] = collector["id"]
        else:
            self.fail(
                msg="Error: No collector found. Unable to build host hash.")

        if description:
            h["description"] = description

        if groups is not None and groups is not []:
            logging.debug("Group property exists")
            groupids = ""

            for group in groups:
                groupids = groupids + str(self.create_group(group)) + ","

            h["hostGroupIds"] = groupids.rstrip(',')

        if properties is not None and properties is not {}:
            logging.debug("Properties hash exists")
            propnum = 0
            for key, value in properties.iteritems():
                h["propName" + str(propnum)] = key
                h["propValue" + str(propnum)] = value
                propnum = propnum + 1

        return h

    def _verify_property(self, propname):
        """Check with LogicMonitor server to
        verify property is unchanged"""
        logging.debug("Running Host._verify_property...")

        if self.info:
            logging.debug("Host is registered")
            if propname not in self.properties:
                logging.debug("Property " + propname + " does not exist")
                return False
            else:
                logging.debug("Property " + propname + " exists")
                h = {"hostId": self.info["id"],
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
                msg="Error: Host doesn't exist. Unable to verify properties")

    def _compare_groups(self, hostresp):
        """Function to compare the host's current
        groups against provided groups"""
        logging.debug("Running Host._compare_groups")

        g = []
        fullpathinids = hostresp["fullPathInIds"]
        logging.debug("Building list of groups")
        for path in fullpathinids:
            if path != []:
                h = {'hostGroupId': path[-1]}

                hgresp = json.loads(self.rpc("getHostGroup", h))

                if (hgresp["status"] == 200 and
                   hgresp["data"]["appliesTo"] == ""):

                    g.append(path[-1])

        if self.groups is not None:
            logging.debug("Comparing group lists")
            for group in self.groups:
                groupjson = self.get_group(group)

                if groupjson is None:
                    logging.debug("Group mismatch. No result.")
                    return True
                elif groupjson['id'] not in g:
                    logging.debug("Group mismatch. ID doesn't exist.")
                    return True
                else:
                    g.remove(groupjson['id'])

            if g != []:
                logging.debug("Group mismatch. New ID exists.")
                return True
            logging.debug("Groups match")

    def _compare_props(self, propresp, ignore):
        """Function to compare the host's current
        properties against provided properties"""
        logging.debug("Running Host._compare_props...")
        p = {}

        logging.debug("Creating list of properties")
        for prop in propresp:
            if prop["name"] not in ignore:
                if ("*******" in prop["value"] and
                   self._verify_property(prop["name"])):
                    p[prop["name"]] = self.properties[prop["name"]]
                else:
                    p[prop["name"]] = prop["value"]

        logging.debug("Comparing properties")
        # Iterate provided properties and compare to received properties
        for prop in self.properties:
            if (prop not in p or
               p[prop] != self.properties[prop]):
                logging.debug("Properties mismatch")
                return True
        logging.debug("Properties match")

    def _strip_groups(self, groups):
        """Function to strip whitespace from group list.
        This function provides the user some flexibility when
        formatting group arguments """
        logging.debug("Running Host._strip_groups...")
        return map(lambda x: x.strip(), groups)
