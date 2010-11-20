# Implementation Engine for MongoDB

from pymongo import Connection, DESCENDING
from time import time, strftime, gmtime
from waskr.config import options
from waskr import log


class Stats(object):

    def __init__(self, config=None, test=False):
        config = options(config)
        try:
            self.connection = Connection(
                    config['db_host'], 
                    int(config['db_port']))
        except Exception, error:
            log.database.critical("Could not connect to MongoDB: %s" % error)
        self.waskr = self.connection['waskr']
        self.stats = self.waskr['stats']
        self.users = self.waskr['user']
        self.cache = self.waskr['cache']
        log.database.debug("database connection initialized")
        if test:
            self.waskr = self.connection['test_waskr']
            self.stats = self.waskr['stats']
            self.users = self.waskr['user']

    def insert(self, stats):
        # Stats should come as a list of dictionaries
        for stat in stats:
            self.stats.insert(stats)
            self.cache.update({"time": stat['time']}, {"$inc": {"count": 1}}, upsert=True)
        log.database.debug("inserted stats to database")

    def last_insert(self):
        last = self.stats.find().sort('time', DESCENDING).limit(1)
        for entry in last:
            unix_time =  entry['time']
            struct = gmtime(unix_time)
            formatted = strftime('%Y-%m-%d %H:%M:%S', struct)
            return formatted
        log.model.debug("returned formatted last insert from database")

    def apps_nodes(self):
        apps = []
        for application in self.stats.distinct('application'):
            c = self.stats.find({'application': application}).sort('time', -1).limit(1000)
            for record in c:
                match = (record['application']), record['server_id']
                if match not in apps:
                    apps.append(match)
        log.model.debug("returned all application nodes present")
        return apps

    def response_time(self, minutes):
        """Get the last N minutes of response stats"""
        time_response = []
        mins = int(minutes) * 60
        start = time() - int(mins)
        records = self.stats.find({"time": {"$gte": start, "$lt": time()}})
        for stat in records:
            data = []
            miliseconds = int(stat['time']) * 1000
            data.append(miliseconds)
            data.append(stat['response'])
            time_response.append(data)
        log.model.debug("returned the last N minutes of response stats")
        return time_response

    def response_bundle(self, minutes):
        """Get the last N minutes of response stats in a bundle"""
        time_response = []
        total = 0
        mins = int(minutes) * 60
        start = time() - int(mins)
        records = self.stats.find({"time": {"$gte": start, "$lt": time()}})
        for stat in records:
            total = total + stat['response']
            time_response.append(stat['response'])
        divide_by = len(time_response)
        try:
            average = total /divide_by
        except ZeroDivisionError:
            average = 0
        return average

    def request_bundle(self, minutes):
        """Get the last N minutes of request stats in a bundle"""
        mins = int(minutes) * 60
        start = time() - int(mins)
        hits = self.stats.find({"time": {"$gte": start, "$lt": time()}}).count()
        log.model.debug("returned requests per second")
        return hits
 
    def request_time(self, minutes):
        """Get the last N minutes of request stats"""
        log.model.debug("quering request time...")
        requests_second = []
        mins = int(minutes) * 60
        start = time() - int(mins)
        records = self.cache.find({"time": {"$gte": start, "$lt": time()}})
        log.model.debug("records: %s" % records.count())
        log.model.debug("query finished. processing...")
        for stat in records:
            data = []
            log.model.debug("refreshing...")
            hits = self.cache.find_one({'time':stat['time']}).get('count')
            log.model.debug("hits: %s" % hits)
            miliseconds = int(stat['time']) * 1000
            data.append(miliseconds)
            data.append(hits)
            requests_second.append(data)        
        log.model.debug("returned requests per second")
        return requests_second