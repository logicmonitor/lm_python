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
        self.collector = self._getcollectorbydescription(collector)
        #end if
        self.hostname = hostname or self.fqdn
        self.displayname = displayname or self.fqdn
        self.info = self._gethostbydisplayname(self.displayname) or self._gethostbyhostname(self.hostname)
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
        ignore = ['system.categories']
        hostresp = self._gethostbydisplayname(self.displayname) or self._gethostbyhostname(self.hostname)
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
                groupjson = self._getgroup(group)
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
            "year": offsetstart.year, "month": offsetstart.month, "day": offsetstart.day, "hour": offsetstart.hour, "minute": offsetstart.minute,
            "endYear": offsetend.year, "endMonth": offsetend.month, "endDay": offsetend.day, "endHour": offsetend.hour, "endMinute": offsetend.minute,
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

    def _gethostbyhostname(self, hostname):
        hostlist_json = json.loads(self.rpc("getHosts", {"hostGroupId": 1}))
        if hostlist_json["status"] == 200:
            hosts = hostlist_json["data"]["hosts"]
            for host in hosts:
                if host["hostName"] == hostname and host["agentId"] == self.collector["id"]:
                    return host
                #end if
            #end for
            return None
        else:
            print "Error: Unable to retrieve list of hosts from server"
            exit(resp["status"])
        #end if
    #end gethostbyhostname

    def _gethostbydisplayname(self, displayname):
        host_json = json.loads(self.rpc("getHost", {"displayName": displayname}))
        if host_json["status"] == 200:
            return host_json["data"]
        else:
            return None
        #end if
    #end gethostbydisplayname

    def _getcollectorbyid(self, id):
        """return the collector json object for the collector with matching ID in your LogicMonitor account"""
        collector_json = json.loads(self.rpc("getAgent", {"id": id}))
        if collector_json["status"] == 200:
            return collector_json["data"]
        else:
            exit(resp["status"])
        #end if
    #end getcollectorbyid
    
    def _getcollectorbydescription(self, description):
        """return the collector json object for the collector with the matching FQDN (description) in your LogicMonitor account"""
        collector_list = self.getcollectors()
        if collector_list is not None:
            for collector in collector_list:
                if collector["description"] == description:
                    return collector
                #end if
            #end for
        #end if
        return None
    #end getcollectorbydescription
    
    def _getgroup(self, fullpath):
        """Return a JSON object with the current state of a group in your LogicMonitor account"""
        resp = json.loads(self.rpc("getHostGroups", {}))
        if resp["status"] == 200:
            groups = resp["data"]
            for group in groups:
                if group["fullPath"] == fullpath.lstrip('/'):
                    return group
                #end if
            #end for
        else:
            print "Error: Unable to retreive the list of host groups from the server."
            exit(resp["status"])
        #end if
        return None
    #end _getgroup
    
    def _creategroup(self, fullpath):
        """Recursively create a path of host groups. return value is the id of the newly created hostgroup in your LogicMonitor account"""
        if self._getgroup(fullpath):
            return self._getgroup(fullpath)["id"]
        #end if
        parentpath, name = fullpath.rsplit('/', 1)
        parentgroup = self._getgroup(parentpath)
        if fullpath == "/":
            return 1
        elif parentpath == "":
            parentid = 1
            resp = json.loads(self.rpc("addHostGroup", {"name": name, "parentId": parentid, "alertEnable": True}))
            if resp["status"] == 200:
                return resp["data"]["id"]
            else:
                print "Error: unable to create new hostgroup"
                exit(resp["status"])
            #end if
        elif parentgroup:
            parentid = parentgroup["id"]
            resp = json.loads(self.rpc("addHostGroup", {"name": name, "parentId": parentid, "alertEnable": True}))
            if resp["status"] == 200:
                return resp["data"]["id"]
            else:
                print "Error: unable to create new hostgroup"
                exit(resp["status"])
            #end if
        else:
            resp = json.loads(self.rpc("addHostGroup", {"name": name, "parentId": self._creategroup(parentpath), "alertEnable": True}))
            if resp["status"] == 200:
                return resp["data"]["id"]
            else:
                print "Error: unable to create new hostgroup"
                print json.dumps(resp)
            #end if
            
        #end if
    #end _createparentgroup
    
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
                groupids = groupids + str(self._creategroup(group)) + ","
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
