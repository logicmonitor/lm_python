# lm_python
LogicMonitor is a cloud-based, full stack, IT infrastructure monitoring
solution that allows you to manage your infrastructure from the cloud.
lm_python contains a set of stand-alone scripts which can be used to manage
your LogicMonitor account programmatically. These scripts are intended to be
functional examples of interaction with the LogicMonitor API in python.

## Prerequisites
In order to use these scripts there are a few things you will need.
- Access to a LogicMonitor account
- Sufficient permissions to perform the desired action
- A ruby run time environment (Python version [TODO] or later)

## Overview
This repository is not a complete set of scripts required to fully manage your
LogicMonitor account, nor does it cover the full extent of the LogicMonitor
API. Here's what we have so far.

## Setup
Install the lm_python package using a python package tool or clone the
repository from github and install the package locally

#### Package example
```
$> pip install logicmonitor_core
```

#### github example
```
$> git clone https://github.com/logicmonitor/lm_python.git
$> cd lm_python
$> python setup.py install
```

#### Platform specific tools
The following scripts are for managing specific types of device

**Linux collector management:**
- collector_add
- collector_remove
- collector_sdt

#### Platform agnostic tools
**Host management:**
- device_add
- device_remove
- device_update
- device_sdt
- device_info

** device group management:**
- devicegroup_add
- devicegroup_remove
- devicegroup_update
- devicegroup_sdt
- devicegroup_info

