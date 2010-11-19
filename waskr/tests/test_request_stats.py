import unittest
from time import time

from waskr.middleware import RequestStatsMiddleware

class TestRequestStatsMiddleware(unittest.TestCase):

    def test_init(self):
        app = RequestStatsMiddleware(app=None)
        self.assertEqual(app.app, None)
        self.assertEqual(type(app.config), dict)

    def test_call_app_exception(self):
        app = RequestStatsMiddleware(app=None)
        app(environ=None, start_response=None)
        actual = app.parser.cache
        expected = []
        self.assertEqual(actual, expected) 

    def test_call_app(self):
        environ = {'PATH_INFO':'/'}
        app = RequestStatsMiddleware(app=None)
        app(environ=environ, start_response=None)
        actual = app.parser.cache

        self.assertEqual(type(actual), list)
        self.assertEqual(actual[0]['url'], '/')
        self.assertEqual(actual[0]['application'], 'main')
        self.assertEqual(actual[0]['server_id'], '1')
        
    def test_timing(self):
        """Timing substracts zero from current time"""
        application = RequestStatsMiddleware(app=None)
        actual = int(application.timing(zero=0))
        expected = int(time())
        self.assertEqual(actual, expected)

    def test_config(self):
        """Config should be defaults if None is passed"""
        application = RequestStatsMiddleware(app=None)
        actual = application.config 
        expected = {
                'db_engine': 'sqlite',
                'db_location': '/tmp',
                'server_id': '1', 
                'web_port': '8080', 
                'db_port': 27017, 
                'application': 'main', 
                'db_host': 'localhost', 
                'web_host': 'localhost',
                'web_user':False,
                'cache': '10',
                'plugin_path': False,
                'plugins':None,
                'log_level': 'DEBUG',
                'log_format': '%(asctime)s %(levelname)s %(name)s  %(message)s',
                'log_datefmt' : '%H:%M:%S'
                }
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
