.. _plugins:

:mod:`plugins` -- API
===============================

.. module:: plugins 

Waskr provides a simple yet flexible way to write plugins so you can extract stored
stats and alter them in whatever way you need.

The API offers a few things:

 *  Full Access to waskr's config values (parsed from the config file you provide)
 *  Custom entries for the config file that get parsed and stored (as many as you may need)
 *  Displays your plugin in the help menu (if configured)
 *  Allows to force a parameter on your plugin option (command line)

.. class:: Plugin(name[, action[, description]])

    The main class in the module, has 1 required parameter and 3 optionals:

    :param name: The command line option (e.g. --my-plugin) **required**
    :param action: ``None`` enforces the user to pass an argument, and ``"store_true"`` doesn't.
    :param description: is the help menu that will get displayed along with waskr's options

              
    .. method:: run(values)
    
        The actual method that gets called when your plugin name gets passed
        as an option to waskr.
    
        :param values: Used in case you are passing arguments in the command line. 
            The argument will get pushed to this parameter.


    .. method:: config_values()
        
        Returns a dictionary with the current parsed configuration options including
        custom options set in the config file. 



.. _first-step:

First Step
-------------
Any plugin will need to inherit from our Plugin class. This basically allows waskr to
"know" about your plugin. So the most basic example would look like this::

    from waskr.plugins import Plugin

    class my_class(Plugin):

        def __init__(self): 
            Plugin.__init__(self,
                name = "--my-plugin",
                action = None,
                description = "My own custom plugin woot"
                ) 
 
In the above snippet, you are doing a few things, lets break what is happening there
line by line:

 *  From the ``plugins`` module you are importing ``Plugin``
 *  Your class (whatever the name) inherits ``Plugin`` (if curious, ``Plugin`` inherits from ``object``)
 *  init needs to call ``Plugin.__init__``

This would be the bare minimum for you to get a plugin up and running.

.. _enabling:

Enabling plugin(s)
----------------------
Waskr needs to know about plugins and the plugin location. In your configuration file,
you should add these options.

.. note::
    If either option for the plugin system is not set, plugins will fail to load

*waskr.plugins* Will tell the app what plugin(s) it needs to load. 
*waskr.plugin.path* Is the absolute path to the plugin **directory**

Below are the options in INI style::

    # Plugins
    waskr.plugins = my_plugin 
    waskr.plugin.path = /Users/alfredo/waskr_plugins

You do **not** need that directory to have a ``__init__.py`` file

For the above to actually make your plugin work, you would need to have a file called ``my_plugin.py``
inside the specified directory with the code shown in :ref:`first-step`.

.. _actions:

Actions
------------
To make your plugin do something when it is called via the command line, you need to use the 
``Plugin`` method ``run()``. 

Just in case you fail to use ``run()`` waskr will produce a warning message as output::

    $ waskr --my-plugin foo

    If you see this text, it means you are *not* using
    the "run()" method in your plugin code.
    You should be defining such a method to be executed when 
    your plugin is called.

The most simple way to implement this is to create such a method in your code. 
Using the same plugin example as in :ref:`first-step` you should add this to the 
class::

    def run(self, value):
        print value

Here is another requirement for the plugin: it needs to have a *value* argument.

The reason for this, is that if you decide to take arguments in the command line and
want to use them in your ``run()`` method, then those arguments are passed on to your
plugin via that key.

If you added the above method, you should see something like this when running 
without arguments::

    $ waskr --my-plugin    
    Usage: waskr [options]

    waskr: error: --my-plugin option requires an argument

And something like this when adding an argument to ``--my-plugin``::

    $ waskr --my-plugin foo
    foo

To change the enforcement of arguments, you should change the attribute of 
the ``Plugin`` class (*action*) from ``None`` to ``"store_true"``.
If you are familiar with the *OptParse* module from the standard library in 
Python, this works very similar, and although waskr uses *OptParse* 
we are just registering your options there for the help menu.


.. _configuration-access:

Configuration Access
------------------------
At runtime, waskr parses values and stores them in a dictionary. Behind the scenes
it does some mappings to get default values if some things are not set.

When writing a plugin you may want to access the database but it is always easier
to access what you already have in the config file such as users and passwords and 
paths.

The :class:`Plugin` class has a method  called :meth:`config_values` that will return the dictionary with all the config
values waskr has currently in memory.

To access such a method, you just need to call it within your plugin. So something like this would work::

    conf = self.config_values()
    print conf 
    {'web_user': 'alfredodeza@example.com', 'server_id': '1', 
    'web_port': '8081', 'log_level': 'DEBUG', 
    'cache': '10', 'db_port': '27017', 'application': 'main', 
    'db_host': 'localhost', 'plugins': 'my_plugin', 
    'log_datefmt': '%H:%M:%S', 
    'plugin_path': '/Users/alfredo/waskr_plugins',
    'log_format': '%(asctime)s %(levelname)s %(name)s  %(message)s', 
    'web_host': 'localhost'}

