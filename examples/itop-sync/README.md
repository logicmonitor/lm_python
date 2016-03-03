# iTop CMDB Synchronization Scripts
These are sample Python scripts to synchronize LogicMonitor devices with [iTop CMDB 2.2.0](http://www.combodo.com/itop-193) using the [iTop data synchronization engine](https://wiki.openitop.org/doku.php?id=advancedtopics:data_synchronization)

There are two scripts, one for each direction of synchronization:

* **lm_itop_sync.py**: LogicMonitor -> iTop CMDB direction
* **itop_lm_sync.py**: iTop CMDB -> LogicMonitor direction

These scripts are for **education/demo purposes** and only support the following iTop CI classes:

* Server
* Hypervisor\*
* Printer\*

\* _The scripts synchronize Printer and Hypervisor CIs only in the LM->iTop direction; Server - both directions_


## Configure iTop
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

## Configure LogicMonitor
In your LogicMonitor portal, identify the Devices that you want to federate to iTop. Create a custom property `itop.class` and give it the value `Server`, `Printer` or `Hypervisor`. Apply the property at a Device or Device Group level. This will be used to federate devices from LogicMonitor to iTop with the appropriate CI class.

You will also need to identify the Collector description that you want to use, if synchronizing devices from iTop to LogicMonitor.

## Execute lm_itop_sync.py Script (LogicMonitor to iTop)
**lm_itop_sync.py** script can be executed on its own schedule, with the following arguments (gathered from iTop Configuration above):

```
$> python ./examples/lm_itop_sync.py -h
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

## Execute itop_lm_sync.py Script (iTop to LogicMonitor)
The **itop_lm_sync.py** script can be executed on its own schedule, with the following arguments (gathered from iTop and LogicMonitor Configurations above):

```
$> python ./examples/itop_lm_sync.py -h
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
