.. _changelog:

ChangeLog
===========
A list with all the changes for each version of Waskr should be listed here.


Version 0.9
------------

 *  A web user will now come from the config file. 
 *  Will no longer support adding/removing users
 *  Removed first_run() that would check if a user was in the DB
 *  Added Plugin Support with a plugin API
 *  The config file could show plugins to enable and plugin path
 *  Added tests for the new plugin system   
 *  A user can add custom config options via waskr.custom in INI files 
 *  Plugins can use the current config values within a class

Version 0.8
------------

 *  Added a cache size that will indicate what is the treshold of requests
    before Waskr pushes the stats to the DB.
