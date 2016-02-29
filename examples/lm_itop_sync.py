#!/usr/bin/env python2
# lm_itop_sync.py
#
# Synchronize LogicMonitor devices to iTop CMDB (federation)
# Developed for Python 2.7.11
#
# External modules required:
#  - requests (pip install requests)
#  - ipaddress (pip install ipaddress)
#  - MySQLdb (pip install mysql-python)
#  - argparse (pip install argparse)
#  - logicmonitor_core (pip install logicmonitor_core)
#
# LogicMonitor - Professional Services
# Bennett Borofka - bennett@logicmonitor.com

import argparse
import MySQLdb  # case-sensitive
import requests
import sys
from logicmonitor_core.HostList import HostList


def main():
    # Script arguments
    description = "Synchronize LogicMonitor devices to iTop CMDB (federation)"
    parser = argparse.ArgumentParser(description)
    parser.add_argument("-c", "--company", metavar="CUSTOMER_PORTAL",
                        help="LogicMonitor account", required=True)
    parser.add_argument("-u", "--user", metavar="USERNAME",
                        help="LogicMonitor username", required=True)
    parser.add_argument("-p", "--password", metavar="PASSWORD",
                        help="LogicMonitor password", required=True)
    parser.add_argument("-ih", metavar="ITOP_HOST",
                        help="iTop server hostname", required=True)
    parser.add_argument("-iu", metavar="ITOP_USERNAME",
                        help="iTop server username", required=True)
    parser.add_argument("-ip", metavar="ITOP_PASSWORD",
                        help="iTop server password", required=True)
    parser.add_argument("-mh", metavar="MYSQL_HOST",
                        help="iTop MySQL server hostname (optional)")
    parser.add_argument("-mu", metavar="MYSQL_USERNAME",
                        help="iTop MySQL server username", required=True)
    parser.add_argument("-mp", metavar="MYSQL_PASSWORD",
                        help="iTop MySQL server password", required=True)
    parser.add_argument("-md", metavar="MYSQL_DATABASE",
                        help="iTop MySQL server database name", required=True)
    args = parser.parse_args()

    # Define iTop parameters
    itop_params = {}
    itop_params["host"] = args.ih    # iTop server hostname
    itop_params["user"] = args.iu    # iTop account
    itop_params["password"] = args.ip    # iTop password

    # Define iTop MySQL DB variables
    if args.mh is None:
        itop_mysql_host = args.ih    # Hostname of iTop MYSQL database
    else:
        itop_mysql_host = args.mh
    itop_mysql_username = args.mu    # iTop MYSQL DB account
    itop_mysql_password = args.mp    # iTop MYSQL DB password
    itop_mysql_db = args.md    # iTop MYSQL database name

    # MySQL database for Server class; replace x with #
    server_table = "synchro_data_server_1"
    # MySQL database for Printer class; replace y with #
    printer_table = "synchro_data_printer_2"
    # MySQL database for Hypervisor class; replace z with #
    hypervisor_table = "synchro_data_hypervisor_5"
    # iTop Organization ID that all devices will be categorized with (3 = Demo)
    itop_org_id = "3"

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

    except:
        sys.exit("ERROR: Can't connect to MySQL database.")

    print "Device(s) Added or Updated in iTop: "

    # Iterate through all Devices in portal and insert into
    # MySQL (temporary tables)
    for x in range(0, len(j["hosts"])):
        device_id = j["hosts"][x]["id"]    # Get Device id from JSON

        # Use the LM Device ID as the primary key in MySQL
        primary_key = device_id

        # Check if the "itop.class" property has been applied to the Device
        if "itop.class" in j["hosts"][x]["properties"]:

            itop_class = j["hosts"][x]["properties"]["itop.class"]
            name = j["hosts"][x]["properties"]["system.displayname"]
            ips = j["hosts"][x]["properties"]["system.ips"]
            description = j["hosts"][x]["properties"]["system.sysinfo"]

            # Split string of IP addresses and assign first IP address
            # to managementip
            managementip = ips.split(",")[0]

            # Skip the Device if it came from iTop
            if "itop.source" in j["hosts"][x]["properties"]:
                if j["hosts"][x]["properties"]["itop.source"] == "yes":
                    print " - " + name + " skipped."

            elif itop_class == "Server":
                # Concatenate SQL
                sql = "".join(["INSERT INTO ",
                               server_table,
                               " (primary_key, name, description, org_id, man",
                               "agementip) VALUES (%s, %s, %s, ",
                               itop_org_id,
                               ", %s)"])
                cur.execute(sql, (primary_key, name, description,
                                  managementip))
                db.commit()
                print " - " + name

            elif itop_class == "Printer":
                # Concatenate SQL
                sql = "".join(["INSERT INTO ",
                               printer_table,
                               " (primary_key, name, description, org_id) VAL",
                               "UES (%s, %s, %s, ",
                               itop_org_id,
                               ")"])
                print sql
                cur.execute(sql, (primary_key, name, description))
                db.commit()
                print " - " + name

            elif itop_class == "Hypervisor":
                # Concatenate SQL
                sql = "".join(["INSERT INTO ",
                               hypervisor_table,
                               " (primary_key, name, description, org_id) VAL",
                               "UES (%s, %s, %s, ",
                               itop_org_id,
                               ")"])
                cur.execute(sql, (primary_key, name, description))
                db.commit()
                print " - " + name

    # Execute iTop PHP script to insert MySQL temporary table data into
    # CMDB (create or update). Concatenate URL to PHP script
    url_sync = "".join(["http://",
                        itop_params["host"],
                        "/web/synchro/synchro_exec.php"])

    # Get the last character of each table, which provides the data_source #
    # Build comma-separate string to use in URL payload.
    ds_value = "".join([server_table[-1:],
                        ",",
                        printer_table[-1:],
                        ",",
                        hypervisor_table[-1:]])
    payload = {"data_sources": ds_value}

    # Remotely execute iTop PHP script
    requests.get(url_sync, auth=(itop_params["user"],
                                 itop_params["password"]), params=payload)

    # Empty MySQL tables
    sql = "TRUNCATE TABLE " + server_table
    cur.execute(sql)
    sql = "TRUNCATE TABLE " + printer_table
    cur.execute(sql)
    sql = "TRUNCATE TABLE " + hypervisor_table
    cur.execute(sql)
    db.commit()
    db.close()

main()
