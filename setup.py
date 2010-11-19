import distribute_setup
distribute_setup.use_setuptools()
from setuptools import setup

tests_require = ['nose', 'webtest']

setup(
    name = "waskr",
    version = "0.0.10",
    packages = ['waskr','waskr.engines','waskr.web'],
    install_requires = ['bottle>=0.8', 'pymongo'],
    entry_points = {
        'console_scripts': [
            'waskr = waskr:main_'
            ]
        },
    include_package_data=True,
    package_data = {
        '': ['distribute_setup.py'],
        },

    # metadata 
    author = "Alfredo Deza",
    author_email = "alfredodeza [at] gmail [dot] com",
    description = "Stats Middleware for WSGI applications.",
    long_description = """\
 Provides statistics for any WSGI application:

  * Requests Per Second
  * Time to respond

 Data can be accessed via a web interface and/or writing your own
 plugins.
 The plugins API is simple yet flexible enough to allow you to 
 get the specific stats you may need.

 Configuration is not needed and waskr provides a simple way 
 of configuring the middleware. 
 You can pass a dictionary with some values a path to an INI file 
 or work with paster/pylons/turbogears configuration objects.

 Full documentation can be found at http://code.google.com/p/waskr
 """,

   classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
      ],

    license = "MIT",
    keywords = "WSGI stats statistics request measure performance",
    url = "http://code.google.com/p/waskr",   

)

