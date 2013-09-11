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

    
#end LogicMonitor
