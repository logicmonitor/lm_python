#!/usr/bin/python

import json
import logging
from datetime import datetime, timedelta
from LogicMonitor import LogicMonitor


class Datasource(LogicMonitor):

    def __init__(self, params):
        """Initializor for the LogicMonitor Datasource object"""
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Instantiating Datasource object")
        self.change = False
        self.params = params

        LogicMonitor.__init__(self, **params)

        self.id = self.params["id"]
        self.starttime = self.params["starttime"]
        self.duration = self.params["duration"]

    def sdt(self):
        """Create a scheduled down time
        (maintenance window) for this host"""
        logging.debug("Running Datasource.sdt...")

        logging.debug("System changed")
        self.change = True

        if self.check_mode:
            self.exit(changed=True)

        duration = self.duration
        starttime = self.starttime
        offsetstart = starttime

        if starttime:
            logging.debug("Start time specified")
            start = datetime.strptime(starttime, '%Y-%m-%d %H:%M')
            offsetstart = start
        else:
            logging.debug("No start time specified. Using default.")
            start = datetime.utcnow()

            # Use user UTC offset
            logging.debug("Making RPC call to 'getTimeZoneSetting'")
            accountresp = json.loads(self.rpc("getTimeZoneSetting", {}))

            if accountresp["status"] == 200:
                logging.debug("RPC call succeeded")

                offset = accountresp["data"]["offset"]
                offsetstart = start + timedelta(0, offset)
            else:
                self.fail(msg="Error: Unable to retrieve timezone offset")

        offsetend = offsetstart + timedelta(0, int(duration)*60)

        h = {"hostDataSourceId": self.id,
             "type": 1,
             "notifyCC": True,
             "year": offsetstart.year,
             "month": offsetstart.month-1,
             "day": offsetstart.day,
             "hour": offsetstart.hour,
             "minute": offsetstart.minute,
             "endYear": offsetend.year,
             "endMonth": offsetend.month-1,
             "endDay": offsetend.day,
             "endHour": offsetend.hour,
             "endMinute": offsetend.minute}

        logging.debug("Making RPC call to 'setHostDataSourceSDT'")
        resp = json.loads(self.rpc("setHostDataSourceSDT", h))

        if resp["status"] == 200:
            logging.debug("RPC call succeeded")
            return resp["data"]
        else:
            logging.debug("RPC call failed")
            self.fail(msg=resp["errmsg"])
