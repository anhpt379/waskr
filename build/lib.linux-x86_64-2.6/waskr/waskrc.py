#!/usr/bin/env python

""" WASKR Command Line Utility """

__version__ = '0.0.2'

from optparse import OptionParser
from os import path
import sys

from waskr import database, config_options
from waskr.web import server

def main():
    """Handle all options"""
    parser = OptionParser(description="""WASKR Command Line Utility""", 
            version=__version__)
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
            configuration = config_options(options.conf)
            server.CONF = configuration
            server.main(configuration)
        else:
            server.main()

    if options.add_user and options.conf:
        try:
            config = config_options(options.conf)
            db = database.Stats(config)
            db.add_user(options.add_user)
            print "User %s was added to the DB" % options.add_user
        except Exception, e:
            print 'waskrc could not add user: %s' % e

    if options.remove_user and options.conf:
        try:
            config = config_options(options.conf)
            db = database.Stats(config)
            db.remove_user(options.add_user)
            print "User %s removed from DB" % options.remove_user
        except Exception, e:
            print 'waskrc could not remove user: %s' % e


if __name__ == "__main__":
        main() 
