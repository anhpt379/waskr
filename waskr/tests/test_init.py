
import sys
import unittest
import waskr
from waskr import database
from mock import MockSys

class TestWarning(unittest.TestCase):

    def test_warning(self):
        actual = waskr.WARNING
        expected = """ 
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
        self.assertEqual(actual, expected) 

class TestWaskrCommands(unittest.TestCase):


    def test_init_(self):
        actual = waskr.WaskrCommands(argv=None, test=False, parse=False, db=False)

        self.assertEqual(actual.test, False)
        self.assertEqual(actual.db, False)

    
    def test_enable_plugins_keyerror(self):
        commands = waskr.WaskrCommands(argv=None, test=False, parse=False, db=False)
        actual = commands.enable_plugins()

        self.assertFalse(actual) 

    
    def test_enable_plugins_attributeerror(self):
        commands = waskr.WaskrCommands(argv=None, test=False, parse=False, db=False)
        commands.config = {'plugin_path':'/tmp', 'plugins':False}
        actual = commands.enable_plugins()

        self.assertFalse(actual)


    def test_enable_plugins_none(self):
        commands = waskr.WaskrCommands(argv=None, test=False, parse=False, db=False)
        commands.config = {'plugin_path':False, 'plugins':''}
        actual = commands.enable_plugins()

        self.assertFalse(actual)


    def test_enable_plugins(self):
        commands = waskr.WaskrCommands(argv=None, test=False, parse=False, db=False)
        commands.config = {'plugin_path':'/tmp', 'plugins':'foo'}
        actual = commands.enable_plugins()

        self.assertFalse(actual)


    def test_msg_stdout(self):
        sys.stderr = MockSys()
        sys.stdout = MockSys()
        commands = waskr.WaskrCommands(argv=None, test=True, parse=False, db=False)
        commands.msg("foo")
        expected = "foo"
        actual = sys.stdout.captured()
        self.assertEqual(actual, expected) 


    def test_msg_stderr(self):
        sys.stderr = MockSys()
        sys.stdout = MockSys()
        commands = waskr.WaskrCommands(argv=None, test=True, parse=False, db=False)
        commands.msg("bar", std="err")
        expected = "bar"
        actual = sys.stderr.captured()
        self.assertEqual(actual, expected) 

    
    def test_check_config_indexerror(self):
        commands = waskr.WaskrCommands(argv=None, test=True, 
                parse=False, db=database.conf_db(db=':memory:'))
        actual = commands.check_config()
        self.assertFalse(actual)
        

    def test_check_config(self):
        sys.stderr = MockSys()
        sys.stdout = MockSys()
        commands = waskr.WaskrCommands(argv=None, test=True, 
                parse=False, db=database.conf_db(db=':memory:'))
        commands.add_config('/tmp/waskr.ini')
        actual = commands.check_config()
    
        self.assertTrue(actual)
        self.assertEqual(type(actual), dict)


    def test_add_config(self):
        sys.stderr = MockSys()
        sys.stdout = MockSys()
        commands = waskr.WaskrCommands(argv=None, test=True, 
                parse=False, db=database.conf_db(db=':memory:'))
        commands.add_config('/tmp/waskr.ini')
        actual = sys.stdout.captured()
        expected = 'Configuration file added: /tmp/waskr.ini'
    
        self.assertEqual(actual, expected) 
        

    def test_config_values_error(self):
        sys.stderr = MockSys()
        commands = waskr.WaskrCommands(argv=None, test=True, 
                parse=False, db=None)
        commands.config_values()
        actual = sys.stderr.captured()
        expected = "Could not complete command: 'NoneType' object has no attribute 'get_config_path'"
        self.assertEqual(actual, expected) 


    def test_config_values(self):
        sys.stdout = MockSys()
        commands = waskr.WaskrCommands(argv=None, test=True, 
                parse=False, db=database.conf_db(db=':memory:'))
        commands.add_config('/tmp/waskr.ini')
        commands.config_values()
        actual = sys.stdout.captured()
        print actual
        expected = u'Configuration file added: /tmp/waskr.ini\nConfiguration file: /tmp/waskr.ini\n\nweb_password       = False\ndb_engine      = sqlite\nlog_level      = DEBUG\nweb_port       = 8080\ncache          = 10  \nserver_id      = 1   \ndb_port        = 27017\napplication    = main\ndb_location    = /tmp\ndb_host        = localhost\nplugins        = None\nlog_datefmt    = %H:%M:%S\nlog_format     = %(asctime)s %(levelname)s %(name)s  %(message)s\nplugin_path    = False\nweb_host       = localhost\n'
        self.assertEqual(actual, expected) 


    def test_clean_plugin_option_single(self):
        commands = waskr.WaskrCommands(argv=None, test=True, 
                parse=False, db=database.conf_db(db=':memory:'))
        actual = commands.clean_plugin_option("foo-bar")
        expected = "foo_bar"
        self.assertEqual(actual, expected) 


    def test_clean_plugin_option_double(self):
        commands = waskr.WaskrCommands(argv=None, test=True, 
                parse=False, db=database.conf_db(db=':memory:'))
        actual = commands.clean_plugin_option("--foo")
        expected = "foo"
        self.assertEqual(actual, expected) 


    def test_clean_plugin_option_double_single(self):
        commands = waskr.WaskrCommands(argv=None, test=True, 
                parse=False, db=database.conf_db(db=':memory:'))
        actual = commands.clean_plugin_option("--foo-bar")
        expected = "foo_bar"
        self.assertEqual(actual, expected) 

    
if __name__ == '__main__':
    unittest.main()

