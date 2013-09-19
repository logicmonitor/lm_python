#!/usr/bin/python
#
# hostgroup.py
# Purpose:
#   Allow for the use of hostgroup management functions
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



class Hostgroup(LogicMonitor):
    
    def __init__(self, fullpath, description=None, properties={}, alertenable=True, credentials_file="/tmp/lm_credentials.txt"):
        """Initializor for the LogicMonitor host object"""
        LogicMonitor.__init__(self, credentials_file)
        self.fullpath = fullpath
        self.info = self.getgroup(self.fullpath)
        self.properties = properties
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
            properties_json = json.loads(self.rpc("getHostGroupProperties", {'hostGroupId': self.info["id"], "finalResult": False}))
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
        """Idempotent function to ensure that the host group exists in your LogicMonitor account"""
        hgid = self.creategroup(self.fullpath)
        self.info = self.getgroup(self.fullpath)
        return self.info
    #end create
    
    def update(self):
        """Idempotent function to ensure the host group settings (alertenable, properties, etc) in the LogicMonitor account match the current object."""
        if self.fullpath == "/":
            h =  self._buildhostgrouphash( self.fullpath, self.description, self.properties, self.alertenable)
            resp = json.loads(self.rpc("updateHostGroup", h))
            if resp["status"] == 200:
                return resp["data"]
            else:
                print "Error: unable to update the host."
                exit(resp["status"])
        elif self.info:
            if self.ischanged():
                h =  self._buildhostgrouphash( self.fullpath, self.description, self.properties, self.alertenable)
                h["id"] = self.info["id"]
                resp = json.loads(self.rpc("updateHostGroup", h))
                if resp["status"] == 200:
                    return resp["data"]
                else:
                    print "Error: unable to update the host."
                    exit(resp["status"])
            else:
                return self.info
            #end if
        else:            
            return self.add()
        #end if
    #end update
        
    def remove(self):
        """Idempotent function to ensure the host group does not exist in your LogicMonitor account"""
        if self.info:
            self.change = True
            if self.module.check_mode:
                self.module.exit_json(changed=True)
            #end if
            resp = json.loads(self.rpc("deleteHostGroup", {"hgId": self.info["id"]}))
        #end if
    #end if
    
    def ischanged(self):
        """Return true if the host doesn't match the LogicMonitor account"""
        ignore = []
        group = self.getgroup(self.fullpath)
        properties = self.getproperties()
        if properties is not None and group is not None:
            if group["alertEnable"] != self.alertenable:
                return True
            #end if
            if group["description"] != self.description:
                return True
            #end if
            p = {}
            for prop in properties:
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
            resp = json.loads(self.rpc("setHostGroupSDT", {"hostGroupId": self.info["id"], "type": 1, "dataSourceId": 0,
            "year": offsetstart.year, "month": offsetstart.month-1, "day": offsetstart.day, "hour": offsetstart.hour, "minute": offsetstart.minute,
            "endYear": offsetend.year, "endMonth": offsetend.month-1, "endDay": offsetend.day, "endHour": offsetend.hour, "endMinute": offsetend.minute,
            }))
            if resp["status"] == 200:
                return resp["data"]
            else:
                return None
            #end
        else:
            print "Error: Unable to retrieve timezone from server"
            exit(resp["status"])
        #end if
    #end sdt

    ####################################
    #                                  #
    #    internal utility methods      #
    #                                  #
    ####################################
    
    def _buildhostgrouphash(self, fullpath, description, properties, alertenable):
        """Return a property formated hash for the creation of a hostgroup using the rpc function"""
        h = {}
        if fullpath == "/":
            h["id"] = 1
        else:
            parentpath, name = fullpath.rsplit('/', 1)
            parent = self.getgroup(parentpath)
            if parent:
                h["parentID"] = parent["id"]
            else:
                h["parentID"] = 1
            #end if
            h["name"] = name
        #end if
        if description:
            h["description"] = description
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
                resp = json.loads(self.rpc('verifyProperties', {"hostGroupId": self.info["id"], "propName0": propname, "propValue0": self.properties[propname]}))
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
    

#end Class Hostgroup
