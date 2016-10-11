#!/usr/bin/python

import logging
import os
import platform
import subprocess
import sys
import time
from subprocess import Popen
from LogicMonitor import LogicMonitor
from Service import Service


class Collector(LogicMonitor):

    def __init__(self, params):
        '''Initializor for the LogicMonitor Collector object'''
        logging.basicConfig(level=logging.DEBUG)
        logging.debug('Instantiating Collector object')
        self.change = False
        self.params = params
        self.api = self.rest
        self.resource = '/setting/collectors/'
        self.path = self.resource + ''

        LogicMonitor.__init__(self, **params)

        if 'description' in self.params:
            self.description = self.params['description']
        else:
            self.description = self.fqdn

        if 'collector_id' in self.params:
            self.collector_id = self.params['collector_id']
        else:
            self.collector_id = None

        self.info = self._get()
        self.installdir = '/usr/local/logicmonitor'
        self.platform = platform.system()
        self.is_64bits = sys.maxsize > 2**32

        if 'duration' in self.params:
            self.duration = self.params['duration']
        if 'starttime' in self.params:
            self.starttime = self.params['starttime']

        if self.info is None:
            self.id = None
        else:
            self.id = self.info['id']
            self.path = self.resource + str(self.id)

    def create(self):
        '''Idempotent function to make sure that there is a running collector
        installed and registered'''
        logging.debug('Running Collector.create...')

        self._create()
        self.installer = self.get_installer_binary()
        self.install()
        self.start()
        logging.debug('Collector created')

    def remove(self):
        '''Idempotent function to make sure that there is not a running
        collector installed and registered'''
        logging.debug('Running Collector.destroy...')

        self.stop()
        self._unregister()
        self.uninstall()
        logging.debug('Collector removed')

    def get_installer_binary(self):
        '''Download the LogicMonitor collector installer binary'''
        logging.debug('Running Collector.get_installer_binary...')

        self._os_check()

        arch = 32
        if self.is_64bits:
            logging.debug('64 bit system')
            arch = 64
        else:
            logging.debug('32 bit system')

        if self.id is None:
            self.fail(msg='Error: Unable  to retrieve the installer from ' +
                          'the server')

        logging.debug('Agent ID is ' + str(self.id))

        installfilepath = (self.installdir + '/logicmonitorsetup' +
                           str(self.id) + '_' + str(arch) + '.bin')

        logging.debug('Looking for existing installer at ' + installfilepath)

        if os.path.isfile(installfilepath):
            logging.debug('Collector installer already exists')
            return installfilepath

        logging.debug('No previous installer found')
        self._changed(True)

        logging.debug('Downloading installer file')
        try:
            # create install dir if it doesn't exist
            if not os.path.exists(self.installdir):
                os.makedirs(self.installdir)
                logging.debug('Created installdir at ' + self.installdir)

            download_path = ('/setting/collectors/' + str(self.id) +
                             '/installers/linux' + str(arch))
            installer = self.api(download_path, 'GET')
            logging.debug('Writing installer file')
            with open(installfilepath, 'wb') as f:
                    for chunk in installer.iter_content():
                        if chunk:
                            f.write(chunk)
            return installfilepath
        except Exception as e:
            self.fail(msg='Unable to open installer file for writing. ' +
                          e.message)

    def install(self):
        '''Execute the LogicMonitor installer if not already installed'''
        logging.debug('Running Collector.install...')

        self._os_check()

        if self.info is None:
            logging.debug('Retriving collector information')
            self.info = self._get()

        if os.path.exists(self.installdir + '/agent'):
            logging.debug('Collector already installed')
            return

        self._changed(True)

        logging.debug('Setting installer file permissions')
        os.chmod(self.installer, 0o744)

        try:
            logging.debug('Executing installer')
            p = (Popen([self.installer, '-y'],
                       stdout=subprocess.PIPE,
                       cwd=self.installdir))
            ret, err = p.communicate()
            cmd_result = p.returncode
            if cmd_result != 0:
                self.fail(msg='Error: Unable to install collector: ' +
                              str(ret))
            logging.debug('Collector installed successfully')
        except Exception as e:
            self.fail('Error: Unable to installer collector. ' + e.message)

    def uninstall(self):
        '''Uninstall LogicMontitor collector from the system'''
        logging.debug('Running Collector.uninstall...')

        uninstallfile = self.installdir + '/agent/bin/uninstall.pl'

        if os.path.isfile(uninstallfile):
            logging.debug('Collector uninstall file exists')

            self._changed(True)

            try:
                logging.debug('Running collector uninstaller')
                p = (Popen([uninstallfile],
                           stdout=subprocess.PIPE))
                ret, err = p.communicate()
                cmd_result = p.returncode
                if cmd_result != 0:
                    self.fail(msg='Error: Unable to uninstall collector: ' +
                              str(err))

                logging.debug('Collector successfully uninstalled')
            except Exception as e:
                self.fail('Error: Unable to uninstall collector. ' + e.message)
        else:
            if os.path.exists(self.installdir + '/agent'):
                self.fail(msg='Unable to uninstall LogicMonitor Collector. ' +
                              'Can not find LogicMonitor uninstaller.')

    def start(self):
        '''Start the LogicMonitor collector'''
        logging.debug('Running Collector.start')

        self._os_check()

        output = Service.getStatus('logicmonitor-agent')
        if 'is running' not in output:
            self._changed(True)

            output = Service.start('logicmonitor-agent')
            if output != 0:
                self.fail(msg=str(output))

        output = Service.getStatus('logicmonitor-watchdog')
        if 'is running' not in output:
            self._changed(True)

            output = Service.start('logicmonitor-watchdog')
            if output != 0:
                self.fail(msg=str(output))

    def restart(self):
        '''Restart the LogicMonitor collector'''
        logging.debug('Running Collector.restart...')

        self._os_check()

        output = Service.restart('logicmonitor-agent')
        if output != 0:
            self.fail(msg=str(output))

        output = Service.restart('logicmonitor-watchdog')
        if output != 0:
            self.fail(msg=str(output))

    def stop(self):
        '''Stop the LogicMonitor collector'''
        logging.debug('Running Collector.stop...')

        self._os_check()

        output = Service.getStatus('logicmonitor-agent')
        if 'is running' in output:
            self._changed(True)

            output = Service.stop('logicmonitor-agent')
            if output != 0:
                self.fail(msg=str(output))

        output = Service.getStatus('logicmonitor-watchdog')
        if 'is running' in output:
            self._changed(True)

            output = Service.stop('logicmonitor-watchdog')
            if output != 0:
                self.fail(msg=str(output))

    def sdt(self):
        '''Create a scheduled down time (maintenance window) for this host'''
        logging.debug('Running Collector.sdt...')

        self._changed(True)

        starttime = self.starttime

        if starttime:
            logging.debug('Start time specified')
            pattern = '%Y-%m-%d %H:%M'
            starttime = int(time.mktime(time.strptime(starttime, pattern)) *
                            1000)
        else:
            logging.debug('No start time specified. Using now.')
            starttime = int(time.time() * 1000)

        endtime = starttime + (int(self.duration) * 1000 * 60)

        data = {
            'collectorId': self.id,
            'type': 'CollectorSDT',
            'sdtType': 1,
            'startDateTime': starttime,
            'endDateTime': endtime
        }

        resp = self.api('/sdt/sdts', 'POST', data)
        if resp.status_code != 200:
            self.fail('Error: Invalid API response')

        resp = resp.json()
        return resp['data']

    def site_facts(self):
        '''Output current properties information for the Collector'''
        logging.debug('Running Collector.site_facts...')

        if not self.info:
            self.fail(msg='Error: Collector does not exit.')

        logging.debug('Collector exists')
        props = self.get_properties(True)

        self.output_info(props)

    def _get(self):
        '''Returns a JSON object representing this collector'''
        logging.debug('Running Collector._get...')

        ret = None

        collector_list = self.get_collectors()
        if collector_list is None:
            logging.debug('No collectors returned')
            return ret

        logging.debug('Collectors returned')
        for collector in collector_list['items']:
            if (
                collector['description'] == self.description and
                collector['description'] != ''
            ):
                logging.debug('Collector matching description ' +
                              self.description + ' found.')
                ret = collector
                break
            elif str(collector['id']) == str(self.collector_id):
                logging.debug('Collector id ' + self.collector_id + ' found.')
                ret = collector
                break
        return ret

    def _create(self):
        '''Create a new collector in the associated LogicMonitor account'''
        logging.debug('Running Collector._create...')

        self._os_check()

        ret = self.info or self._get()
        if ret is not None:
            self.info = ret
            self.id = ret['id']
            self.path = self.resource + str(self.id)
            return ret

        self._changed(True)

        resp = self.api('/setting/collectors',
                        'POST',
                        {'name': self.description})
        if resp.status_code != 200:
            self.fail('Error: Invalid API response')

        resp = resp.json()
        if 'data' in resp and 'id' in resp['data']:
            self.info = resp['data']
            self.id = resp['data']['id']
            return resp['data']

    def get_collectors(self):
        '''Returns JSON object containing a list of LogicMonitor collectors'''
        logging.debug('Running LogicMonitor.get_collectors...')

        resp = self.api(self.resource, 'GET')
        if resp.status_code == 200:
            logging.debug('API call succeeded')
            resp = resp.json()
            return resp['data']
        else:
            self.fail(msg='Failed to retrieve collectors')

    def _unregister(self):
        '''Delete this collector from the associated LogicMonitor account'''
        logging.debug('Running Collector._unregister...')

        if self.info is None:
            logging.debug('Retrieving collector information')
            self.info = self._get()

        if self.info is None:
            logging.debug('Collector not found')
            return None

        logging.debug('Collector found')

        self._changed(True)

        resp = self.api(self.path, 'DELETE')
        if resp.status_code == 200:
            logging.debug('API call succeeded')
            return resp.json()
        else:
            # The collector couldn't unregister. Restart service
            logging.debug('Error unregistering collector.')
            logging.debug('The collector service will be restarted')

            self.start()
            self.fail(msg='Error unregistering collector.')

    def _os_check(self):
        if self.platform == 'Linux':
            logging.debug('Platform is Linux')
        else:
            self.fail(msg='Error: LogicMonitor Collector must be installed ' +
                          'on a Linux device.')

    def _changed(self, changed):
        self.change = changed
        if self.change is True:
            logging.debug('System changed')
            if self.check_mode:
                self.exit(changed=True)
