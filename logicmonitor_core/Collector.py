#!/usr/bin/python

import json
import logging
import os
import platform
import subprocess
import sys
from datetime import datetime, timedelta
from subprocess import Popen
from LogicMonitor import LogicMonitor
from Service import Service


class Collector(LogicMonitor):

    def __init__(self, params):
        """Initializor for the LogicMonitor Collector object"""
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Instantiating Collector object")
        self.change = False
        self.params = params

        LogicMonitor.__init__(self, **params)

        if "description" in self.params:
            self.description = self.params['description']
        else:
            self.description = self.fqdn

        if "collector_id" in self.params:
            self.collector_id = self.params["collector_id"]
        else:
            self.collector_id = None

        self.info = self._get()
        self.installdir = "/usr/local/logicmonitor"
        self.platform = platform.system()
        self.is_64bits = sys.maxsize > 2**32

        if "duration" in self.params:
            self.duration = self.params['duration']
        if "starttime" in self.params:
            self.starttime = self.params['starttime']

        if self.info is None:
            self.id = None
        else:
            self.id = self.info["id"]

    def create(self):
        """Idempotent function to make sure that there is
        a running collector installed and registered"""
        logging.debug("Running Collector.create...")

        self._create()
        self.get_installer_binary()
        self.install()
        self.start()
        logging.debug("Collector created")

    def remove(self):
        """Idempotent function to make sure that there is
        not a running collector installed and registered"""
        logging.debug("Running Collector.destroy...")

        self.stop()
        self._unregister()
        self.uninstall()
        logging.debug("Collector removed")

    def get_installer_binary(self):
        """Download the LogicMonitor collector installer binary"""
        logging.debug("Running Collector.get_installer_binary...")

        arch = 32

        if self.is_64bits:
            logging.debug("64 bit system")
            arch = 64
        else:
            logging.debug("32 bit system")

        if self.platform == "Linux" and self.id is not None:
            logging.debug("Platform is Linux")
            logging.debug("Agent ID is " + str(self.id))

            if not os.path.exists(self.installdir):
                os.makedirs(self.installdir)
                logging.debug("Created installdir at " +
                              self.installdir)

            installfilepath = (self.installdir +
                               "/logicmonitorsetup" +
                               str(self.id) + "_" + str(arch) +
                               ".bin")

            logging.debug("Looking for existing installer at " +
                          installfilepath)
            if not os.path.isfile(installfilepath):
                logging.debug("No previous installer found")
                logging.debug("System changed")
                self.change = True

                if self.check_mode:
                    self.exit(changed=True)

                logging.debug("Downloading installer file")
                try:
                    f = open(installfilepath, "w")
                    installer = (self.do("logicmonitorsetup",
                                         {"id": self.id,
                                          "arch": arch}))
                    f.write(installer)
                    f.closed
                except:
                    self.fail(msg="Unable to open installer file for writing")
                    f.closed
            else:
                logging.debug("Collector installer already exists")
                return installfilepath

        elif self.id is None:
            self.fail(
                msg="Error: There is currently no collector " +
                    "associated with this device. To download " +
                    " the installer, first create a collector " +
                    "for this device.")
        elif self.platform != "Linux":
            self.fail(
                msg="Error: LogicMonitor Collector must be " +
                "installed on a Linux device.")
        else:
            self.fail(
                msg="Error: Unable  to retrieve the installer from the server")

    def install(self):
        """Execute the LogicMonitor installer if not
        already installed"""
        logging.debug("Running Collector.install...")

        if self.platform == "Linux":
            logging.debug("Platform is Linux")

            installer = self.get_installer_binary()

            if self.info is None:
                logging.debug("Retriving collector information")
                self.info = self._get()

            if not os.path.exists(self.installdir + "/agent"):
                logging.debug("System changed")
                self.change = True

                if self.check_mode:
                    self.exit(changed=True)

                logging.debug("Setting installer file permissions")
                os.chmod(installer, 0744)

                logging.debug("Executing installer")
                p = (Popen([installer, "-y"],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE))
                ret, err = p.communicate()
                cmd_result = p.returncode

                if cmd_result != 0:
                    self.fail(
                        msg="Error: Unable to install collector: " + str(err))
                else:
                    logging.debug("Collector installed successfully")
            else:
                logging.debug("Collector already installed")
        else:
            self.fail(
                msg="Error: LogicMonitor Collector must be " +
                "installed on a Linux device")

    def uninstall(self):
        """Uninstall LogicMontitor collector from the system"""
        logging.debug("Running Collector.uninstall...")

        uninstallfile = self.installdir + "/agent/bin/uninstall.pl"

        if os.path.isfile(uninstallfile):
            logging.debug("Collector uninstall file exists")
            logging.debug("System changed")
            self.change = True

            if self.check_mode:
                self.exit(changed=True)

            logging.debug("Running collector uninstaller")
            p = (Popen([uninstallfile],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE))
            ret, err = p.communicate()

            if p.returncode != 0:
                self.fail(msg="Error: Unable to uninstall collector: " + str(err))
            else:
                logging.debug("Collector successfully uninstalled")
        else:
            if os.path.exists(self.installdir + "/agent"):
                (self.fail(
                    msg="Unable to uninstall LogicMonitor " +
                    "Collector. Can not find LogicMonitor " +
                    "uninstaller."))

    def start(self):
        """Start the LogicMonitor collector"""
        logging.debug("Running Collector.start")

        if self.platform == "Linux":
            logging.debug("Platform is Linux")

            output = Service.getStatus("logicmonitor-agent")
            if "is running" not in output:
                logging.debug("Service logicmonitor-agent is not running")
                logging.debug("System changed")
                self.change = True

                if self.check_mode:
                    self.exit(changed=True)

                logging.debug("Starting logicmonitor-agent service")
                (output, err) = Service.doAction("logicmonitor-agent", "start")

                if output != 0:
                    self.fail(
                        msg="Error: Failed starting logicmonitor-agent " +
                            "service. " + err)

            output = Service.getStatus("logicmonitor-watchdog")

            if "is running" not in output:
                logging.debug("Service logicmonitor-watchdog is not running")
                logging.debug("System changed")
                self.change = True

                if self.check_mode:
                    self.exit(changed=True)

                logging.debug("Starting logicmonitor-watchdog service")
                (output, err) = Service.doAction("logicmonitor-watchdog",
                                                 "start")

                if output != 0:
                    self.fail(
                        msg="Error: Failed starting logicmonitor-watchdog " +
                            "service. " + err)
        else:
            self.fail(
                msg="Error: LogicMonitor Collector must be " +
                "installed on a Linux device.")

    def restart(self):
        """Restart the LogicMonitor collector"""
        logging.debug("Running Collector.restart...")

        if self.platform == "Linux":
            logging.debug("Platform is Linux")

            logging.debug("Restarting logicmonitor-agent service")
            (output, err) = Service.doAction("logicmonitor-agent", "restart")

            if output != 0:
                self.fail(
                    msg="Error: Failed starting logicmonitor-agent " +
                        "service. " + err)

            logging.debug("Restarting logicmonitor-watchdog service")
            (output, err) = Service.doAction("logicmonitor-watchdog",
                                             "restart")

            if output != 0:
                self.fail(
                    msg="Error: Failed starting logicmonitor-watchdog " +
                        "service. " + err)
        else:
            (self.fail(
                msg="Error: LogicMonitor Collector must be installed " +
                    "on a Linux device."))

    def stop(self):
        """Stop the LogicMonitor collector"""
        logging.debug("Running Collector.stop...")

        if self.platform == "Linux":
            logging.debug("Platform is Linux")

            output = Service.getStatus("logicmonitor-agent")

            if "is running" in output:
                logging.debug("Service logicmonitor-agent is running")
                logging.debug("System changed")
                self.change = True

                if self.check_mode:
                    self.exit(changed=True)

                logging.debug("Stopping service logicmonitor-agent")
                (output, err) = Service.doAction("logicmonitor-agent", "stop")

                if output != 0:
                    self.fail(
                        msg="Error: Failed stopping logicmonitor-agent " +
                            "service. " + err)

            output = Service.getStatus("logicmonitor-watchdog")

            if "is running" in output:
                logging.debug("Service logicmonitor-watchdog is running")
                logging.debug("System changed")
                self.change = True

                if self.check_mode:
                    self.exit(changed=True)

                logging.debug("Stopping service logicmonitor-watchdog")
                (output, err) = Service.doAction("logicmonitor-watchdog",
                                                 "stop")

                if output != 0:
                    self.fail(
                        msg="Error: Failed stopping logicmonitor-watchdog " +
                            "service. " + err)
        else:
            self.fail(
                msg="Error: LogicMonitor Collector must be " +
                "installed on a Linux device.")

    def sdt(self):
        """Create a scheduled down time
        (maintenance window) for this host"""
        logging.debug("Running Collector.sdt...")

        logging.debug("System changed")
        self.change = True

        if self.check_mode:
            self.exit(changed=True)

        duration = self.duration
        starttime = self.starttime
        offsetstart = starttime

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
                self.fail(msg="Error: Unable to retrieve timezone offset")

        offsetend = offsetstart + timedelta(0, int(duration)*60)

        h = {"agentId": self.id,
             "type": 1,
             "notifyCC": True,
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

        logging.debug("Making RPC call to 'setAgentSDT'")
        resp = json.loads(self.rpc("setAgentSDT", h))

        if resp["status"] == 200:
            logging.debug("RPC call succeeded")
            return resp["data"]
        else:
            logging.debug("RPC call failed")
            self.fail(msg=resp["errmsg"])

    def site_facts(self):
        """Output current properties information for the Collector"""
        logging.debug("Running Collector.site_facts...")

        if self.info:
            logging.debug("Collector exists")
            props = self.get_properties(True)

            self.output_info(props)
        else:
            self.fail(msg="Error: Collector doesn't exit.")

    def _get(self):
        """Returns a JSON object representing this collector"""
        logging.debug("Running Collector._get...")

        ret = None

        collector_list = self.get_collectors()

        if collector_list is not None:
            logging.debug("Collectors returned")
            for collector in collector_list:
                if (
                    collector["description"] == self.description and
                    collector["description"] != ""
                ):
                    logging.debug(
                        "Collector matching description " +
                        self.description + " found."
                    )
                    ret = collector
                elif str(collector["id"]) == str(self.collector_id):
                    logging.debug(
                        "Collector id " + self.collector_id + " found."
                    )
                    ret = collector

        else:
            logging.debug("No collectors returned")
            ret = None
        return ret

    def _create(self):
        """Create a new collector in the associated
        LogicMonitor account"""
        logging.debug("Running Collector._create...")

        if self.platform == "Linux":
            logging.debug("Platform is Linux")
            ret = self.info or self._get()

            if ret is None:
                self.change = True
                logging.debug("System changed")

                if self.check_mode:
                    self.exit(changed=True)

                h = {"autogen": True,
                     "description": self.description}

                logging.debug("Making RPC call to 'addAgent'")
                create = (json.loads(self.rpc("addAgent", h)))

                if create["status"] is 200:
                    logging.debug("RPC call succeeded")
                    self.info = create["data"]
                    self.id = create["data"]["id"]
                    return create["data"]
                else:
                    self.fail(msg=create["errmsg"])
            else:
                self.info = ret
                self.id = ret["id"]
                return ret
        else:
            self.fail(
                msg="Error: LogicMonitor Collector must be " +
                "installed on a Linux device.")

    def _unregister(self):
        """Delete this collector from the associated
        LogicMonitor account"""
        logging.debug("Running Collector._unregister...")

        if self.info is None:
            logging.debug("Retrieving collector information")
            self.info = self._get()

        if self.info is not None:
            logging.debug("Collector found")
            logging.debug("System changed")
            self.change = True

            if self.check_mode:
                self.exit(changed=True)

            logging.debug("Making RPC call to 'deleteAgent'")
            delete = json.loads(self.rpc("deleteAgent",
                                         {"id": self.id}))

            if delete["status"] is 200:
                logging.debug("RPC call succeeded")
                return delete
            else:
                # The collector couldn't unregister. Start the service again
                logging.debug("Error unregistering collecting. " +
                              delete["errmsg"])
                logging.debug("The collector service will be restarted")

                self.start()
                self.fail(msg=delete["errmsg"])
        else:
            logging.debug("Collector not found")
            return None