No parameters or extra code needed!

And the above is a very *cheap* call since it is not re-parsing the config, but rather, returning
what is already in memory.


.. _custom-plugin-config:

Custom Plugin Configuration
-------------------------------
This can be achieved with adding lines in the configuration that matches the 
pattern waskr looks at parse time. Those values will get included in the 
dictionary and should be accessible at any point by your plugin.

For a more complete reference on how to implement custom configuration 
key and values please check :ref:`custom-configuration`

If your custom config sections looks like this::

    waskr.custom.foo = 1

Then ``foo`` would be added to the parsed config dictionary with a value of ``1``, such as::

    {'foo':'1'}

.. _advanced-plugin:

Advanced Plugins - Exporting To ServerDensity
================================================
In this section we will show you a couple of things thay you may be interested when
writing a plugin with **waskr**.

`Server Density <http://www.serverdensity.com>`_ is a server monitoring service (paid)
that allows you to have great visualization and alerts together in a great UI. 
Our example below, will include a plugin for Waskr that will be able to push 
your WSGI application's stats to them.

We will not be going through how to get a Server Density plugin up and running here.

If you are not familiar with their system, check their 
`Plugin Documentation <http://www.serverdensity.com/docs/agent/plugins/>`_ for requirements
on how to set this plugin properly.

In case you want to skip the step by step explanation, this is the full, working plugin::

    from waskr.plugins import Plugin
    from waskr.database import Stats

    class Wsgi(Plugin):

        def __init__(self, agentConfig=None, checksLogger=None, rawConfig=None): 
            self.agentConfig = agentConfig
            self.checksLogger = checksLogger
            self.rawConfig = rawConfig
            self.stats = {}
            Plugin.__init__(self,
                name = "--wsgi-stats",
                action = "store_true",
                description = "My own custom plugin woot"
                )   
         
        def get_stats(self):
            db = Stats(self.config_values())
            self.stats['Response Time'] = db.response_bundle(minutes=1)
            self.stats['Requests'] = db.request_bundle(minutes=1)


        def run(self, value=None):
            """When your option is called, this runs"""
            self.get_stats()
            return self.stats



Initial Setup
-----------------
You need a couple of things to import from **waskr**:

 *  **Plugins** That will get your plugin recognized by the middleware.
 *  **Stats** The main class that is able to connect to your stored data.

Since the ServerDensity plugin requirements force you to have a few arguments, 
set them to be (by default) to ``None``::

    agentConfig=None, checksLogger=None, rawConfig=None

The plugin system from ServerDensity will overwrite those default values at runtime.

The Class Name of the plugin has to match the exact name their system gives you. In this case 
it just happens to be ``Wsgi`` which is also the name of the file.

Getting Stats Data
--------------------
In our plugin, we have a ``get_stats()`` method where we call the database and get some 
information back.

The first part, initializes the database connection with the configuration coming from 
**waskr**::

    db = Stats(self.config_values())

``self.config()`` is waskr's own Plugin method that has already parsed the values you need 
to connect.

Now you need to *build* the dictionary necessary to pass on to ServerDensity.

We already have an empty dictionary instance when we initialized our plugin, so we are 
adding some values to it::

    self.stats['Response Time'] = db.response_bundle(minutes=1)
    self.stats['Requests'] = db.request_bundle(minutes=1)

Here we are adding a ``Response Time`` and ``Requests`` keys. These names will be displayed within
ServerDensity when it receives the stats. If you want to change the naming, do that here so 
it displays properly.

Note we are specifying a ``minutes=1``, what this does, is telling the database to return 
the last 60 seconds of stats *bundled* together. This differes in how **waskr** works (we supply
stats for every second) but the ServerDensity plugin system will call this plugin every minute, so 
we need to get everything together and return it to get data that makes sense.

Also note that since we are not giving the response time for *every* single request, we are 
just returning an average of **all** responses in the given time (e.g. 1 minute)

Pushing Data 
---------------
``run()`` method happens to be the method that ServerDensity calls (matches what **waskr** uses but 
it doesn't matter at this point).

You call the ``get_stats`` method we described above that populates the empty dictionary and then you 
return it when ``run()`` gets called.

This is how your data might look once it gets picked up by the ServerDensity agent running on your
machine:

.. image:: _static/serverdensity.png


And note how the keys we supplied in the dictionary will get displayed:

.. image:: _static/serverdensity2.png
