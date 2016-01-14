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

#### Platform specific tools
The following scripts are for managing specific types of device

**Linux collector management:**
- collector_add
- collector_remove
- collector_sdt

#### Platform agnostic tools
**Host management:**
- host_add
- host_remove
- host_update
- host_sdt
- host_info

** device group management:**
- hostgroup_add
- hostgroup_remove
- hostgroup_update
- hostgroup_sdt
- hostgroup_info

### collector_add.py
This idempotent script creates a new LogicMonitor collector for a Linux device.
This script assumes that you are running the script on the machine that you
are wanting to install a new collector. For more information about collector
management [click here](http://help.logicmonitor.com/using/managing-collectors/).

```
$> python collector_add.py -h
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
[click here](http://help.logicmonitor.com/using/managing-collectors/).

```
$> python collector_remove.py -h
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
[click here](http://help.logicmonitor.com/using/managing-collectors/).

```
$> python collector_sdt.py -h
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

### host_add.py
This idempotent script adds a new device to monitoring in your LogicMonitor
account. This addition includes setting host properties and group membership.
If the groups required for the addition of this host do not exist, they will
be created. For more information on managing hosts
[click here](http://help.logicmonitor.com/using/managing-hosts/).

```
$> python host_add.py -h
usage: host_add.py [-h] -c COMPANY -u USER -p PASSWORD -C COLLECTOR
                   [-H HOSTNAME] [-d DISPLAYNAME] [--description DESCRIPTION]
                   [-P PROPERTIES] [-g GROUPS [GROUPS ...]] [-a ALERTENABLE]
required arguments:
    -c COMPANY,   --company COMPANY                     LogicMonitor account
    -u USER,      --user USER                           LogicMonitor user name
    -p PASSWORD,  --password PASSWORD                   LogicMonitor password
    -C COLLECTOR, --collector COLLECTOR                 Collector FQDN
optional arguments:
  -h,             --help                                Show this help message and exit
  -H HOSTNAME,    --hostname HOSTNAME                   Machine hostname
  -d DISPLAYNAME, --displayname DISPLAYNAME             Machine display name
  -P PROPERTIES,  --properties PROPERTIES               A dictionary of properties to set for the host
  -a ALERTENABLE, --alertenable ALERTENABLE             Turn alerting on or off
  -g GROUPS [GROUPS ...], --groups GROUPS [GROUPS ...]  Groups the host should be a member of
  --description DESCRIPTION                             Text description of the host
```

### host_remove.py
This idempotent script removes a device from monitoring in your LogicMonitor
account. Note: this does not remove device groups that contain this host even
if they were created by adding this host. For more information on managing hosts
[click here](http://help.logicmonitor.com/using/managing-hosts/).

```
$> python host_remove.py -h
usage: host_remove.py [-h] -c COMPANY -u USER -p PASSWORD [-C COLLECTOR]
                      [-H HOSTNAME] [-d DISPLAYNAME]
required arguments:
    -c COMPANY,     --company COMPANY             LogicMonitor account
    -u USER,        --user USER                   LogicMonitor user name
    -p PASSWORD,    --password PASSWORD           LogicMonitor password
optional arguments:
    -h, --help                                    Show this help message and exit
    -C COLLECTOR,   --collector COLLECTOR         Collector FQDN
    -H HOSTNAME,    --hostname HOSTNAME           Machine hostname
    -d DISPLAYNAME, --displayname DISPLAYNAME     Machine display name
```

### host_update.py
This idempotent script updates a device already being monitored by your LogicMonitor account.
[click here](http://help.logicmonitor.com/using/managing-hosts/).

```
$> python host_update.py -h
usage: host_update.py [-h] -c COMPANY -u USER -p PASSWORD [-C COLLECTOR]
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
    -H HOSTNAME,    --hostname HOSTNAME                     Machine hostname
    -d DISPLAYNAME, --displayname DISPLAYNAME               Machine display name
    -P PROPERTIES,  --properties PROPERTIES                 A dictionary of properties to set for the host
    -a ALERTENABLE, --alertenable ALERTENABLE               Turn alerting on or off
    -g GROUPS [GROUPS ...], --groups GROUPS [GROUPS ...]    Groups the host should be a member of
    --description DESCRIPTION                               Text description of the host
```

### host_sdt.py
This script places a host in scheduled down time (SDT) or maintenance mode.
This will suppress alerting for the duration of the SDT. This script is not
idempotent and the same device can be put into SDT multiple times. For more
information on managing hosts
[click here](http://help.logicmonitor.com/using/managing-hosts/).


```
$> python host_sdt.py  -h
usage: host_sdt.py [-h] -c COMPANY -u USER -p PASSWORD [-C COLLECTOR]
                   [-H HOSTNAME] [-d DISPLAYNAME] [-D DURATION] [-s STARTTIME]
required arguments:
    -c COMPANY,   --company COMPANY               LogicMonitor account
    -u USER,      --user USER                     LogicMonitor user name
    -p PASSWORD,  --password PASSWORD             LogicMonitor password
optional arguments:
    -h,             --help                        Show this help message and exit
    -C COLLECTOR,   --collector COLLECTOR         Collector FQDN
    -H HOSTNAME,    --hostname HOSTNAME           Machine hostname
    -d DISPLAYNAME, --displayname DISPLAYNAME     Machine display name
    -D DURATION,    --duration DURATION           SDT duration
    -s STARTTIME,   --starttime STARTTIME         SDT start time
```

### host_info.py
This script retrieves and displays information about a device already being
monitored by your LogicMonitor account. For more information on managing hosts
[click here](http://help.logicmonitor.com/using/managing-hosts/).

```
$> python host_info.py -h
usage: host_info.py [-h] -c COMPANY -u USER -p PASSWORD -C COLLECTOR
                    [-H HOSTNAME] [-d DISPLAYNAME]
required arguments:
    -c COMPANY,     --company COMPANY           LogicMonitor account
    -u USER,        --user USER                 LogicMonitor user name
    -p PASSWORD,    --password PASSWORD         LogicMonitor password
optional arguments:
    -h, --help                                  Show this help message and exit
    -C COLLECTOR,   --collector COLLECTOR       Collector FQDN
    -H HOSTNAME,    --hostname HOSTNAME         Machine hostname
    -d DISPLAYNAME, --displayname DISPLAYNAME   Machine display name
```

### hostgroup_add.py
This idempotent script adds a new device group to your LogicMonitor account.
This addition includes setting host properties and group membership.
If the groups required for the addition of this host do not exist, they will
be created. For more information on managing device groups
[click here](http://help.logicmonitor.com/the-new-ui/devices/device-groups/).

```
$> python hostgroup_add.py -h
usage: hostgroup_add.py [-h] -c COMPANY -u USER -p PASSWORD -f FULLPATH
                        [--description DESCRIPTION] [-P PROPERTIES]
                        [-a ALERTENABLE]
required arguments:
    -c COMPANY,     --company COMPANY               LogicMonitor account
    -u USER,        --user USER                     LogicMonitor user name
    -p PASSWORD,    --password PASSWORD             LogicMonitor password
    -f FULLPATH,    --fullpath FULLPATH             Full path of the device group
optional arguments:
    -h,             --help                          Show this help message and exit
    -P PROPERTIES,  --properties PROPERTIES         A dictionary of properties to set for the host
    -a ALERTENABLE, --alertenable ALERTENABLE       Turn alerting on or off
    --description DESCRIPTION                       Text description of the host
```

### hostgroup_remove.py
This idempotent script removes a device group from your LogicMonitor account.
For more information on managing device groups
[click here](http://help.logicmonitor.com/the-new-ui/devices/device-groups/).

```
$> python hostgroup_remove.py -h
usage: hostgroup_remove.py [-h] -c COMPANY -u USER -p PASSWORD -f FULLPATH
required arguments:
    -c COMPANY,  --company COMPANY      LogicMonitor account
    -u USER,     --user USER            LogicMonitor user name
    -p PASSWORD, --password PASSWORD    LogicMonitor password
    -f FULLPATH, --fullpath FULLPATH    Full path of the device group
optional arguments:
    -h,          --help                 Show this help message and exit
```

### hostgroup_update.py
This idempotent script updates a device group that in your LogicMonitor account. If the device group doesn't exist, it will create it. For most information about
managing device groups
[click here](http://help.logicmonitor.com/the-new-ui/devices/device-groups/).

```
$> python hostgroup_update.py -h
usage: hostgroup_update.py [-h] -c COMPANY -u USER -p PASSWORD -f FULLPATH
                           [--description DESCRIPTION] [-P PROPERTIES]
                           [-a ALERTENABLE]
required arguments:
    -c COMPANY,     --company COMPANY           LogicMonitor account
    -u USER,        --user USER                 LogicMonitor user name
    -p PASSWORD,    --password PASSWORD         LogicMonitor password
    -f FULLPATH,    --fullpath FULLPATH         Full path of the device group
optional arguments:
    -h,             --help                      Show this help message and exit
    -P PROPERTIES,  --properties PROPERTIES     A dictionary of properties to set for the host
    -a ALERTENABLE, --alertenable ALERTENABLE   Turn alerting on or off
    --description DESCRIPTION                   Text description of the host
```

### hostgroup_sdt.py
This script places a device group in scheduled down time (SDT) or maintenance
mode. This will suppress alerting for the duration of the SDT. This script is
not idempotent and the same device can be put into SDT multiple times.
For more information on managing device groups
[click here](http://help.logicmonitor.com/the-new-ui/devices/device-groups/).

```
$> python hostgroup_sdt.py -h
usage: hostgroup_sdt.py [-h] -c COMPANY -u USER -p PASSWORD -f FULLPATH
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

### hostgroup_info.py
This script retrieves and displays information about a device group in your LogicMonitor account. For more information on managing device groups
[click here](http://help.logicmonitor.com/the-new-ui/devices/device-groups/).

```
$> python hostgroup_info.py -h
usage: hostgroup_info.py [-h] -c COMPANY -u USER -p PASSWORD -f FULLPATH
required arguments:
    -c COMPANY,  --company COMPANY        LogicMonitor account
    -u USER,     --user USER              LogicMonitor user name
    -p PASSWORD, --password PASSWORD      LogicMonitor password
    -f FULLPATH, --fullpath FULLPATH      Full path of the device group
optional arguments:
    -h,          --help                   Show this help message and exit
```
