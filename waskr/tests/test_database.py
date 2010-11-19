import unittest
from time import strftime, time, gmtime
from pymongo import Connection
from waskr.database  import Stats

config = {
        'db_engine': 'mongodb',
        'db_host': 'localhost',
        'db_port': 27017,
        }

class TestDatabase(unittest.TestCase):

    def __init__(self, *args, **params):
        unittest.TestCase.__init__(self, *args, **params)
        connection = Connection(
                config['db_host'], 
                config['db_port'])
        self.waskr = connection['test_waskr']
        self.stats = self.waskr['stats']
        self.users = self.waskr['user']

        self.db = Stats(config, test=True)

        self.single_stat = dict(
                time = 9999,
                response = 9999,
                url = '/',
                application = 'foo',
                server_id = '1'
                )

    def setUp(self):
        """Creates a new empty database for testing"""
        connection = Connection(
                config['db_host'], 
                config['db_port'])
        waskr = connection['test_waskr']
        waskr.drop_collection('user')
        waskr.drop_collection('stats')
        stats = waskr['stats']
        users = waskr['user']


    def tearDown(self):
        """Removes the database previously created"""
        connection = Connection(
                config['db_host'], 
                config['db_port'])
        # make sure there is not a previous instance:
        waskr = connection['test_waskr']
        waskr.drop_collection('user')
        waskr.drop_collection('stats')


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
        data['server_id']   = '1'
        data['application'] = 'foo'
        self.db.insert([data])
        item  = [i for i in self.stats.find()]
        actual = item[0]
        self.assertEqual(actual['time'], data['time'])
        self.assertEqual(actual['response'], data['response'])
        self.assertEqual(actual['url'], data['url'])
        self.assertEqual(actual['application'], data['application'])
        self.assertEqual(actual['server_id'], data['server_id'])

    def test_insert_count(self):
        data = {}

        data['time']        = 9999
        data['response']    = 9999
        data['url']         = '/'
        data['server_id']   = '1'
        data['application'] = 'foo'
        self.db.insert([data])
        self.assertEqual(self.stats.count(), 1)

    def test_last_insert(self):
        current_time = time()
        struct = gmtime(current_time)
        formatted = strftime('%Y-%m-%d %H:%M:%S', struct)
        stats =  dict(
                time = current_time,
                response = 9999,
                url = '/',
                application = 'foo',
                server_id = '1'
                )
        self.db.insert([stats])
        actual = self.db.last_insert()
        self.assertEqual(actual, formatted)

    def test_app_nodes(self):
        self.db.insert([self.single_stat])
        actual = self.db.apps_nodes()
        expected = [(u'foo', u'1')]
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
                server_id = '1'
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
                server_id = '1'
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
                server_id = '1'
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
                server_id = '1'
                )        
        self.db.insert([stats])
        actual = self.db.response_time(120)
        expected = []
        self.assertEqual(actual, expected)


 
if __name__ == '__main__':
    unittest.main()
