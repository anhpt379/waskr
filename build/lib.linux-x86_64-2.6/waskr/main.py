#!/usr/bin/env python
#
# Copyright (c) 2009-2010 Alfredo Deza <alfredodeza [at] gmail [dot] com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import sys
from optparse import OptionParser
from os import path

from waskr import database, config
from waskr.web import server

WARNING = """ 
     +-------------------------------------------------+
     |                 ** WARNING **                   |
     |                                                 |
     |  You have not set a configuration file for the  |
     |  command line version of waskr.                 |
     |                                                 |
     |  To add a configuration file, run:              |
     |                                                 |
     |    waskr --add-config /path/to/config           |
     |                                                 |
     +-------------------------------------------------+
"""
 

class WaskrCommands(object):
    """A lot of complicated options can happen with Pacha, so 
    it is easier if everything lives under a class rather than
    the widely used main()"""

    def __init__(self, argv=None, test=False, parse=True, db=database.conf_db()):
        if argv is None:
            argv = sys.argv

        self.test = test
        if parse:
            self.parseArgs(argv)
        self.config = {}


    def msg(self, msg, std="out"):
        if std == "out":
            sys.stdout.write(msg)
        else:
            sys.stderr.write(msg)
        if not self.test:
            sys.exit(1)


    def add_config(self, path):
        abspath = os.path.abspath(path)
        self.db.add_config(abspath)
        self.msg("Configuration file added: %s" % abspath)


    def check_config(self):
        # if any commands are run, check for a MASTER config file Location
        config_db = self.db.get_config_path()
        config_file = None
        try:
            config_list = [i for i in self.db.get_config_path()]
            config_file = config_list[0][0]
            config = config.options(config_file)
            return config
        except IndexError:
            self.msg(msg=WARNING, std="err")
 

    def config_values(self):
        try:
            config_list = [i for i in self.db.get_config_path()]
            config_file = config_list[0][0]
            config = config.options(config_file)
            print "\nConfiguration file: %s\n" % config_file
            for i in config.items():
                print "%-15s= %-4s" % (i[0], i[1])
        except Exception, error:
            print "Could not complete command: %s" % error 



    def parseArgs(self, argv):
        parser = OptionParser(description="""
A stats engine for WSGI applications
    """
        ,version='0.0.9')

        parser.add_option('--server', action='store_true', help="""Runs the web server. 
    If no configuration file is passed localhost and port 8080 is used.""")
        parser.add_option('--conf', help="""Pass a INI configuration file""")
        parser.add_option('--add-user', help="""Adds a user email for the web interface""")
        parser.add_option('--remove-user', help="""Removes a user email from the web interface""")

        options, arguments = parser.parse_args()

        if len(sys.argv) <= 1:
            parser.print_help()

   
        if options.server:
            if options.conf and path.isfile(options.conf):
                configuration = config.options(options.conf)
                server.CONF = configuration
                server.main(configuration)
            else:        
                configuration = config.options('app.ini')
                server.CONF = configuration
                server.main(configuration)

        if options.add_user and options.conf:
            try:
                config = config.options(options.conf)
                db = database.Stats(config)
                db.add_user(options.add_user)
                print "User %s was added to the DB" % options.add_user
            except Exception, e:
                print 'waskrc could not add user: %s' % e
        
        if not options.conf:
            config = config.options('app.ini')
            db = database.Stats(config)

        if options.remove_user and options.conf:
            try:
                config = config.options(options.conf)
                db = database.Stats(config)
                db.remove_user(options.add_user)
                print "User %s removed from DB" % options.remove_user
            except Exception, e:
                print 'waskrc could not remove user: %s' % e

 

main = WaskrCommands

def main_():
    main()

