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
from optparse import OptionParser, OptionGroup

from waskr import database
from waskr.config import options
from waskr.plugins import init_plugin_system, find_plugins

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
        self.db = db
        if argv is None:
            argv = sys.argv

        self.got_plugins = False
        self.test = test
        self.config = {}
        if parse:
            self.parseArgs(argv)

    def enable_plugins(self):
        try:
            plugin_path = self.config['plugin_path']
            plugins = self.config['plugins'].split(' ')
        except KeyError:
            return False
        except AttributeError:
            return False
        if plugin_path is False or plugins is None:
            return False
        else:
            init_plugin_system({'plugin_path': plugin_path, 'plugins': plugins})
            find_plugins()
       

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
            conf = options(config_file)
            self.config = conf
            return conf
        except IndexError:
            return False
 

    def config_values(self):
        try:
            config_list = [i for i in self.db.get_config_path()]
            config_file = config_list[0][0]
            conf = options(config_file)
            print "\nConfiguration file: %s\n" % config_file
            for i in conf.items():
                print "%-15s= %-4s" % (i[0], i[1])
        except Exception, error:
            self.msg("Could not complete command: %s" % error, std="err") 


    def clean_plugin_option(self, option):
        if '--' in option:
            option = option.replace('--', '')
        if '-' in option:
            option = option.replace('-', '_')
        return option


    def parseArgs(self, argv):
        parser = OptionParser(description="""
A stats engine for WSGI applications
    """
        ,version='0.0.9')

        parser.add_option('--server', action='store_true', help="""Runs the web server. 
 If no configuration file is passed localhost and port 8080 is used.""")
        parser.add_option('--add-config', 
                help="""Adds (overwrites) a config file to the command line app""")
        parser.add_option('--config-values', action="store_true", 
                help="""Show the current parsed config values""")

        # Plugin Group
        plugin_group = OptionGroup(parser, "Plugin Options", "Extend via\
 plugins that can run with this command line tool. If activated you should see\
 them displayed here.")

        if self.check_config() and self.enable_plugins() is not False:
            from waskr.plugins import find_plugins
            self.got_plugins = True
            plugin_options = {}
            for plugin in find_plugins():
                try:
                    cmd = plugin()
                    cmd.config = self.config
                    info = cmd.command()
                    # register it with OptParse to avoid errors
                    plugin_group.add_option(info['option'], action=info['action'],
                        help=info['description'])

                    # now register with a dict so we now what to call when we hit 
                    # that option 
                    plugin_options[info['option']] = cmd 

                except AttributeError:
                    pass # You may have not added what we need to implement
                         # your plugin

        parser.add_option_group(plugin_group)

        options, arguments = parser.parse_args()

        if options.add_config:
            self.add_config(options.add_config)

        # make sure we have a config to work with 
        if self.check_config() == False:
            self.msg(msg=WARNING, std="err")

        if len(sys.argv) <= 1:
            parser.print_help()

        if options.config_values:
            self.config_values()
   
        if options.server:
            # imports here to avoid db connection errors
            from waskr.web import server
            server.CONF = self.config
            server.main(self.config)

        # if we hit the end of *our* options, loop over the plugin options: 
        elif self.got_plugins:
            for i in plugin_options:
                if i in sys.argv[1:]:
                    obj = plugin_options[i]
                    option_value = None
                    if len(sys.argv) == 3:
                        option_value = sys.argv[2] 
                    obj.run(option_value)


main = WaskrCommands

def main_():
    main()

