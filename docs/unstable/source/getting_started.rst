.. _getting_started:

*****************
Getting Started
*****************
There are a few things to keep in mind when wanting to get started with **waskr**. 

.. note:: 
    This portion of the documentation assumes you already have **waskr** installed.

Databases
------------
**waskr** is fully database-driven. For now, it will only work with MongoDB. So make sure you have an instance of MongoDB running in your environment before going forward in this guide.

If there is enough demand, we will accomodate other databases.


No Configuration
-----------------
Let's start with an instance of **waskr** that has not been configured. Since this middleware 
does not need to be fully configured to be working properly!

What a normal, no-middleware application might look like::

    def application(environ, start_response):
        start_response('200 OK', [('content-type', 'text/plain')])
        return ('Hello world!',)

    app = wsgi_server(application)


Now let's add **waskr** as a middleware::

    from waskr.middleware import RequestStatsMiddleware

    app = RequestStatsMiddleware(application)
    wsgi_server(app)

Zero configuration can be fun...

.. _adding-configuration:

Adding Configuration
---------------------
If you are already using configuration files for your application, especially in full WSGI
frameworks like Turbogears or Pylons, then you can add waskr-specfic lines to them and pass the 
configuration to the middleware.

Waskr does not need any configuration to run, as long as your environment is matching some defaults.

For example, if you are running MongoDB in localhost with the standard port.

Below is reduced example of the options you may want to use. For a deeper exaplanation of how you can
use and tweak the configuration options, please go to :ref:`configuration`

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

    # Database (Mongo)
    waskr.db.host = localhost
    waskr.db.port = 27017

    # Logging
    waskr.log.level = DEBUG
    waskr.log.format = %(asctime)s %(levelname)s %(name)s  %(message)s
    waskr.log.datefmt = %H:%M:%S

    # Cache
    waskr.cache = 10
    
    # Web User 
    waskr.web.password = alfredo@example.com

Also note that if no options are passed, defaults are used.
This also means that you may have only a few options set, and some other left as defaults.

You choose!

You can also pass the configuration settings as a dictionary. However, special care needs to
be taken since the naming changes a bit.

And default values are shown below. This is the dictionary you could pass 
directly into the Middleware if you chose to::
            
        defaults = {
            'server_id': '1',
            'db_host': 'localhost',
            'db_port': 27017,
            'application': 'main',
            'web_host': 'localhost',
            'web_port': '8080',
            'web_password': False,
            'plugins': None,
            'plugin_path': False,
            'cache': '10',
            'log_level': 'DEBUG',
            'log_format': '%(asctime)s %(levelname)s %(name)s  %(message)s',
            'log_datefmt' : '%H:%M:%S'
            }


Again, if you are looking for more detailed explanation about configuring. Please jump over to
:ref:`configuration`

Passing the Configuration
----------------------------
Now that you have the file, or dictionary with the specific configuration settings you may
want, how do you pass them to the Middleware?

Since **waskr** is allowing either a file, or a dictionary, passing this to the Middleware
is tribial.

For a INI config file::

    app = RequestStatsMiddleware(app, config='/my/path/to/app.ini')


For a dictionary::

    my_config = {'server_id': '3'}
    app = RequestStatsMiddleware(app, config=my_config)

Note how we only passed one of the items in the configuration? Everything else would be the default. Again, you do not need to pass every option!



