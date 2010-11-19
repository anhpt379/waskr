import sys
import unittest

from waskr.plugins import Plugin  


class MockSys(object):
    """Can grab messages sent to stdout or stderr"""
    def __init__(self):
        self.message = []

    def write(self, string):
        self.message.append(string)
        pass

    def captured(self):
        return ''.join(self.message)

class TestPlugin(unittest.TestCase):

    def test_new_plugin(self):
        plugin = Plugin(name="my_plugin",action="store_true",
                description="my help menu")
        self.assertEqual(plugin.name, "my_plugin")
        self.assertEqual(plugin.action, "store_true")
        self.assertEqual(plugin.description, "my help menu")

    def test_command_dict(self):
        plugin = Plugin(name="my_plugin",action="store_true",
                description="my help menu")
        actual = type(plugin.command())
        expected = dict
        self.assertEqual(actual, expected) 

    def test_command_values(self):
        plugin = Plugin(name="my_plugin",action="store_true",
                description="my help menu")
        actual = plugin.command()
        expected = dict(
            option = "my_plugin",
            action = "store_true",
            description = "my help menu"
            )

        self.assertEqual(actual, expected) 

    def test_run_none(self):
        """Nothing should happen when run is called"""
        sys.stderr = MockSys()
        sys.stdout = MockSys()
        plugin = Plugin(name="my_plugin",action="store_true",
                description="my help menu")
        actual = plugin.run(value=None)
        expected = None
        self.assertEqual(actual, expected)  

    def test_run_message(self):
        """Display a message to stdout when run is not set properly"""
        sys.stderr = MockSys()
        sys.stdout = MockSys()
        plugin = Plugin(name="my_plugin",action="store_true",
                description="my help menu")
        plugin.run(value=None)
        actual = sys.stdout.captured() 
        expected = """
If you see this text, it means you are *not* using
the "run()" method in your plugin code.
You should be defining such a method to be executed when 
your plugin is called.

"""
        self.assertEqual(actual, expected)  


if __name__ == '__main__':
    unittest.main()
