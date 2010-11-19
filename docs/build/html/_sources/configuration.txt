.. _configuration:

Configuring 
==============
Waskr needs very little configuration to get started. However, it 
offers a lot of flexibility if you need to extend Waskr by adding plugins 
and adding specific plugin options, or if you need to use other components
like the web interface.


.. _from_framework:

Framework Configs
-------------------
Some Frameworks like Pylons and Turbogears, have all the configurations in memory 
so you might want to use that instead of passing static dictionaries or a path.

If the configs are already parsed it might be a good idea to go ahead and use that.

However, since those dictionaries differ a bit, you need to pass that instance with 
a different parameter: ``framework_config`` will need to hold that config object.

A framework config would map ``waskr`` configurations like so::

    {'waskr.middleware.server_id':1, 'waskr.middleware.application': 'main'}

That is the reason we need to deal with it differently.

Passing the config instance is trivial::

    # acquire the config object somehow:
    from framework import config 

    app = RequestStatsMiddleware(app, framework_config=config)

.. note::
    Make sure you are using ``framework_config`` and not other parameters in ``RequestStatsMiddleware``


.. _ini:

INI
------
Waskr uses INI format config files, that for the most part should match those 
same config files of current Full WSGI Frameworks like Pylons or Turbogears.

Below, we show what all the standard options Waskr can take, with its defaults.

INI Style Configuration::

    # This is a sample Configuration File
    # for running any of Waskr's utilities
    # It should be taken as an example if you are running
    # a Pylons or Paster app and want to put some Configuration
    # settings there.
    #
    # You can also pass a dictionary, since all of waskr's utilities
    # look for a dictionary type of configuration to read from.

    [DEFAULT]
    # Middleware Configuration
    waskr.middleware.server_id = 1
    waskr.middleware.application = main

    # Database Engine
    waskr.db.engine = sqlite

    # Use only for Sqlite3
    waskr.db.location = /tmp

    # Database (Mongo)
    waskr.db.host = localhost
    waskr.db.port = 27017

    # Web Interface
    waskr.web.host = localhost
    waskr.web.port = 8080

    # Logging
    waskr.log.level = DEBUG
    waskr.log.format = %(asctime)s %(levelname)s %(name)s  %(message)s
    waskr.log.datefmt = %H:%M:%S

    # Cache
    waskr.cache = 10
    
    # Plugins
    waskr.plugins = None
    waskr.plugin.path = False

    # Web User 
    waskr.web.user = False

The values above, get parsed into a dictionary that eventually gets into the Middleware.


.. _dictionary:

Dictionary
----------------

You can also pass the configuration settings as a dictionary. However, special care needs to
be taken since the naming changes a bit. We actually *translate* the options from the INI file 
to more readable strings.

Values from a config file get translated like this::

   from_config = {
            'waskr.db_engine':'db_engine',
            'waskr.db_location':'db_location',
            'waskr.db.host':'db_host',
            'waskr.db.port':'db_port',
            'waskr.web.host':'web_host',
            'waskr.web.port':'web_port',
            'waskr.middleware.application':'application',
            'waskr.middleware.server_id':'server_id',
            'waskr.log.level':'log_level',
            'waskr.log.format':'log_format',
            'waskr.log.datefmt':'log_datefmt',
            'waskr.cache':'cache',
            'waskr.plugins':'plugins',
            'waskr.plugin.path':'plugin_path',
            'waskr.web.user':'web_user'
            }

And default values are shown below. This is the dictionary you could pass 
directly into the Middleware if you chose to::
            
        defaults = {
            'server_id': '1',
            'db_engine':'sqlite',
            'db_location':'/tmp',
            'db_host': 'localhost',
            'db_port': 27017,
            'application': 'main',
            'web_host': 'localhost',
            'web_port': '8080',
            'web_user': False,
            'plugins': None,
            'plugin_path': False,
            'cache': '10',
            'log_level': 'DEBUG',
            'log_format': '%(asctime)s %(levelname)s %(name)s  %(message)s',
            'log_datefmt' : '%H:%M:%S'
            }


Let's go through each one of the configuration labels:

.. note:: 
    Some options are for the command line tool and are displayed here with (CLI)


**server_id**
If you have a load balanced application, you can identify them with an ID. We suggest you use numbers but anything that is a string is an OK value.

**application**
Sometimes you may have your application sub divided into different apps, you can set them here too. For example, your *server_one* may have 2 WSGI apps: *blog* and *ticketing_system*

**db_engine**
sqlite, mongodb are all valid options.

**db_location**
The location of the database. When use Sqlite3.

**db_host**
The host of the database instance. This can be either the IP or the FQDN

**db_port**
The port the database is using (we default to the standard MongoDB port).

**web_host**
When running the web interface, where would you want this web server to serve at. Again, IP's or FQDN are valid options.

**web_port**
The port were the web interface will be running at.

**web_user**
Specify the email that has access to the web interface of the app

**cache**
Waskr holds some data before writing it to the database to avoiding having the middleware 
cluttering DB writes. By default, waskr will wait until it has 10 hits before pushing 
the data to the DB. Tweak this value to accomodate better your app needs (e.g. a much higher
number if you have poppular application).

**log_level**
DEBUG, INFO, WARNING, ERROR are all valid options.

**log_format**
How the log output will be shown.

**log_datefmt**
You can tweak the way we display the time, specially useful when you need miliseconds for precision.

**plugins (CLI)**
Add a list of plugins (or just one) to enable in the command line tool. 
(Needs to be set with the ``plugin_path`` option)

**plugin_path (CLI)**
Specify an absolute path for your plugins. (Needs to be set with the ``plugins`` option.)


.. _custom-configuration:

Custom Configuration
----------------------
You can also have **as many** custom configuration keys enabled. We achieve this by having 
a schema for parsing.

The schema is as follows::

    waskr.custom.foo = True
    waskr.custom.foo.bar = False 

The above would get translated into::

    foo = True
    foo_bar = False 

As long as you are representing your custom options with a preceding ``waskr.custom``
the app will parse those options and make them python-readable strings.

Note however, that we are not *evaluating* the values of your configuration keys. If you 
are setting some key to be ``True`` like we did for ``waskr.custom.foo`` then it will 
get parsed as a string ``"True"``

Those custom configurations (if they do not raise exceptions) will get added to the 
in-memory dictionary when parsed so they should be widely available.


Passing the Configuration
----------------------------
Now that you have the file, or dictionary with the specific configuration settings you may
want, how do you pass them to the Middleware?

Since **waskr** is allowing either a file, or a dictionary, passing this to the Middleware
is tribial.

For a INI config file::

    app = RequestStatsMiddleware(app, config='/my/path/to/app.ini')


For a dictionary::

    my_config = {'server_id': '3','db_engine':'mongodb'}
    app = RequestStatsMiddleware(app, config=my_config)

For Framework that uses Paster-style configurations check :ref:`from_framework`


