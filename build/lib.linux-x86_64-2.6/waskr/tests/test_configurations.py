import unittest
from os import remove

from waskr.config  import options 

def setup():
    txt = open('conf.ini', 'w')
    text = """
[DEFAULT]
# Middleware Configuration
waskr.middleware.server_id = 2
waskr.middleware.application = secondary

# Database Engine
waskr.db.engine = sqlite

# Use only for Sqlite3
waskr.db.location = /tmp

# Database (Mongo)
waskr.db.host = remote.example.com
waskr.db.port = 00000

# Web Interface
waskr.web.host = web.example.com
waskr.web.port = 80

# Logging
waskr.log.level = DEBUG
waskr.log.datefmt = %H:%M:%S
waskr.log.format = %(asctime)s %(levelname)s %(name)s  %(message)s

# Cache
waskr.cache = 10
    """
    txt.write(text)
    txt.close()

    txt = open('conf_two.ini', 'w')
    text = """
[DEFAULT]
# Middleware Configuration
waskr.middleware.application = secondary

# Database (Mongo)
waskr.db.host = remote.example.com
waskr.db.port = 00000

# Web Interface
waskr.web.host = web.example.com
waskr.web.port = 80

# Logging
waskr.log.level = DEBUG
waskr.log.datefmt = %H:%M:%S
waskr.log.format = %(asctime)s %(levelname)s %(name)s  %(message)s    

# Cache
waskr.cache = 10
"""
    txt.write(text)
    txt.close()

    txt = open('conf_three.ini', 'w')
    text = """
[DEFAULT]
# Middleware Configuration
waskr.middleware.server_id = 2
waskr.middleware.application = secondary

# Database (Mongo)
waskr.db.port = 00000

# Web Interface
waskr.web.host = web.example.com
waskr.web.port = 80

# Logging
waskr.log.level = DEBUG
waskr.log.datefmt = %H:%M:%S
waskr.log.format = %(asctime)s %(levelname)s %(name)s  %(message)s    

# Cache
waskr.cache = 10
"""
    txt.write(text)
    txt.close()

    txt = open('conf_four.ini', 'w')
    text = """
[DEFAULT]
# Middleware Configuration
waskr.middleware.server_id = 2
waskr.middleware.application = secondary

# Database (Mongo)
waskr.db.host = remote.example.com

# Web Interface
waskr.web.host = web.example.com
waskr.web.port = 80

# Logging
waskr.log.level = DEBUG
waskr.log.datefmt = %H:%M:%S
waskr.log.format = %(asctime)s %(levelname)s %(name)s  %(message)s    

# Cache
waskr.cache = 10
"""
    txt.write(text)
    txt.close()

    txt = open('conf_five.ini', 'w')
    text = """
[DEFAULT]
# Middleware Configuration
waskr.middleware.server_id = 2

# Database (Mongo)
waskr.db.host = remote.example.com
waskr.db.port = 00000

# Web Interface
waskr.web.host = web.example.com
waskr.web.port = 80

# Logging
waskr.log.level = DEBUG
waskr.log.datefmt = %H:%M:%S
waskr.log.format = %(asctime)s %(levelname)s %(name)s  %(message)s    

# Cache
waskr.cache = 10
"""
    txt.write(text)
    txt.close()

    txt = open('conf_six.ini', 'w')
    text = """
[DEFAULT]
# Middleware Configuration
waskr.middleware.server_id = 2
waskr.middleware.application = secondary

# Database (Mongo)
waskr.db.host = remote.example.com
waskr.db.port = 00000

# Web Interface
waskr.web.port = 80

# Logging
waskr.log.level = DEBUG
waskr.log.datefmt = %H:%M:%S
waskr.log.format = %(asctime)s %(levelname)s %(name)s  %(message)s    

# Cache
waskr.cache = 10
"""
    txt.write(text)
    txt.close()

    txt = open('conf_seven.ini', 'w')
    text = """
[DEFAULT]
# Middleware Configuration
waskr.middleware.server_id = 2
waskr.middleware.application = secondary

# Database (Mongo)
waskr.db.host = remote.example.com
waskr.db.port = 00000

# Web Interface
waskr.web.host = web.example.com

# Logging
waskr.log.level = DEBUG
waskr.log.datefmt = %H:%M:%S
waskr.log.format = %(asctime)s %(levelname)s %(name)s  %(message)s    

# Cache
waskr.cache = 10
"""
    txt.write(text)
    txt.close()

    txt = open('conf_eight.ini', 'w')
    text = """
[DEFAULT]
# Middleware Configuration
waskr.middleware.server_id = 2
waskr.middleware.application = secondary

# Database (Mongo)
waskr.db.host = remote.example.com
waskr.db.port = 00000

# Web Interface
waskr.web.host = web.example.com

# Logging
waskr.log.level = DEBUG
waskr.log.datefmt = %H:%M:%S
waskr.log.format = %(asctime)s %(levelname)s %(name)s  %(message)s    

# Cache
waskr.cache = 10

# Custom
waskr.custom.foo = True
"""
    txt.write(text)
    txt.close()

    txt = open('conf_nine.ini', 'w')
    text = """
[DEFAULT]
# Middleware Configuration
waskr.middleware.server_id = 2
waskr.middleware.application = secondary

# Database (Mongo)
waskr.db.host = remote.example.com
waskr.db.port = 00000

# Web Interface
waskr.web.host = web.example.com

# Logging
waskr.log.level = DEBUG
waskr.log.datefmt = %H:%M:%S
waskr.log.format = %(asctime)s %(levelname)s %(name)s  %(message)s    

# Cache
waskr.cache = 10

# Custom
waskr.custom-foo = True
"""
    txt.write(text)
    txt.close()


