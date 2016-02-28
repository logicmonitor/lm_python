#!/usr/bin/env python2
# itop_lm_sync.py
#
# Synchronize iTop CMDB CIs to LogicMonitor
# Developed for Python 2.7.11
#
# External modules required:
#  - requests (pip install requests)
#  - argparse (pip install argparse)
#  - logicmonitor_core (pip install logicmonitor_core)
#
# LogicMonitor - Professional Services
# Bennett Borofka - bennett@logicmonitor.com

import argparse
import os
import requests
import sys
import xml.etree.ElementTree as ET
from logicmonitor_core.Hostgroup import Hostgroup
from logicmonitor_core.Host import Host


def getTree(itop_params, ci_type):
    url = 'http://' + itop_params["host"] + '/web/webservices/export.php?query=' + itop_params["query_phrasebook"] + '&format=xml'

    try: 
        # Get XML - write to temp file
        response = requests.get(url, auth=(itop_params["user"], itop_params["password"]))
        with open('tmp.xml', 'w') as code:
            code.write(response.content)
        
        # Read in XML file into ElementTree object
        tree = ET.ElementTree(file='tmp.xml')
        
        # Delete temp file
        code.close()
        os.remove('tmp.xml')
        
        return tree
    
    except: sys.exit("ERROR: Can't get XML export from iTop.")


def main():
    # Script arguments
    parser = argparse.ArgumentParser(description="Synchronize iTop CMDB CIs to LogicMonitor")
    parser.add_argument("-c", "--company", metavar="CUSTOMER_PORTAL", help="LogicMonitor account", required=True)
    parser.add_argument("-u", "--user", metavar="USERNAME", help="LogicMonitor username", required=True)
    parser.add_argument("-p", "--password", metavar="PASSWORD", help="LogicMonitor password", required=True)
    parser.add_argument("-ih", metavar="ITOP_HOST", help="iTop server hostname", required=True)
    parser.add_argument("-iu", metavar="ITOP_USERNAME", help="iTop server username", required=True)
    parser.add_argument("-ip", metavar="ITOP_PASSWORD", help="iTop server password", required=True)
    args = parser.parse_args()
    
    # Define variables
    lm_agentid = "Collector_Description"    # LM Collector ID to add Devices to
    
    # Define iTop parameters
    itop_params = {}
    itop_params["host"]  = args.ih    # iTop server hostname
    itop_params["user"] = args.iu    # iTop account
    itop_params["password"] = args.ip    # iTop password
    itop_params["query_phrasebook"] = '1'     # iTop query phrasebook # for getting XML

    # Define LogicMonitor parameters
    params = {}
    params["alertenable"] = False
    params["collector"] = lm_agentid
    params["description"] = "Synchronized from iTop CMDB"
    params["name"] = "iTop"
    params["fullpath"] = "/iTop"
    params["starttime"] = None
    params["duration"] = 30
    params["properties"] = {}
    params["company"] = args.company
    params["user"] = args.user
    params["password"] = args.password

    
    group = Hostgroup(params)
    group.add()

    # As of iTop 2.2, there is no "managementip" property for Printer or Hypervisor CIs, so only Server is synchronized in this script.
    tree = getTree(itop_params, 'server')
    print tree
    
    # Iterate through all Servers
    for elem in tree.iter('Server'):
        # Get CI name and management IP
        itop_name = str(elem.find('name').text)
        itop_managementip = str(elem.find('managementip').text)
        # Add to LM if there's an IP address / FQDN
        if itop_managementip != 'None': 
            # Define Server Host parameters
            params["groups"] = ["iTop"]
            params["displayname"] = itop_name
            params["hostname"] = itop_managementip
            params["properties"] = {"itop.source": "yes"}
            
            host = Host(params)
            host.add()

main()
