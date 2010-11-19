import os
import sqlite3
from time import time, strftime, gmtime
from waskr.config import options
import log

# Fixes Database Absolute Location
FILE_CWD =  os.path.abspath(__file__)
FILE_DIR = os.path.dirname(FILE_CWD)
DB_FILE = FILE_DIR+'/waskr.db'


# Engines Supported
engines_supported = ['sqlite', 'mongodb']


class conf_db(object):

    def __init__(self,
            db = DB_FILE):
        self.db = db 
        if os.path.isfile(self.db):
            self.conn = sqlite3.connect(self.db)
            self.c = self.conn.cursor()
        else:
            self.conn = sqlite3.connect(self.db)
            table = """CREATE TABLE config(path TEXT)"""
            self.c = self.conn.cursor()
            self.c.execute(table)
            self.conn.commit()


    def closedb(self):
        """Make sure the db is closed"""
        self.conn.close()


    def add_config(self, path):
        """Adds a MASTER config for waskr"""
        values = (path,path)
        delete = 'DELETE FROM config'
        command = 'INSERT INTO config(path) select ? WHERE NOT EXISTS(SELECT 1 FROM config WHERE path=?)' 
        self.c.execute(delete)
        self.c.execute(command, values)
        self.conn.commit()


    def get_config_path(self):
        """Returns the first entry for the config path"""
        command = "SELECT * FROM config limit 1"
        return self.c.execute(command)


class Stats(object):

    def __init__(self,config=None, test=False):
        self.config = options(config)
        self.engine = self._load_engine()
        self.stats = self.engine.Stats(config, test)


    def _load_engine(self):
        if self._check_module(self.config['db_engine']):
            engine = __import__('waskr.engines.%s' % self.config['db_engine'], 
                                                              fromlist=['None'])
        else:
            engine = __import__('waskr.engines.sqlite',
                                    fromlist=['None']) # fall backs to sqlite3
        return engine


    def _check_module(self, module):
        if module not in engines_supported:
            return False
            
        return True

    def insert(self, stats):
        self.stats.insert(stats)
        

    def last_insert(self):
        return self.stats.last_insert()


    def apps_nodes(self):
        return self.stats.apps_nodes()


    def response_time(self, minutes):
        return self.stats.response_time(minutes)


    def response_bundle(self, minutes):
        return self.stats.request_bundle(minutes)


    def request_bundle(self, minutes):
        return self.stats.request_bundle(minutes)

 
    def request_time(self, minutes):
        return self.stats.request_time(minutes)
    

