#
# License:
#
#    Copyright (c) 2003-2006 ossim.net
#    Copyright (c) 2007-2010 AlienVault
#    All rights reserved.
#
#    This package is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; version 2 dated June, 1991.
#    You may not use, modify or distribute this program under any other version
#    of the GNU General Public License.
#
#    This package is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this package; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston,
#    MA  02110-1301  USA
#
#
# On Debian GNU/Linux systems, the complete text of the GNU General
# Public License can be found in `/usr/share/common-licenses/GPL-2'.
#
# Otherwise you can read it here: http://www.gnu.org/licenses/gpl-2.0.txt
#

#
# GLOBAL IMPORTS
#
import os, re, shutil, sys, time

#
# LOCAL IMPORTS
#
import ControlError
from ControlNmap import NmapManager
from ControlVAScanner import VAScannerManager
import ControlUtil
from ParserUtil import HostResolv
from Logger import Logger
import Utils
logger = Logger.logger



class ControlManager():
    """This class handles the control messages received from frameworkd"""

    __conf = None
    __nmap = None
    __vascanner = None

    __command_set = {'command_set': "List available control commands.", \
                     'os_info': "List basic OS information.", \
                     'agent_restart': "Restart the agent.", \
                     'config_file_backup': "Backup a config (.cfg) file.", \
                     'config_file_backup_list': "Lists all backups for a specified config (.cfg) file.", \
                     'config_file_restore': "Restore a congif (.cfg) file..", \
                     'config_file_get': "Grab the contents of a config (.cfg) file. Each line is hex'd gzip encoded.", \
                     'config_file_set': "Set the contents of a config (.cfg) file. Each line is hex'd gzip encoded.", \
                     'nmap_scan': "Perform an Nmap scan on a target IP address or IP address range.", \
                     'nmap_status': "Get the status of the Nmap working thread state.", \
                     'nmap_reset': "Reset the error state from the last failure incurred.", \
                     'nmap_report_list': "Lists all reports generated by this agent's specified report path.", \
                     'nmap_report_delete': "Delete a previously generated Nmap report.", \
                     'nmap_report_get': "Get a formatted response from a previously generated report.", \
                     'nmap_report_raw_get': "Get the raw XML from a previously generated report.", \
                     'va_scan': "Perform an VA scan on a target IP address or IP address range.", \
                     'va_status': "Get the status of the VA working thread state.", \
                     'va_reset': "Reset the error state from the last failure incurred.", \
                     'va_report_list': "Lists all reports generated by this agent's specified report path.", \
                     'va_report_delete': "Delete a previously generated report.", \
                     'va_report_get': "Get a formatted response from a previously generated report.", \
                     'va_report_raw_get': "Get the raw NBE from a previously generated VA report.", \
                     'refresh_asset_list':"Refresh the assets list for dns resolv", \
                     'remove_asset':"Remove one asset from asset list to resolv function", \
                     'add_asset':"Add new asset to asset list for resolv function",
    }

    __file_cache = {}


    def __init__(self, conf):
        self.__conf = conf
        self.__framework_id = conf.get("control-framework", "id")
        self.__response = []


    def process(self, conn, data):

        action = Utils.get_var("action=\"([^\"]+)\"", data)
        transaction = Utils.get_var("transaction=\"([^\"]+)\"", data)

        # reset queue the responses generated from the request
        self.__response = []

        # handle ping/pong foremost
        if data == "ping" or data == "pong":
            logger.debug("Got ponged.")
            return self.__response

        # raise exception if we have a bad request
        elif action == "" or transaction == "":
            raise ValueError('Incorrectly formatted control message.')
            return self.__response

        logger.info("Received message from the control framework: %s" % data)
        # construct base message
        message = 'control %s transaction="%s" id="%s"' % (action, transaction, str(self.__framework_id))

        # ensure the action is supported
        if action not in self.__command_set:
            self.__response.append(message + ' %s ackend\n' % ControlError.get(1000))
            return self.__response

        # report available command set
        if action == "command_set":
            commands = self.__command_set.keys()
            commands.sort()

            for k in commands:
                self.__response.append(message + ' command="%s" description="%s"\n' % (k, self.__command_set[k]))

            self.__response.append(message + ' %s ackend\n' % ControlError.get(0))
        elif action == "refresh_asset_list":
            HostResolv.refreshCache(data)
        elif action == "add_asset":
            HostResolv.add_asset(data)
        elif action == "remove_asset":
            HostResolv.remove_asset(data)
        # report basic OS statistics
        # report basic OS statistics
        elif action == "os_info":
            # push and close transaction (ie. ackend)
            message += ' system="%s" hostname="%s" release="%s" version="%s" architecture="%s"' % (os.uname())
            message += ' %s ackend\n' % (ControlError.get(0))
            self.__response.append(message + "\n")

        elif action == "agent_restart":
            self.__response.append(message + ' %s ackend\n' % ControlError.get(1006))

        # backup an ossim configuration file
        elif action == "config_file_backup":
            # ensure we have a "cfg" extension
            path = Utils.get_var("path=\"(/etc/ossim/[^\"]+.cfg)\"", data)

            # only valid paths should get through
            if path != "":
                # grab the current timestamp
                timestamp = str(int(time.time()))

                # the backup path appends the current timestamp
                backup_path = path + "." + timestamp

                try:
                    shutil.copyfile(path, backup_path)
                    self.__response.append(message + ' backup_path="%s" timestamp="%s" %s ackend\n' % (backup_path, timestamp, ControlError.get(0)))

                except Exception, e:
                    logger.warning('Unexpected exception reading file: ' + str(e))
                    self.__response.append(message + ' %s ackend\n' % (ControlError.get(1, str(e))))

            else:
                self.__response.append(message + ' %s ackend\n' % ControlError.get(1001))

        # list all backups available to an ossim configuration file
        elif action == "config_file_backup_list":
            # ensure we have a "cfg" extension
            path = Utils.get_var("path=\"(/etc/ossim/[^\"]+.cfg)\"", data)

            # only valid paths should get through
            if path != "":
                backup_files = self.__get_backup_file_list(path)

                for p in backup_files:
                    message += ' timestamp="%s"' % p[p.rfind(".") + 1:]

                self.__response.append(message + ' count="%i" %s ackend\n' % (len(backup_files), ControlError.get(0)))

            else:
                self.__response.append(message + ' %s ackend\n' & ControlError.get(1001))

        # list all backups available to an ossim configuration file
        elif action == "config_file_restore":
            # ensure we have a "cfg" extension
            path = Utils.get_var("path=\"(/etc/ossim/[^\"]+.cfg)\"", data)

            # only valid paths should get through
            if path != "":
                timestamp = Utils.get_var("timestamp=\"(\d+)\"", data)
                type = Utils.get_var("type=\"(overwrite|overwrite_pop+)\"", data)

                backup_file = self.__get_backup_file(path, timestamp)

                # grab the appropriate backup file
                if backup_file != "":
                    backup_destination = backup_file[:backup_file.rfind(".")]

                    try:
                        dir = os.path.dirname(path)

                        if type == "overwrite_clear":
                            shutil.move(dir + "/" + backup_file, dir + "/" + backup_destination)
                        else:
                            shutil.copyfile(dir + "/" + backup_file, dir + "/" + backup_destination)

                        self.__response.append(message + ' %s ackend\n' % ControlError.get(0))

                    except Exception, e:
                        self.__response.append(message + ' %s ackend\n' % ControlError.get(1, str(e)))

                # otherwise the backup file must not be available
                else:
                        self.__response.append(message + ' %s ackend\n' % ControlError.get(1002))

            else:
                self.__response.append(message + ' %s ackend\n' % ControlError.get(1001))

        # read an ossim configuration file
        elif action == "config_file_get":
            # ensure we have a "cfg" extension
            path = Utils.get_var("path=\"(/etc/ossim/[^\"]+.cfg)\"", data)

            # only valid paths should get through
            if path != "":
                try:
                    response = ControlUtil.get_file(path, message)
                    self.__response.extend(response)
                    self.__response.append(message + ' %s ackend\n' % ControlError.get(0))

                except Exception, e:
                    logger.warning('Unexpected exception reading file: ' + str(e))
                    self.__response.append(message + ' length="-1" line="" %s ackend\n' % ControlError.get(1, str(e)))
            else:
                self.__response.append(message + ' %s ackend\n' % ControlError.get(1001))

        # read an ossim configuration file
        elif action == "config_file_set":
            # ensure we have a "cfg" extension
            path = Utils.get_var("path=\"(/etc/ossim/[^\"]+.cfg)\"", data)
            type = Utils.get_var("type=\"(write|clear|commit)\"", data)

            if path != "" and type != "":

                # add new file entry if not existing
                if path not in self.__file_cache:
                    self.__file_cache[path] = []

                if type == "write":
                    contents_length = Utils.get_var("length=\"(\d+)\"", data)
                    contents_gziphex = Utils.get_var("line=\"([0-9a-fA-F]+)\"", data)

                    # ensure we have the require parameters for "write"
                    if contents_length != "" and contents_gziphex != "":
                        contents = zlib.decompress(unhexlify(contents_gziphex))

                        if len(contents) == contents_length or contents[-1] == '\n':
                            self.__file_cache[path].append(contents)
                            self.__response.append(message + ' %s ackend\n' % ControlError.get(0))

                        else:
                            self.__response.append(message + ' %s ackend\n' % ControlError.get(1005))

                    else:
                        self.__response.append(message + ' %s ackend\n' % ControlError.get(1004))

                elif type == "clear":
                    self.__file_cache[path] = []
                    self.__response.append(message + ' %s ackend\n' % ControlError.get(0))

                elif type == "commit":
                    try:
                        # open file for writing
                        f = open(path, 'w')

                        # dump the file cache
                        for l in self.__file_cache[path]:
                            f.write(l)

                        f.close()
                        self.__response.append(message + ' %s ackend\n' % ControlError.get(0))

                    except Exception, e:
                        self.__response.append(message + ' %s ackend\n' % ControlError.get(1, str(e)))

            else:
                self.__response.append(message + ' %s ackend\n' % ControlError.get(1003))

        # process all nmap_* commands via the NmapManager
        elif len(action) > 5 and action[:5] == "nmap_":
            if self.__nmap == None:
                logger.debug("Starting a new NMAP because I don't have once started, apparently.")
                self.__nmap = NmapManager(self.__conf)

            nmap_response = self.__nmap.process(data, message)
            self.__response.extend(nmap_response)

        # process all va_* commands via the VAScannerManager
        elif len(action) > 3 and action[:3] == "va_":
            if self.__vascanner == None:
                logger.debug("Starting a new VAScanner because I don't have once started, apparently.")
                self.__vascanner = VAScannerManager(self.__conf)

            vascanner_response = self.__vascanner.process(data, message)
            self.__response.extend(vascanner_response)

        return self.__response


    def __get_backup_file_list(self, path):
        dir = os.path.dirname(path)
        filter = re.compile(os.path.basename(path) + "\.(\d+)$")
        files = [f for f in os.listdir(dir) if filter.search(f)]
        files.sort()

        return files


    def __get_backup_file(self, path, timestamp=""):

        backup_files = self.__get_backup_file_list(path)

        # check we have some files to work with
        if len(backup_files) > 0:
            if timestamp != "":
                backup_file = path + "." + timestamp

                # check our requested backup file exists
                if backup_file in backup_files:
                    return backup_file

            # return the most recent
            else:
                return backup_files[-1]

        return ""