def teardown():
    remove('conf.ini') 
    remove('conf_two.ini') 
    remove('conf_three.ini') 
    remove('conf_four.ini') 
    remove('conf_five.ini') 
    remove('conf_six.ini') 
    remove('conf_seven.ini') 
    remove('conf_eight.ini') 
    remove('conf_nine.ini') 


class TestConfigOptions(unittest.TestCase):

    def setUp(self):
        self.opt_mapper = {
            'waskr.db.engine':'db_engine',
            'waskr.db.location':'db_location',
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

        self.defaults = {
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

        self.pylons_config = {
            'waskr.middleware.server_id' : 2,
            'waskr.middleware.application' : 'secondary',
            'waskr.db.host' : 'remote.example.com',
            'waskr.db.port' : 4444,
            'waskr.web.host' : 'web.example.com',
            'waskr.cache' : 20
            }

        setup()

    def tearDown(self):
        teardown()

    def test_framework_config(self):
        actual = options(framework_config=self.pylons_config)
        expected ={
            'server_id': 2,
            'db_engine':'sqlite',
            'db_location':'/tmp',
            'db_host': 'remote.example.com',
            'db_port': 4444,
            'application': 'secondary',
            'web_host': 'web.example.com',
            'web_port': '8080',
            'web_user': False,
            'plugins': None,
            'plugin_path': False,
            'cache': 20,
            'log_level': 'DEBUG',
            'log_format': '%(asctime)s %(levelname)s %(name)s  %(message)s',
            'log_datefmt' : '%H:%M:%S'
            } 
        self.assertEqual(actual, expected) 

    def test_options_TypeError(self):
        actual = options(config={})
        expected = self.defaults
        self.assertEqual(actual, expected)

    def test_options_empty(self):
        actual = options()
        expected = self.defaults
        self.assertEqual(actual, expected)

    def test_options_invalid_file(self):
        actual = options('/path/to/invalid/file.txt')
        expected = self.defaults
        self.assertEqual(actual, expected)

    def test_options_typeError(self):
        actual = options(['a list should never be passed'])
        expected = self.defaults
        self.assertEqual(actual, expected)

    def test_options_Error_string(self):
        actual = options('a string should never be passed')
        expected = self.defaults
        self.assertEqual(actual, expected)

    def test_options_ini(self):
        actual = options('./conf.ini')
        expected = { 
                'web_user': False,
                'plugins': None,
                'plugin_path': False,
                'server_id': '2',
                'db_engine':'sqlite',
                'db_location':'/tmp',
                'db_host': 'remote.example.com',
                'db_port': '00000',
                'application': 'secondary',
                'web_host': 'web.example.com',
                'web_port': '80',
                'cache': '10',
                'log_level': 'DEBUG',
                'log_format': '%(asctime)s %(levelname)s %(name)s  %(message)s',
                'log_datefmt' : '%H:%M:%S'
                } 
        self.assertEqual(actual, expected)

    def test_options_ini_no_id(self):
        actual = options('conf_two.ini')
        expected = {
                'db_engine':'sqlite',
                'db_location':'/tmp',
                'web_user': False,
                'plugins': None,
                'plugin_path': False,
                'server_id': '1',
                'db_host': 'remote.example.com',
                'db_port': '00000',
                'application': 'secondary',
                'web_host': 'web.example.com',
                'cache': '10',
                'web_port': '80',
                'log_level': 'DEBUG',
                'log_format': '%(asctime)s %(levelname)s %(name)s  %(message)s',
                'log_datefmt' : '%H:%M:%S'
                }    
        self.assertEqual(actual, expected)

    def test_options_ini_no_dbhost(self):
        actual = options('conf_three.ini')
        expected = { 
                'db_engine':'sqlite',
                'db_location':'/tmp',
                'web_user': False,
                'plugins': None,
                'plugin_path': False,
                'server_id': '2',
                'db_host': 'localhost',
                'db_port': '00000',
                'application': 'secondary',
                'web_host': 'web.example.com',
                'cache': '10',
                'web_port': '80',
                'log_level': 'DEBUG',
                'log_format': '%(asctime)s %(levelname)s %(name)s  %(message)s',
                'log_datefmt' : '%H:%M:%S'
                }    
        self.assertEqual(actual, expected)

    def test_options_ini_no_dbport(self):
        actual = options('conf_four.ini')
        expected = {
                'db_engine':'sqlite',
                'db_location':'/tmp',
                'web_user': False,
                'plugins': None,
                'plugin_path': False,
                'server_id': '2',
                'db_host': 'remote.example.com',
                'db_port': 27017,
                'application': 'secondary',
                'web_host': 'web.example.com',
                'cache': '10',
                'web_port': '80',
                'log_level': 'DEBUG',
                'log_format': '%(asctime)s %(levelname)s %(name)s  %(message)s',
                'log_datefmt' : '%H:%M:%S'
                }    
        self.assertEqual(actual, expected)

    def test_options_ini_noapp(self):
        actual = options('conf_five.ini')
        expected = {
                'db_engine':'sqlite',
                'db_location':'/tmp',
                'web_user': False,
                'plugins': None,
                'plugin_path': False,
                'server_id': '2',
                'db_host': 'remote.example.com',
                'db_port': '00000',
                'application': 'main',
                'web_host': 'web.example.com',
                'cache': '10',
                'web_port': '80',
                'log_level': 'DEBUG',
                'log_format': '%(asctime)s %(levelname)s %(name)s  %(message)s',
                'log_datefmt' : '%H:%M:%S'
                }    
        self.assertEqual(actual, expected)

    def test_options_ini_no_webhost(self):
        actual = options('conf_six.ini')
        expected = { 
                'db_engine':'sqlite',
                'db_location':'/tmp',
                'web_user': False,
                'plugins': None,
                'plugin_path': False,
                'server_id': '2',
                'db_host': 'remote.example.com',
                'db_port': '00000',
                'application': 'secondary',
                'web_host': 'localhost',
                'cache': '10',
                'web_port': '80',
                'log_level': 'DEBUG',
                'log_format': '%(asctime)s %(levelname)s %(name)s  %(message)s',
                'log_datefmt' : '%H:%M:%S'
                }    
        self.assertEqual(actual, expected)

    def test_options_ini_no_webport(self):
        actual = options('conf_seven.ini')
        expected = {
                'db_engine':'sqlite',
                'db_location':'/tmp',
                'web_user': False,
                'plugins': None,
                'plugin_path': False,
                'server_id': '2',
                'db_host': 'remote.example.com',
                'db_port': '00000',
                'application': 'secondary',
                'web_host': 'web.example.com',
                'cache': '10',
                'web_port': '8080',
                'log_level': 'DEBUG',
                'log_format': '%(asctime)s %(levelname)s %(name)s  %(message)s',
                'log_datefmt' : '%H:%M:%S'
                }    
        self.assertEqual(actual, expected)

    def test_custom_plugin(self):
        actual = options('conf_eight.ini')
        expected = { 
                'db_engine':'sqlite',
                'db_location':'/tmp',
                'foo' : 'True',
                'web_user': False,
                'plugins': None,
                'plugin_path': False,
                'server_id': '2',
                'db_host': 'remote.example.com',
                'db_port': '00000',
                'application': 'secondary',
                'web_host': 'web.example.com',
                'cache': '10',
                'web_port': '8080',
                'log_level': 'DEBUG',
                'log_format': '%(asctime)s %(levelname)s %(name)s  %(message)s',
                'log_datefmt' : '%H:%M:%S'
                }    
        self.assertEqual(actual, expected)

    def test_custom_plugin_none(self):
        """When bad configured it will not display or get parsed"""
        actual = options('conf_nine.ini')
        expected = {
                'db_engine':'sqlite',
                'db_location':'/tmp',
                'web_user': False,
                'plugins': None,
                'plugin_path': False,
                'server_id': '2',
                'db_host': 'remote.example.com',
                'db_port': '00000',
                'application': 'secondary',
                'web_host': 'web.example.com',
                'cache': '10',
                'web_port': '8080',
                'log_level': 'DEBUG',
                'log_format': '%(asctime)s %(levelname)s %(name)s  %(message)s',
                'log_datefmt' : '%H:%M:%S'
                }    
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
