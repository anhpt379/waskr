from threading import Thread
import Queue

import log
from waskr.database import Stats

class Synchronizer(Thread):
    """Checks the queue every n minutes and pushes
    the data to the database if it finds an item"""

    def __init__(self, queue, config):
        self.config = config
        Thread.__init__(self)
        self.queue = queue
        log.util.debug("thread and queue initialized")

    def run(self):
        log.util.debug("running thread and looking into the queue")
        while True:
            stats = self.queue.get()
            self.push_to_db(stats)
            self.queue.task_done()

    def push_to_db(self, stats):
        try:
            db = Stats(self.config) 
            db.insert(stats)
            log.util.info("stats pushed to database")
        except Exception, error:
            log.util.critical("thread unable to push stats: %s" % error)

class RequestParser(object):
    """Receives a dictionary with the request and arranges
    the data to pass to the Queue instance"""

    def __init__(self, config, test=False):
        self.config = config
        self.queue = Queue.Queue()
        self.cache = []
        if not test:
            self.spawn_sync()

    def construct(self, data):
        self.cache.append(data)
        if len(self.cache) == int(self.config['cache']):
            self.push_to_queue(self.cache)
            self.flush()
            log.util.info("hit cache threshold (%s) - pushing to queue" % self.config['cache'])

    def flush(self):
        """Flushes the cached data after it goes to the 
        Queue"""
        self.cache = []
        log.util.debug("flushed stats cache")

    def push_to_queue(self, stats):
        """Submits a dictionary of stats to the queue"""
        self.queue.put(stats)
        log.util.debug("pushing stats to the queue")

    def spawn_sync(self):
        """Creates a thread that will fetch data from the queue"""
        sync = Synchronizer(self.queue, self.config)
        sync.setDaemon(True)
        sync.start()
        log.util.debug("spawned a thread")


   


