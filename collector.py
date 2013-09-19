#!/usr/bin/python
#
# collector.py
# Purpose:
#   Allow for the use of logicmonitor collector management functions
#
# Parameters:
#
# Author: Ethan Culler-Mayeno
#

import json
import sys
import os
import platform
import subprocess
import datetime
from datetime import datetime, time, tzinfo, timedelta
from subprocess import call
from subprocess import Popen
from logicmonitor import LogicMonitor

class Collector(LogicMonitor):
        
    def __init__(self, description=None, installdir="/usr/local/logicmonitor", credentials_file="/tmp/lm_credentials.txt"):
        """Initializor for the LogicMonitor Collector object"""
        LogicMonitor.__init__(self, credentials_file)
        self.description = description or self.fqdn
        self.info = self._get()
        if self.info:
            self.id        = self.info["id"]
        else:
            self.id        = None
        #end if
        if not os.path.exists(installdir):
            os.makedir(installdir)
        #end if
        self.installdir    = installdir
        self.platform      = platform.system()
        self.is_64bits     = sys.maxsize > 2**32
    #end __init__
        
    ####################################
    #                                  #
    #    Public methods                #
    #                                  #
    ####################################
    
    
    def create(self):
        """Create a new collector in the LogicMonitor account associated with this device"""
        if self.id is None:
            create_json = json.loads(self.rpc("addAgent", {"autogen": True, "description": self.description}))
            if create_json["status"] is 200:
                self.info = create_json["data"]
                self.id = create_json["data"]["id"]
                return create_json["data"]
            else:
                print "Error: Unable to create a new collector"
                print json.dumps(create_json)
            #end if
        else:
            self.info = self._get()
            self.id = self.info['id']
            return self.info
        #end if
    #end create

    def delete(self):
        """Delete this collector from the associated LogicMonitor account"""
        if self.id is not None:
            delete_json = json.loads(self.rpc("deleteAgent", {"id": self.id}))
            if delete_json["status"] is 200:
                return delete_json["data"]
            else:
                print "Error: Unable to remove collector"
                print json.dumps(delete_json)
            #end if
        else:
            return None
        # end if
    #end delete
    
    def getinstallerbin(self):
        """Download the LogicMonitor collector installer binary"""
        arch = 32
        if self.is_64bits:
            arch = 64
        #end
        if self.platform == "Linux" and self.id is not None:
            installfilepath = self.installdir + "/logicmonitorsetup" + str(self.id) + "_" + str(arch) + ".bin"
            print installfilepath
            if not os.path.isfile(installfilepath):             #else create the installer file and return the file object
                with open(installfilepath, "w") as f:
                    installer = self.do("logicmonitorsetup", {"id": self.id, "arch": arch})
                    f.write(installer)
                f.closed
                #end with
            #end if not
            return installfilepath
        elif self.id is None:
            print "Error: There is currently no collector associated with this device. To download the installer, first create a collector for this device."
            return None
        elif self.platform != "Linux":
            print "Error: LogicMonitor Collector must be installed on a Linux device."
            return None
        else:
            print "Error: Something went wrong. We were unable to retrieve the installer from the server"
            return None
        #end if
    #end getinstallerbin
    
    def install(self):
        """Execute the LogicMonitor installer if not already installed"""
        if self.platform == "Linux":
            installer = self.getinstallerbin()
            if not os.path.exists(self.installdir + "/agent") or (self._get()["platform"] != 'linux'):
                os.chmod(installer, 755)
                output = call([installer, "-y"])
                if output != 0:
                    print "There was an issue installing the collector"
                #end if
            #end if not
        else:
            print "Error: LogicMonitor Collector must be installed on a Linux device."
        #end if
    #end install

    def uninstall(self):
        """Uninstall LogicMontitor collector from the system"""
        uninstallfile = self.installdir + "/agent/bin/uninstall.pl"
        if os.path.isfile(uninstallfile):
            output = call([uninstallfile])
            if output != 0:
                print "There was an issue installing the collector"
            #end if
        else:
            print "Unable to uninstall LogicMonitor Collector. Can not find LogicMonitor uninstaller."
        #end if
    #end uninstall
    
    def start(self):
        """Start the LogicMonitor collector"""
        if self.platform == "Linux":
            a = Popen(["service", "logicmonitor-agent", "status"], stdout=subprocess.PIPE)
            (aoutput, aerror) = a.communicate()
            if "is running" not in aoutput:
                call(["service", "logicmonitor-agent", "start"])
            #end if
            w = Popen(["service", "logicmonitor-watchdog", "status"], stdout=subprocess.PIPE)
            (woutput, werror) = w.communicate()
            if "is running" not in woutput:
                call(["service", "logicmonitor-watchdog", "start"])
            #end if
        else:
            print "Error: LogicMonitor Collector must be installed on a Linux device."
        #end if
    #end start
    
    def restart(self):
        """Restart the LogicMonitor collector"""
        """Start the LogicMonitor collector"""
        if self.platform == "Linux":
            call(["service", "logicmonitor-agent", "restart"])
            call(["service", "logicmonitor-watchdog", "restart"])
        else:
            print "Error: LogicMonitor Collector must be installed on a Linux device."
        #end if
    #end restart
    
    def stop(self):
        """Stop the LogicMonitor collector"""
        if self.platform == "Linux":
            a = Popen(["service", "logicmonitor-agent", "status"], stdout=subprocess.PIPE)
            (aoutput, aerror) = a.communicate()
            if "is running" in aoutput:
                call(["service", "logicmonitor-agent", "stop"])
            #end if
            w = Popen(["service", "logicmonitor-watchdog", "status"], stdout=subprocess.PIPE)
            (woutput, werror) = w.communicate()
            if "is running" in woutput:
                call(["service", "logicmonitor-watchdog", "stop"])
            #end if
        else:
            print "Error: LogicMonitor Collector must be installed on a Linux device."
        #end if
    #end stop
    
    def sdt(self, duration=30, starttime=None):
        """create a scheduled down time (maintenance window) for this host"""
        accountresp = json.loads(self.rpc("getCompanySettings", {}))
        if accountresp["status"] == 200:
            offset = accountresp["data"]["offset"]
            if starttime:
                start = datetime.strptime(starttime, '%Y-%m-%d %H:%M')
            else:
                start = datetime.utcnow()
            #end if
            offsetstart = start + timedelta(0, offset)
            offsetend = offsetstart + timedelta(0, duration*60)
            resp = json.loads(self.rpc("setAgentSDT", {"agentId": self.id, "type": 1, "notifyCC": True,
            "year": offsetstart.year, "month": offsetstart.month - 1, "day": offsetstart.day, "hour": offsetstart.hour, "minute": offsetstart.minute,
            "endYear": offsetend.year, "endMonth": offsetend.month - 1, "endDay": offsetend.day, "endHour": offsetend.hour, "endMinute": offsetend.minute,
            }))
            if resp["status"] == 200:
                return resp["data"]
            else:
                return None
            #end
        else:
            print "Error: Unable to retrieve list of hosts from server"
            exit(resp["status"])
        #end if
    #end sdt

    ####################################
    #                                  #
    #    internal methods              #
    #                                  #
    ####################################    

    def _get(self):
        """Returns a JSON object representing the collector"""
        collector_list = self.getcollectors()
        if collector_list is not None:
            for collector in collector_list:
                if collector["description"] == self.description:
                    return collector
                #end if
            #end for
        #end if
        return None
    #end _get        

#end Collector