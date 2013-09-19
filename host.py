#!/usr/bin/python
#
# host.py
# Purpose:
#   Allow for the use of host management functions
#
# Parameters:
#
# Author: Ethan Culler-Mayeno
#

import sys
import json
import os
import datetime
from datetime import datetime, time, tzinfo, timedelta
from logicmonitor import LogicMonitor

class Host(LogicMonitor):
    
    def __init__(self, collector, hostname=None, displayname=None, description=None, properties={}, groups=[], alertenable=True, credentials_file="/tmp/lm_credentials.txt"):
        """Initializor for the LogicMonitor host object"""
        LogicMonitor.__init__(self, credentials_file)
        self.collector = self.getcollectorbydescription(collector)
        self.hostname = hostname or self.fqdn
        self.displayname = displayname or self.fqdn
        self.info = self.gethostbydisplayname(self.displayname) or self.gethostbyhostname(self.hostname)
        self.properties = properties
        self.groups = groups
        self.description = description
        self.alertenable = alertenable
    #end __init__
    
    ####################################
    #                                  #
    #    Public methods                #
    #                                  #
    ####################################    
    
    
    def getproperties(self):
        """Returns a hash of the properties associated with this LogicMonitor host"""
        if self.info:
            properties_json = json.loads(self.rpc("getHostProperties", {'hostId': self.info["id"], "filterSystemProperties": True, "finalResult": False}))
            if properties_json["status"] == 200:
                return properties_json["data"]
            else:
                print "Error: there was an issue retrieving the host properties"
                print json.dumps(properties_json)
                exit(properties_json["status"])
            #end if
        else:
            print "Unable to find LogicMonitor host which matches {0} ({1})".format(self.displayname, self.hostname) 
            return None
        #end
    #end getproperties

    def setproperties(self, propertyhash):
        """update the host to have the properties contained in the property hash"""
        self.properties = propertyhash
    #end setproperties

    def add(self):
        """Add this device to monitoring in your LogicMonitor account"""
        if not self.info:
            return self.rpc("addHost", self._buildhosthash( self.hostname, self.displayname, self.collector, self.description, self.groups, self.properties, self.alertenable))
        #end if
    #end add_host

    def update(self):
        """This method takes changes made to this host and applies them to the corresponding host in your LogicMonitor account."""
        if self.info:
            if self.ischanged():
                h =  self._buildhosthash( self.hostname, self.displayname, self.collector, self.description, self.groups, self.properties, self.alertenable)
                h["id"] = self.info["id"]
                resp = json.loads(self.rpc("updateHost", h))
                if resp["status"] == 200:
                    return resp["data"]
                else:
                    print "Error: unable to update the host."
                    exit(resp["status"])
            else:
                return self.info
            #end if
        else:
            return self.rpc("addHost", self._buildhosthash( self.hostname, self.displayname, self.collector, self.description, self.groups, self.properties, self.alertenable))
        #end if
    #end update_host
        
    def remove(self):
        """remove this host from your LogicMonitor account"""
        if self.info:
            return json.loads(self.rpc("deleteHost", {"id": self.info["id"], "deleteFromSystem": True, "hostGroupId": 1}))
        else:
            exit(resp["status"])
        #end if
    #end remove
    
    def ischanged(self):
        """Return true if the host doesn't match the LogicMonitor account"""
        ignore = ['system.categories', 'snmp.version']
        hostresp = self.gethostbydisplayname(self.displayname) or self.gethostbyhostname(self.hostname)
        propresp = self.getproperties()
        if propresp and hostresp:
            if hostresp["alertEnable"] != self.alertenable:
                return True
            #end if
            if hostresp["description"] != self.description:
                return True
            #end if
            if hostresp["displayedAs"] != self.displayname:
                return True
            #end if
            if hostresp["agentId"] != self.collector["id"]:
                return True
            #end if
            g = []
            fullpathinids = hostresp["fullPathInIds"]
            for path in fullpathinids:
                hgresp = json.loads(self.rpc("getHostGroup", {'hostGroupId': path[-1]}))
                if hgresp["status"] == 200 and hgresp["data"]["appliesTo"] == "":
                    g.append(path[-1])
                #end if
            #end for
            for group in self.groups:
                groupjson = self.getgroup(group)
                if groupjson is None:
                    return True
                elif groupjson['id'] not in g:
                    return True
                else:
                    g.remove(groupjson['id'])
                #end if
            #end for
            if g != []:
                return True
            #end
            p = {}
            for prop in propresp:
                if prop["name"] not in ignore:
                    if "*******" in prop["value"] and self._verifyproperty(prop["name"]):
                        p[prop["name"]] = self.properties[prop["name"]]
                    else:
                        p[prop["name"]] = prop["value"]
                    #end if
                #end if
            #end for
            
            if set(p) != set(self.properties):
                return True
            #end if
        else:
            exit(1)
        #end if
        return False
    #end ischanged

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
            resp = json.loads(self.rpc("setHostSDT", {"hostId": self.info["id"], "type": 1, 
            "year": offsetstart.year, "month": offsetstart.month-1, "day": offsetstart.day, "hour": offsetstart.hour, "minute": offsetstart.minute,
            "endYear": offsetend.year, "endMonth": offsetend.month-1, "endDay": offsetend.day, "endHour": offsetend.hour, "endMinute": offsetend.minute,
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
    #    internal utility methods      #
    #                                  #
    ####################################    

        
    def _buildhosthash(self, hostname, displayname, collector, description, groups, properties, alertenable):
        """Return a property formated hash for the creation of a host using the rpc function"""
        h = {}
        h["hostName"] = hostname
        h["displayedAs"] = displayname
        if collector:
            h["agentId"] = collector["id"]
        else:
            print "Error: Unable to build host hash. No collector found."
        #end if
        if description:
            h["description"] = description
        #end if
        if groups != []:
            groupids = ""
            for group in groups:
                groupids = groupids + str(self.creategroup(group)) + ","
            #end for
            h["hostGroupIds"] = groupids.rstrip(',')
        #end if
        if properties != {}:
            propnum = 0
            for key, value in properties.iteritems():
                h["propName{0}".format(str(propnum))] = key
                h["propValue{0}".format(str(propnum))] = value
                propnum = propnum + 1
            #end for
        #end if
        h["alertEnable"] = alertenable
        return h
    #end _buildhosthash
    
    def _verifyproperty(self, propname):
        """Check with LogicMonitor server to verify property is unchanged"""
        if self.info:
            if propname not in self.properties:
                return False
            else:
                resp = json.loads(self.rpc('verifyProperties', {"hostId": self.info["id"], "propName0": propname, "propValue0": self.properties[propname]}))
                if resp["status"] == 200:
                    return resp["data"]["match"]
                else:
                    print "Error: unable to get verification from server."
                    exit(resp["status"])
            #end if
        else:
            print "Error: Can not verify properties of a host which doesn't exist"
            exit(1)
    #end _verifyproperty
    
    
#end class lm_host
