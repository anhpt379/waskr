.. _under_the_hood:

*****************
Under the Hood
*****************
There are a few things to keep in mind when using  **waskr**. These are mainly how this
middleware ties some things behind the scenes.


Code Base and Hosting
========================
**waskr** is hosted at `Google Code <http://code.google.com/p/waskr>`_ 

If you want to check out the code, we use Mercurial, so you would need to run::

    hg clone https://waskr.googlecode.com/hg/ waskr 

If you want to install it, you can use ``pip``::

  pip install waskr

Dependencies
=============
Usually taken care of by ``setup.py`` but is good to know that you need to have the following
up and running:

*  MongoDB

Configuration
-----------------
Waskr needs a couple of configuration options passed as a dictionary. This allows you to get the configuration from where you may be storing it and then push it to the middleware when running your app.

All of the following configuration settings are optional

*  server_id - If you have more than one instance you can add a name or a number here (defaults to 1)
*  db_host = The database host (IP or FQDN) defaults to localhost
*  db_port = The port where your DB is running on (defaults to 27017).
*  application = The name of the application you are running (you may have other WSGI apps) it defaults to 'main'.
