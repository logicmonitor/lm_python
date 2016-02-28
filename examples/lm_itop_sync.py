#!/usr/bin/env python2
# lm_itop_sync.py
#
# Synchronize LogicMonitor devices to iTop CMDB (federation)
# Developed for Python 2.7.11
#
# External modules required:
#  - requests (pip install requests)
#  - MySQLdb (pip install mysql-python)
#  - argparse (pip install argparse)
#  - logicmonitor_core (pip install logicmonitor_core)
#
# LogicMonitor - Professional Services
# Bennett Borofka - bennett@logicmonitor.com

import argparse
import json
import MySQLdb # case-sensitive
import requests
import subprocess
import sys
import re
from logicmonitor_core.HostList import HostList

# Function to determine if a string is a valid IPv4 address
def is_ipv4(ip):
    match = re.match("^(\d{0,3})\.(\d{0,3})\.(\d{0,3})\.(\d{0,3})$", ip)
    if not match:
        return False
    quad = []
    for number in match.groups():
        quad.append(int(number))
    if quad[0] < 1:
        return False
    for number in quad:
        if number > 255 or number < 0:
            return False
    return True

def main():
    # Script arguments
    parser = argparse.ArgumentParser(description="Synchronize LogicMonitor devices to iTop CMDB (federation)")
    parser.add_argument("-c", "--company", metavar="CUSTOMER_PORTAL", help="LogicMonitor account", required=True)
    parser.add_argument("-u", "--user", metavar="USERNAME", help="LogicMonitor username", required=True)
    parser.add_argument("-p", "--password", metavar="PASSWORD", help="LogicMonitor password", required=True)
    parser.add_argument("-ih", metavar="ITOP_HOST", help="iTop server hostname", required=True)
    parser.add_argument("-iu", metavar="ITOP_USERNAME", help="iTop server username", required=True)
    parser.add_argument("-ip", metavar="ITOP_PASSWORD", help="iTop server password", required=True)
    parser.add_argument("-mh", metavar="MYSQL_HOST", help="iTop MySQL server hostname (optional - use ITOP_HOST if unspecified)")
    parser.add_argument("-mu", metavar="MYSQL_USERNAME", help="iTop MySQL server username", required=True)
    parser.add_argument("-mp", metavar="MYSQL_PASSWORD", help="iTop MySQL server password", required=True)
    parser.add_argument("-md", metavar="MYSQL_DATABASE", help="iTop MySQL server database name", required=True)
    args = parser.parse_args()

    # Define iTop parameters
    itop_params = {}
    itop_params["host"]  = args.ih    # iTop server hostname
    itop_params["user"] = args.iu    # iTop account
    itop_params["password"] = args.ip    # iTop password

    # Define iTop MySQL DB variables
    if args.mh is None: itop_mysql_host = args.ih    # Hostname of iTop MYSQL database
    else: itop_mysql_host = args.mh
    itop_mysql_username = args.mu    # iTop MYSQL DB account
    itop_mysql_password = args.mp    # iTop MYSQL DB password
    itop_mysql_db = args.md    # iTop MYSQL database name
    server_table = 'synchro_data_server_x'  # MySQL database for Server class; replace x with #
    printer_table = 'synchro_data_printer_y'    # MySQL database for Printer class; replace y with #
    hypervisor_table = 'synchro_data_hypervisor_z'  # MySQL database for Hypervisor class; replace z with #
    itop_org_id = '3'    # iTop Organization ID that all devices will be categorized with (3 = Demo)

    # Define LogicMonitor parameters
    params = {}
    params["group"] = None
    params["company"] = args.company
    params["user"] = args.user
    params["password"] = args.password

    # Get JSON of all devices
    host_list = HostList(params)
    j = host_list.get_hosts()

    try:
        # Setup MySQL connection
        db = MySQLdb.connect(host=itop_mysql_host,
                                user=itop_mysql_username,
                                passwd=itop_mysql_password,
                                db=itop_mysql_db)
        cur = db.cursor()
 
    except: sys.exit("ERROR: Can't connect to MySQL database.")
    
    print "Device(s) Added or Updated in iTop: "

    # Iterate through all Devices in portal and insert into MySQL (temporary tables)
    for x in range(0, len(j['hosts'])):
        device_id = j['hosts'][x]['id']    # Get Device id from JSON
        
        primary_key = device_id # Use the LM Device ID as the primary key in MySQL
         
        # Check if the 'itop.class' property has been applied to the Device
        if 'itop.class' in j['hosts'][x]['properties']: 
            
            itop_class = j['hosts'][x]['properties']['itop.class']
            name = j['hosts'][x]['properties']['system.displayname']
            hostname = j['hosts'][x]['properties']['system.hostname']
            description = j['hosts'][x]['properties']['system.sysinfo']
            
            # If the LM hostname for the device is a valid IP address, insert it into iTop; otherwise ignore FQDN
            if is_ipv4(hostname): managementip = hostname
            else: managementip = ""
            
            # Skip the Device if it came from iTop
            if 'itop.source' in j['hosts'][x]['properties']:
                if j['hosts'][x]['properties']['itop.source'] == 'yes': print ' - ' + name + ' skipped.'
                
            elif itop_class == 'Server':
                # Concatenate SQL
                sql = 'INSERT INTO ' + server_table + ' (primary_key, name, description, org_id, managementip) VALUES (%s, %s, %s, ' + itop_org_id + ', %s)'
                cur.execute(sql, (primary_key, name, description, managementip))
                db.commit()
                print ' - ' + name
                
            elif itop_class == 'Printer':
                # Concatenate SQL
                sql = 'INSERT INTO ' + printer_table + ' (primary_key, name, description, org_id) VALUES (%s, %s, %s, ' + itop_org_id + ')'
                cur.execute(sql, (primary_key, name, description))
                db.commit()
                print ' - ' + name
        
            elif itop_class == 'Hypervisor':
                # Concatenate SQL
                sql = 'INSERT INTO ' + hypervisor_table + ' (primary_key, name, description, org_id) VALUES (%s, %s, %s, ' + itop_org_id + ')'
                cur.execute(sql, (primary_key, name, description))
                db.commit()
                print ' - ' + name

    # Execute iTop PHP script to insert MySQL temporary table data into CMDB (create or update)
    # Concatenate URL to PHP script
    url_sync = 'http://' + itop_params["host"] + '/web/synchro/synchro_exec.php'

    # Get the last character of each table, which provides the data_source #. Build comma-separate string to use in URL payload.
    ds_value = server_table[-1:] + ',' + printer_table[-1:] + ',' + hypervisor_table[-1:]
    payload = {'data_sources': ds_value}

    # Remotely execute iTop PHP script
    response = requests.get(url_sync, auth=(itop_params["user"], itop_params["password"]), params=payload)

    # Empty MySQL tables
    sql = 'TRUNCATE TABLE ' + server_table
    cur.execute(sql)
    sql = 'TRUNCATE TABLE ' + printer_table
    cur.execute(sql)
    sql = 'TRUNCATE TABLE ' + hypervisor_table
    cur.execute(sql)
    db.commit()
    db.close()

main()
