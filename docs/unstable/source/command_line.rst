.. _command-line:

Command Line
=================
A command line tool is provided to *start*, *stop* or provide a configuration file to the web instance.

Here is a list of different flags and options you have when running the command-line_ ::

    [alfredo@mbp ~/] waskrc
    Usage: waskrc [options]

    WASKR Command Line Utility

    Options:
      --version    show program's version number and exit
      -h, --help   show this help message and exit
      --server     Runs the web server.  If no configuration file is passed
                   localhost and port 8080 is used.
      --conf=CONF  Pass a INI configuration file


.. _server:

server
--------
The server flag ``--server`` calls the web instance (provided by the Bottle Framework). You 
do not need to pass any value to this option, defaults will be used in that case::

    [alfredo@mbp ~/]$ waskrc --server
    Bottle server starting up (using WSGIRefServer())...
    Listening on http://localhost:8080/
    Use Ctrl-C to quit.

In case of errors, you should get an output with some explanation like in this case::

    Bottle server starting up (using WSGIRefServer())...
    Listening on http://localhost:8080/
    Use Ctrl-C to quit.

    Couldn't start the waskr server:
    [Errno 48] Address already in use

conf
------
If you have a INI configuration (similar to :ref:`adding-configuration`) you can pass
it with the ``--conf`` flag. In this case we changed the port from ``8080`` to ``8081``::

    [alfredo@mbp ~/]$ waskrc --server --conf app.ini
    Bottle server starting up (using WSGIRefServer())...
    Listening on http://localhost:8081/
    Use Ctrl-C to quit.



