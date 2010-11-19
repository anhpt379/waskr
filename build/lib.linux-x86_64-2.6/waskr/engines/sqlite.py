# Implementation Engine for Sqlite3

import os
import sqlite3
from os import path
from time import time, strftime, gmtime
from waskr.config import options
from waskr import log

STATS_TABLE = """CREATE TABLE IF NOT EXISTS %s(
    time            INT, 
    response        INT, 
    url             TEXT, 
    application     TEXT,
    server_id       INT 
)"""


class Stats(object):

    def __init__(self, config=None, test=False):
        config = options(config)
        self.db = self._location_verify(config['db_location'])
        self.table = 'stats'
        if test:
            self.table = 'test_stats'    
       
        self.conn = sqlite3.connect(self.db)
        self.c = self.conn.cursor()
        self.c.execute(STATS_TABLE % self.table)
        self.conn.commit()
        
        log.database.debug("database connection initialized Sqlite3")

                
    def __del__(self):
        """Make sure the db is closed"""
        self.conn.close()
        

    def _location_verify(self, location):
        """The need to have valid absolute paths"""
        if not path.isdir(location):
            return path.abspath(location)
        if path.isdir(location):
            abspath = path.abspath(location)
            return abspath+'/waskr_stats.db'

    def insert(self, stats):
        # Stats should come as a list of dictionaries
        for stat in stats:
            values = (stat['time'], stat['response'], stat['url'],
                        stat['application'], stat['server_id'])
            command = """INSERT INTO %s (time, 
            response, 
            url, 
            application, 
            server_id) values (?,?,?,?,?)""" % self.table
            self.c.execute(command, values)
        self.conn.commit()
        log.database.debug("inserted stats to database")


    def last_insert(self):
        command = 'SELECT time FROM %s ORDER BY time DESC LIMIT 1' % self.table
        row = self.c.execute(command).fetchone()
        if row:
            unix_time =  row[0]
            struct = gmtime(unix_time)
            formatted = strftime('%Y-%m-%d %H:%M:%S', struct)
            return formatted
        log.model.debug("returned formatted last insert from database sqlite3(%s)" % self.table)

    
    def apps_nodes(self):
        apps = []
        command = 'SELECT DISTINCT application, server_id FROM %s' % self.table
        records = self.c.execute(command).fetchall()
        for (application, server_id) in records:
            match = (application), server_id
            if match not in apps:
                apps.append(match)
        return apps
        log.model.debug("returned all application nodes present")

    
    def response_time(self, minutes):
        """Get the last N minutes of response stats"""
        time_response = []
        mins = int(minutes) * 60
        start = time() - int(mins)
        command = 'SELECT time, response FROM %s WHERE time >= ? AND time <= ?' % self.table
        values = (start, time())
        records = self.c.execute(command, values).fetchall()
        for (stat_time, stat_response) in records:
            data = []
            miliseconds = int(stat_time) * 1000
            data.append(miliseconds)
            data.append(stat_response)
            time_response.append(data)
        log.model.debug("returned the last N minutes of response stats")
        return time_response

    def response_bundle(self, minutes):
        """Get the last N minutes of response stats in a bundle"""
        time_response = []
        total = 0
        mins = int(minutes) * 60
        start = time() - int(mins)
        command = 'SELECT response FROM %s WHERE time >= ? and time <= ?' % self.table
        values = (start, time())
        records = self.c.execute(command, values).fecthall()
        for response in records:
            total = total + response
            time_response.append(response)
        divide_by = len(time_response)
        try:
            average = total /divide_by
        except ZeroDivisionError:
            average = 0
        return average

    def request_bundle(self, minutes):
        """Get the last N minutes of request stats in a bundle"""
        hits = 0
        mins = int(minutes) * 60
        start = time() - int(mins)
        command = 'SELECT COUNT(*) FROM %s  WHERE time >= ? AND time <= ?' % self.table
        values = (start, time())
        row = self.c.execute(command,values).fetchone()
        if row:
            hits = row[0]
        return hits
        log.model.debug("returned requests per second")
 
    def request_time(self, minutes):
        """Get the last N minutes of request stats"""
        requests_second = []
        mins = int(minutes) * 60
        start = time() - int(mins)
        command = 'SELECT time FROM %s WHERE time >= ? AND time <= ?' % self.table
        values = (start, time())
        records = self.c.execute(command, values).fetchall()
        for (stat_time,) in records:
            data = []
            hits = 0
            command = 'SELECT COUNT(*) FROM %s WHERE time = ?' % self.table
            row = self.c.execute(command,(stat_time,)).fetchone()
            if row:
                hits = row[0]
            miliseconds = int(stat_time) * 1000
            data.append(miliseconds)
            data.append(hits)
            requests_second.append(data)
        return requests_second
        log.model.debug("returned requests per second")
    
