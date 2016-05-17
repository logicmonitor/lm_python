# lm_python

[![Build Status](https://travis-ci.org/logicmonitor/lm_python.svg?branch=master)](https://travis-ci.org/logicmonitor/lm_python)

LogicMonitor is a cloud-based, full stack, IT infrastructure monitoring
solution that allows you to manage your infrastructure from the cloud.
lm_python contains a set of stand-alone scripts which can be used to manage
your LogicMonitor account programmatically. These scripts are intended to be
functional examples of interaction with the LogicMonitor API in python.

## Prerequisites
In order to use these scripts there are a few things you will need.
- Access to a LogicMonitor account
- Sufficient permissions to perform the desired action
- Python version 2.7 or later

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