### collector_add.py
This idempotent script creates a new LogicMonitor collector for a Linux device.
This script assumes that you are running the script on the machine that you
are wanting to install a new collector. For more information about collector
management [click here](http://help.logicmonitor.com/the-new-ui/settings/collectors/what-is-the-logicmonitor-collector/).

```
$> python ./examples/collector_add.py -h
usage: collector_add.py [-h] -c COMPANY -u USER -p PASSWORD
required arguments:
    -c COMPANY,  --company COMPANY      LogicMonitor account
    -u USER,     --user USER            LogicMonitor user name
    -p PASSWORD, --password PASSWORD    LogicMonitor password
optional arguments:
    -h,          --help                 Show this help message and exit
```

### collector_remove.py
This idempotent script removes and existing LogicMonitor collector from a
Linux device. This script assumes that you are running the script on the
machine that you want to remove a collector from. For more information about
collector management
[click here](http://help.logicmonitor.com/the-new-ui/settings/collectors/what-is-the-logicmonitor-collector/).

```
$> python ./examples/collector_remove.py -h
usage: collector_remove.py [-h] -c COMPANY -u USER -p PASSWORD
required arguments:
    -c COMPANY,  --company COMPANY      LogicMonitor account
    -u USER,     --user USER            LogicMonitor user name
    -p PASSWORD, --password PASSWORD    LogicMonitor password
optional arguments:
    -h,          --help                 Show this help message and exit
```

### collector_sdt.py
This script sets places a collector in scheduled down time (SDT) or
maintenance mode. This script assumes that you are running the script on the
same machine as the collector to SDT. This script is not
idempotent and the same collector can be put into SDT multiple times.
For more information about collector management
[click here](http://help.logicmonitor.com/the-new-ui/settings/collectors/what-is-the-logicmonitor-collector/).

```
$> python ./examples/collector_sdt.py -h
usage: collector_sdt.py [-h] -c COMPANY -u USER -p PASSWORD [-d DURATION] [-s STARTTIME]
required arguments:
    -c COMPANY,  --company COMPANY      LogicMonitor account
    -u USER,     --user USER            LogicMonitor user name
    -p PASSWORD, --password PASSWORD    LogicMonitor password
optional arguments:
    -h,           --help                Show this help message and exit
    -d DURATION,  --duration DURATION   SDT duration
    -s STARTTIME, --starttime STARTTIME SDT start time
```

### device_add.py
This idempotent script adds a new device to monitoring in your LogicMonitor
account. This addition includes setting device properties and group membership.
If the groups required for the addition of this device do not exist, they will
be created. For more information on managing devices
[click here](http://help.logicmonitor.com/the-new-ui/devices/).

```
$> python ./examples/device_add.py -h
usage: device_add.py [-h] -c COMPANY -u USER -p PASSWORD -C COLLECTOR
                   [-H HOSTNAME] [-d DISPLAYNAME] [--description DESCRIPTION]
                   [-P PROPERTIES] [-g GROUPS [GROUPS ...]] [-a ALERTENABLE]
required arguments:
    -c COMPANY,   --company COMPANY                     LogicMonitor account
    -u USER,      --user USER                           LogicMonitor user name
    -p PASSWORD,  --password PASSWORD                   LogicMonitor password
    -C COLLECTOR, --collector COLLECTOR                 Collector FQDN
optional arguments:
  -h,             --help                                Show this help message and exit
  -H HOSTNAME,    --hostname HOSTNAME                   Device hostname
  -d DISPLAYNAME, --displayname DISPLAYNAME             Device display name
  -P PROPERTIES,  --properties PROPERTIES               A dictionary of properties to set for the device
  -a ALERTENABLE, --alertenable ALERTENABLE             Turn alerting on or off
  -g GROUPS [GROUPS ...], --groups GROUPS [GROUPS ...]  Groups the device should be a member of
  --description DESCRIPTION                             Text description of the device
```

### device_remove.py
This idempotent script removes a device from monitoring in your LogicMonitor
account. Note: this does not remove device groups that contain this device even
if they were created by adding this device. For more information on managing devices
[click here](http://help.logicmonitor.com/the-new-ui/devices/).

```
$> python ./examples/device_remove.py -h
usage: device_remove.py [-h] -c COMPANY -u USER -p PASSWORD [-C COLLECTOR]
                      [-H HOSTNAME] [-d DISPLAYNAME]
required arguments:
    -c COMPANY,     --company COMPANY             LogicMonitor account
    -u USER,        --user USER                   LogicMonitor user name
    -p PASSWORD,    --password PASSWORD           LogicMonitor password
optional arguments:
    -h, --help                                    Show this help message and exit
    -C COLLECTOR,   --collector COLLECTOR         Collector FQDN
    -H HOSTNAME,    --hostname HOSTNAME           Device hostname
    -d DISPLAYNAME, --displayname DISPLAYNAME     Device display name
```

### device_update.py
This idempotent script updates a device already being monitored by your LogicMonitor account.
[click here](http://help.logicmonitor.com/the-new-ui/devices/).

```
$> python ./examples/device_update.py -h
usage: device_update.py [-h] -c COMPANY -u USER -p PASSWORD [-C COLLECTOR]
                      [-H HOSTNAME] [-d DISPLAYNAME]
                      [--description DESCRIPTION] [-P PROPERTIES]
                      [-g GROUPS [GROUPS ...]] [-a ALERTENABLE]
required arguments:
    -c COMPANY,     --company COMPANY                       LogicMonitor account
    -u USER,        --user USER                             LogicMonitor user name
    -p PASSWORD,    --password PASSWORD                     LogicMonitor password
optional arguments:
    -h,             --help                                  Show this help message and exit
    -C COLLECTOR,   --collector COLLECTOR                   Collector FQDN
    -H HOSTNAME,    --hostname HOSTNAME                     Device hostname
    -d DISPLAYNAME, --displayname DISPLAYNAME               Device display name
    -P PROPERTIES,  --properties PROPERTIES                 A dictionary of properties to set for the device
    -a ALERTENABLE, --alertenable ALERTENABLE               Turn alerting on or off
    -g GROUPS [GROUPS ...], --groups GROUPS [GROUPS ...]    Groups the device should be a member of
    --description DESCRIPTION                               Text description of the device
```

### device_sdt.py
This script places a host in scheduled down time (SDT) or maintenance mode.
This will suppress alerting for the duration of the SDT. This script is not
idempotent and the same device can be put into SDT multiple times. For more
information on managing devices
[click here](http://help.logicmonitor.com/the-new-ui/devices/).


```
$> python ./examples/device_sdt.py  -h
usage: device_sdt.py [-h] -c COMPANY -u USER -p PASSWORD [-C COLLECTOR]
                   [-H HOSTNAME] [-d DISPLAYNAME] [-D DURATION] [-s STARTTIME]
required arguments:
    -c COMPANY,   --company COMPANY               LogicMonitor account
    -u USER,      --user USER                     LogicMonitor user name
    -p PASSWORD,  --password PASSWORD             LogicMonitor password
optional arguments:
    -h,             --help                        Show this help message and exit
    -C COLLECTOR,   --collector COLLECTOR         Collector FQDN
    -H HOSTNAME,    --hostname HOSTNAME           Device hostname
    -d DISPLAYNAME, --displayname DISPLAYNAME     Device display name
    -D DURATION,    --duration DURATION           SDT duration
    -s STARTTIME,   --starttime STARTTIME         SDT start time
```

### device_info.py
This script retrieves and displays information about a device already being
monitored by your LogicMonitor account. For more information on managing devices
[click here](http://help.logicmonitor.com/the-new-ui/devices/).

```
$> python ./examples/device_info.py -h
usage: device_info.py [-h] -c COMPANY -u USER -p PASSWORD -C COLLECTOR
                    [-H HOSTNAME] [-d DISPLAYNAME]
required arguments:
    -c COMPANY,     --company COMPANY           LogicMonitor account
    -u USER,        --user USER                 LogicMonitor user name
    -p PASSWORD,    --password PASSWORD         LogicMonitor password
optional arguments:
    -h, --help                                  Show this help message and exit
    -C COLLECTOR,   --collector COLLECTOR       Collector FQDN
    -H HOSTNAME,    --hostname HOSTNAME         Device hostname
    -d DISPLAYNAME, --displayname DISPLAYNAME   Device display name
```

### datasource_sdt.py
This script places a datasource in scheduled down time (SDT) or maintenance mode.
This will suppress alerting for the duration of the SDT. This script is not
idempotent and the same datasource can be put into SDT multiple times. For more
information on managing datasources
[click here](http://help.logicmonitor.com/the-new-ui/devices/device-datasources-instances/).


```
$> python ./examples/datasource_sdt.py  -h
usage: device_sdt.py [-h] -c COMPANY -u USER -p PASSWORD -i ID
    required arguments:
       -c COMPANY,     --company COMPANY           LogicMonitor account
       -u USER,        --user USER                 LogicMonitor user name
       -p PASSWORD,    --password PASSWORD         LogicMonitor password
    optional arguments:
       -h, --help                                  Show this help message and exit
       -i ID,          --id ID                     Datasource ID
```

### list_devices.py
This script list all devices being monitored in your LogicMonitor account.

```
$> python ./examples/list_devices.py -h
usage: device_add.py [-h] -c COMPANY -u USER -p PASSWORD
                   [-g GROUP]
required arguments:
    -c COMPANY,   --company COMPANY                     LogicMonitor account
    -u USER,      --user USER                           LogicMonitor user name
    -p PASSWORD,  --password PASSWORD                   LogicMonitor password

optional arguments:
  -h,             --help                                Show this help message and exit
  -g GROUP,    --group GROUP                   Limit the results to hosts in the group path specified. Example: /Servers

```

### devicegroup_add.py
This idempotent script adds a new device group to your LogicMonitor account.
This addition includes setting device properties and group membership.
If the groups required for the addition of this device do not exist, they will
be created. For more information on managing device groups
[click here](http://help.logicmonitor.com/the-new-ui/devices/device-groups/).

```
$> python ./examples/devicegroup_add.py -h
usage: devicegroup_add.py [-h] -c COMPANY -u USER -p PASSWORD -f FULLPATH
                        [--description DESCRIPTION] [-P PROPERTIES]
                        [-a ALERTENABLE]
required arguments:
    -c COMPANY,     --company COMPANY               LogicMonitor account
    -u USER,        --user USER                     LogicMonitor user name
    -p PASSWORD,    --password PASSWORD             LogicMonitor password
    -f FULLPATH,    --fullpath FULLPATH             Full path of the device group
optional arguments:
    -h,             --help                          Show this help message and exit
    -P PROPERTIES,  --properties PROPERTIES         A dictionary of properties to set for the device
    -a ALERTENABLE, --alertenable ALERTENABLE       Turn alerting on or off
    --description DESCRIPTION                       Text description of the device
```

### devicegroup_remove.py
This idempotent script removes a device group from your LogicMonitor account.
For more information on managing device groups
[click here](http://help.logicmonitor.com/the-new-ui/devices/device-groups/).

```
$> python ./examples/devicegroup_remove.py -h
usage: devicegroup_remove.py [-h] -c COMPANY -u USER -p PASSWORD -f FULLPATH
required arguments:
    -c COMPANY,  --company COMPANY      LogicMonitor account
    -u USER,     --user USER            LogicMonitor user name
    -p PASSWORD, --password PASSWORD    LogicMonitor password
    -f FULLPATH, --fullpath FULLPATH    Full path of the device group
optional arguments:
    -h,          --help                 Show this help message and exit
```

### devicegroup_update.py
This idempotent script updates a device group that in your LogicMonitor account. If the device group doesn't exist, it will create it. For most information about
managing device groups
[click here](http://help.logicmonitor.com/the-new-ui/devices/device-groups/).

```
$> python ./examples/devicegroup_update.py -h
usage: devicegroup_update.py [-h] -c COMPANY -u USER -p PASSWORD -f FULLPATH
                           [--description DESCRIPTION] [-P PROPERTIES]
                           [-a ALERTENABLE]
required arguments:
    -c COMPANY,     --company COMPANY           LogicMonitor account
    -u USER,        --user USER                 LogicMonitor user name
    -p PASSWORD,    --password PASSWORD         LogicMonitor password
    -f FULLPATH,    --fullpath FULLPATH         Full path of the device group
optional arguments:
    -h,             --help                      Show this help message and exit
    -P PROPERTIES,  --properties PROPERTIES     A dictionary of properties to set for the device
    -a ALERTENABLE, --alertenable ALERTENABLE   Turn alerting on or off
    --description DESCRIPTION                   Text description of the device
```

### devicegroup_sdt.py
This script places a device group in scheduled down time (SDT) or maintenance
mode. This will suppress alerting for the duration of the SDT. This script is
not idempotent and the same device can be put into SDT multiple times.
For more information on managing device groups
[click here](http://help.logicmonitor.com/the-new-ui/devices/device-groups/).

```
$> python ./examples/devicegroup_sdt.py -h
usage: devicegroup_sdt.py [-h] -c COMPANY -u USER -p PASSWORD -f FULLPATH
                        [-D DURATION] [-s STARTTIME]
required arguments:
    -c COMPANY,   --company COMPANY       LogicMonitor account
    -u USER,      --user USER             LogicMonitor user name
    -p PASSWORD,  --password PASSWORD     LogicMonitor password
    -f FULLPATH,  --fullpath FULLPATH     Full path of the device group
optional arguments:
    -h,           --help                  Show this help message and exit
    -D DURATION,  --duration DURATION     SDT duration
    -s STARTTIME, --starttime STARTTIME   SDT start time
```

### devicegroup_info.py
This script retrieves and displays information about a device group in your LogicMonitor account. For more information on managing device groups
[click here](http://help.logicmonitor.com/the-new-ui/devices/device-groups/).

```
$> python ./examples/devicegroup_info.py -h
usage: devicegroup_info.py [-h] -c COMPANY -u USER -p PASSWORD -f FULLPATH
required arguments:
    -c COMPANY,  --company COMPANY        LogicMonitor account
    -u USER,     --user USER              LogicMonitor user name
    -p PASSWORD, --password PASSWORD      LogicMonitor password
    -f FULLPATH, --fullpath FULLPATH      Full path of the device group
optional arguments:
    -h,          --help                   Show this help message and exit
```

### iTop CMDB Synchronization Scripts
These are sample Python scripts to synchronize LogicMonitor devices with [iTop CMDB 2.2.0](http://www.combodo.com/itop-193) using the [iTop data synchronization engine](https://wiki.openitop.org/doku.php?id=advancedtopics:data_synchronization)

There are two scripts, one for each direction of synchronization:

* **lm_itop_sync.py**: LogicMonitor -> iTop CMDB direction
* **itop_lm_sync.py**: iTop CMDB -> LogicMonitor direction

These scripts are for **education/demo purposes** and only support the following iTop CI classes:

* Server
* Hypervisor\*
* Printer\*

\* _The scripts synchronize Printer and Hypervisor CIs only in the LM->iTop direction; Server - both directions_


#### Configure iTop
With iTop installed, login as an administrator and create your **Synchronization Data Sources**. This creates a target CI class to synchronize devices to and a unique database staging table for each CI type.

1. Navigate to *Admin tools > Synchronization Data Sources* and click *New...*
2. Create a new *Synchronization Data Source* for each iTop class we'll use in this demo:

* Name: server
* Target class: Server
* Name: printer
* Target class: Printer
* Name: hypervisor
* Target class: Hypervisor

In your MySQL database, check for the tables that were created when you created the three Synchronization Data Sources, they should be similar to:

* synchro_data_server_x
* synchro_data_printer_y
* synchro_data_hypervisor_z

You will need to use the tables as arguments when running the **lm_itop_sync.py** script.

Next, you'll need to create a **Query Phrasebook** in iTop to export Server CIs to XML format.

1. Navigate to *Admin tools > Query phrasebook* and click *New...*
2. Give it the following configuration:

* Name: Get Servers
* Description: Get Servers
* Expression: SELECT Server

Note the query # in the **URL to use for MS-Excel web queries field**. You will need to pass this # as a script argument for **lm_itop_sync.py**.

Lastly, you'll need to get the **Organization ID** you want to create the devices under, in iTop. Navigate to *Data administration > Organizations* and get the decide if you want to use one of the three defaults (*Demo*, *IT Department* or *My Company/Department*) or create a new one.

Once decided, hover your cursor over the organization name and note the # of the organization id, it will be used as an argument with the **lm_itop_sync.py** script.

#### Configure LogicMonitor
In your LogicMonitor portal, identify the Devices that you want to federate to iTop. Create a custom property `itop.class` and give it the value `Server`, `Printer` or `Hypervisor`. Apply the property at a Device or Device Group level. This will be used to federate devices from LogicMonitor to iTop with the appropriate CI class.

You will also need to identify the Collector description that you want to use, if synchronizing devices from iTop to LogicMonitor.

#### Execute lm_itop_sync.py Script (LogicMonitor to iTop)
**lm_itop_sync.py** script can be executed on its own schedule, with the following arguments (gathered from iTop Configuration above):

```
$> python lm_itop_sync.py -h
usage: Synchronize LogicMonitor devices to iTop CMDB (federation)
       [-h] -c CUSTOMER_PORTAL -u USERNAME -p PASSWORD -ih ITOP_HOST -iu
       ITOP_USERNAME -ip ITOP_PASSWORD -io ITOP_ORG_ID [-mh MYSQL_HOST] -mu
       MYSQL_USERNAME -mp MYSQL_PASSWORD -md MYSQL_DATABASE -st SERVER_TABLE
       -pt PRINTER_TABLE -ht HYPERVISOR_TABLE

optional arguments:
  -h, --help            show this help message and exit
  -c CUSTOMER_PORTAL, --company CUSTOMER_PORTAL
                        LogicMonitor account
  -u USERNAME, --user USERNAME
                        LogicMonitor username
  -p PASSWORD, --password PASSWORD
                        LogicMonitor password
  -ih ITOP_HOST         iTop server hostname
  -iu ITOP_USERNAME     iTop server username
  -ip ITOP_PASSWORD     iTop server password
  -io ITOP_ORG_ID       iTop organization id
  -mh MYSQL_HOST        iTop MySQL server hostname (optional)
  -mu MYSQL_USERNAME    iTop MySQL server username
  -mp MYSQL_PASSWORD    iTop MySQL server password
  -md MYSQL_DATABASE    iTop MySQL server database name
  -st SERVER_TABLE      iTop MySQL staging table name for Server class
  -pt PRINTER_TABLE     iTop MySQL staging table name for Printer class
  -ht HYPERVISOR_TABLE  iTop MySQL staging table name for Hypervisor class
```

#### Execute itop_lm_sync.py Script (iTop to LogicMonitor)
The **itop_lm_sync.py** script can be executed on its own schedule, with the following arguments (gathered from iTop and LogicMonitor Configurations above):

```
$> python itop_lm_sync.py -h
usage: Synchronize iTop CMDB CIs to LogicMonitor [-h] -c CUSTOMER_PORTAL -u
                                                 USERNAME -p PASSWORD -cn
                                                 COLLECTOR_NAME -ih ITOP_HOST
                                                 -iu ITOP_USERNAME -ip
                                                 ITOP_PASSWORD -iq
                                                 ITOP_QUERY_PHRASEBOOK

optional arguments:
  -h, --help            show this help message and exit
  -c CUSTOMER_PORTAL, --company CUSTOMER_PORTAL
                        LogicMonitor account
  -u USERNAME, --user USERNAME
                        LogicMonitor username
  -p PASSWORD, --password PASSWORD
                        LogicMonitor password
  -cn COLLECTOR_NAME    LogicMonitor collector description
  -ih ITOP_HOST         iTop server hostname
  -iu ITOP_USERNAME     iTop server username
  -ip ITOP_PASSWORD     iTop server password
  -iq ITOP_QUERY_PHRASEBOOK
                        iTop query phrasebook #
```

If a device originates from iTop CMDB and is added to LogicMonitor, a custom `itop.source` property will be created with a value of `yes`. This is to flag the device not to be synchronized back to iTop in the **lm_itop_sync.py** script.
