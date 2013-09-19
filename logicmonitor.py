#!/usr/bin/python
#
# logicmonitor.py
# Purpose:
#   Allow for the use of logicmonitor management functions
#
# Parameters:
#
# Author: Ethan Culler-Mayeno
#

import urllib
import urlparse
import sys
import json
import os
import shlex
import hashlib
import socket

class LogicMonitor:
            
    def __init__(self, credential_file):
        """docstring for %s"""
        lm_credentials_file     = open(credential_file)
        lm_credentials          = json.loads(lm_credentials_file.read())
        self.company            = lm_credentials["company"]
        self.user               = lm_credentials["user"]
        self.password           = lm_credentials["password"]
        if lm_credentials["digest"]:
            self.password_digest = self.password
        else:
            m = hashlib.md5()
            m.update(self.password)
            self.password_digest = m.hexdigest()
        #end if lm_credentials
        self.fqdn           = socket.getfqdn()

    #end __init__
        
    def rpc(self, action, params):
        """Make a call to the LogicMonitor RPC library and return the response"""
        param_str = urllib.urlencode(params)
        creds = urllib.urlencode({"c": self.company, "u": self.user, "pmd5": self.password_digest})
        if param_str:
            param_str = param_str + "&"
        param_str = param_str + creds
        try:
            f = urllib.urlopen("https://{0}.logicmonitor.com/santaba/rpc/{1}?{2}".format(self.company, action, param_str))
            return f.read()
        except IOError as ioe:
            print ioe
            sys.exit(1)
        #end try
    #end rpc

    def do(self, action, params):
        """Make a call to the LogicMonitor server \"do\" function"""
        param_str = urllib.urlencode(params)
        creds = urllib.urlencode({"c": self.company, "u": self.user, "pmd5": self.password_digest})
        if param_str:
            param_str = param_str + "&"
        param_str = param_str + creds
        try:
            f = urllib.urlopen("https://{0}.logicmonitor.com/santaba/do/{1}?{2}".format(self.company, action, param_str))
            return f.read()
        except IOError as ioe:
            print ioe
            sys.exit(1)
        #end try
    #end do

    def getcollectors(self):
        """Returns a JSON object containing a list of LogicMonitor collectors"""
        resp = self.rpc("getAgents", {})
        resp_json = json.loads(resp)
        if resp_json["status"] is 200:
             return resp_json["data"]
        else:
            self.module.fail_json(msg=resp)
        #end if
    #end getcollectors
    
    def getgroup(self, fullpath):
        """Return a JSON object with the current state of a group in your LogicMonitor account"""
        resp = json.loads(self.rpc("getHostGroups", {}))
        if resp["status"] == 200:
            groups = resp["data"]
            for group in groups:
                if group["fullPath"] == fullpath.lstrip('/'):
                    return group
                #end if
            #end for
        #end if
        return None
    #end getgroup

    def creategroup(self, fullpath):
        """Recursively create a path of host groups. return value is the id of the newly created hostgroup in your LogicMonitor account"""
        if self.getgroup(fullpath):
            #group already exists
            return self.getgroup(fullpath)["id"]
        #end if
        if fullpath == "/":
            #manage the global settings
            return 1
        #end if
        parentpath, name = fullpath.rsplit('/', 1)
        parentgroup = self.getgroup(parentpath)
        if parentpath == "":
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
            resp = json.loads(self.rpc("addHostGroup", {"name": name, "parentId": self.creategroup(parentpath), "alertEnable": True}))
            if resp["status"] == 200:
                return resp["data"]["id"]
            else:
                print "Error: unable to create new hostgroup"
                print json.dumps(resp)
            #end if
            
        #end if
    #end creategroup
    
    def gethostbyhostname(self, hostname, collector):
        hostlist_json = json.loads(self.rpc("getHosts", {"hostGroupId": 1}))
        if collector is not None and hostlist_json["status"] == 200:
            hosts = hostlist_json["data"]["hosts"]
            for host in hosts:
                if host["hostName"] == hostname and host["agentId"] == collector["id"]:
                    return host
                #end if
            #end for
        #end if
        return None
    #end gethostbyhostname

    def gethostbydisplayname(self, displayname):
        host_json = json.loads(self.rpc("getHost", {"displayName": displayname}))
        if host_json["status"] == 200:
            return host_json["data"]
        else:
            return None
        #end if
    #end gethostbydisplayname

    def getcollectorbyid(self, id):
        """return the collector json object for the collector with matching ID in your LogicMonitor account"""
        collector_json = json.loads(self.rpc("getAgent", {"id": id}))
        if collector_json["status"] == 200:
            return collector_json["data"]
        else:
            exit(resp["status"])
        #end if
    #end getcollectorbyid
    
    def getcollectorbydescription(self, description):
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
    
    
#end LogicMonitor
