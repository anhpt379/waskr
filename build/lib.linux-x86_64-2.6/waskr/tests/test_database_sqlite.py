import unittest
import os
import sqlite3
from os import path
from time import strftime, time, gmtime
from waskr.database  import Stats

TEST_STATS_TABLE = """CREATE TABLE IF NOT EXISTS test_stats(
time            INT, 
response        INT, 
url             TEXT, 
application     TEXT,
server_id       INT 
)"""


config = {
        'db_engine':'sqlite',
        'db_location': '/tmp/waskr_stats.db',
        }



class TestDatabase(unittest.TestCase):

    def __init__(self, *args, **params):
        unittest.TestCase.__init__(self, *args, **params)
        self.db_name = config['db_location']
        self.conn = sqlite3.connect(self.db_name)
        self.c = self.conn.cursor()
       
        print self.db_name

        self.db = Stats(config, test=True)

        self.single_stat = dict(
                time = 9999,
                response = 9999,
                url = '/',
                application = 'foo',
                server_id = 1
                )


    def setUp(self):
        """Creates a new empty database for testing"""
        self.c.execute('DROP TABLE IF EXISTS test_stats')
        self.c.execute(TEST_STATS_TABLE)
        self.conn.commit()
        
    def tearDown(self):
        """Removes the database previously created"""
        self.c.execute('DROP TABLE IF EXISTS test_stats')
        self.conn.commit()
        self.conn.close()
        
    def test_connection(self):
        try:
            Stats(config, test=True)
            db_conn = True
        except:
            db_conn = False
        self.assertTrue(db_conn)

    
    def test_insert_validate_data(self):
        data = {}
        data['time']        = 9999
        data['response']    = 9999
        data['url']         = '/'
        data['server_id']   = 1
        data['application'] = 'foo'
        self.db.insert([data])
        
        time, response, url, application, server_id  = self.c.execute(
        'SELECT time, response, url, application,server_id\
                FROM test_stats').fetchone()
        self.assertEqual(time, data['time'])
        self.assertEqual(response, data['response'])
        self.assertEqual(url, data['url'])
        self.assertEqual(application, data['application'])
        self.assertEqual(server_id, data['server_id'])

    def test_insert_count(self):
        data = {}
        data['time']        = 9999
        data['response']    = 9999
        data['url']         = '/'
        data['server_id']   = 1
        data['application'] = 'foo'
        self.db.insert([data])
        response = self.c.execute('SELECT COUNT(*) FROM test_stats')
        actual = response.fetchone()
        count = 0
        if actual is not None:
            count = actual[0]
        self.assertEqual(count, 1)

    def test_last_insert(self):
        current_time = time()
        struct = gmtime(current_time)
        formatted = strftime('%Y-%m-%d %H:%M:%S', struct)
        stats =  dict(
                time = current_time,
                response = 9999,
                url = '/',
                application = 'foo',
                server_id = 1
                )
        self.db.insert([stats])
        actual = self.db.last_insert()
        self.assertEqual(actual, formatted)

    def test_app_nodes(self):
        self.db.insert([self.single_stat])
        actual = self.db.apps_nodes()
        expected = [(u'foo', 1)]
        self.assertEqual(actual, expected)

    def test_response_time_out_of_range(self):
        """An out of range time should return an empty list """
        self.db.insert([self.single_stat])
        actual = self.db.response_time(1)
        expected = []
        self.assertEqual(actual, expected)

    def test_response_time_in_range(self):
        current_time = int(time())
        stats =  dict(
                time = current_time,
                response = 9999,
                url = '/',
                application = 'foo',
                server_id = 1
                )        
        self.db.insert([stats])
        actual = self.db.response_time(120)
        expected = [[current_time*1000, 9999]]
        self.assertEqual(actual, expected)

    def test_response_time_in_miliseconds(self):
        current_time = int(time())
        stats =  dict(
                time = current_time,
                response = 9999,
                url = '/',
                application = 'foo',
                server_id = 1
                )        
        self.db.insert([stats])
        response = self.db.response_time(120)
        actual = response[0][0]
        expected = current_time*1000
        self.assertEqual(actual, expected)

    def test_request_time(self):
        current_time = int(time())
        stats =  dict(
                time = current_time,
                response = 9999,
                url = '/',
                application = 'foo',
                server_id = 1
                )        
        self.db.insert([stats])
        actual = self.db.request_time(120)
        expected = [[current_time*1000, 1]]
        self.assertEqual(actual, expected)

    def test_request_time_out_of_range(self):
        current_time = int(time()) - 20000
        stats =  dict(
                time = current_time,
                response = 9999,
                url = '/',
                application = 'foo',
                server_id = 1
                )        
        self.db.insert([stats])
        actual = self.db.response_time(120)
        expected = []
        self.assertEqual(actual, expected)
   

 
if __name__ == '__main__':
    unittest.main()
