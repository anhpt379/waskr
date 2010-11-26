from time import time
from waskr.config import options, setlogging
from util import RequestParser
import log, traceback

class RequestStatsMiddleware(object):

    def __init__(self, app, config=None, framework_config=None):
        """Initialize the RequestStats Middleware
        Every single request will get logged with a unix timestamp
        the time it took to respond and the url that was requested.
        The dictionary is passed on the RequestParser that deals
        with building the cache and submitting the data to 
        the queue.
        """
        self.app = app

        self.config = options(config, framework_config)
        self.parser = RequestParser(self.config)

        setlogging(self.config)
        log.middleware.debug('middleware Initialized')

    def __call__(self, environ, start_response):
        log.middleware.debug('received request call')
        zero = time()
        data = {}
        try:
            return self.app(environ, start_response)
        except Exception, error:
            log.middleware.critical("failed to return the response: %s" % error)
        finally:
            try:
                data['time']        = int(time())
                data['response']    = self.timing(zero)
                data['url']         = environ['PATH_INFO']
                if environ['QUERY_STRING']:
                  data['url'] += '?' + environ['QUERY_STRING']
                if environ.get("HTTP_X_REAL_IP"):
                  data['remote_addr'] = environ["HTTP_X_REAL_IP"]
                else: 
                  data['remote_addr'] = environ['REMOTE_ADDR']
                data['server_id']   = self.config['server_id']
                data['application'] = self.config['application']
                self.parser.construct(data)             
            except Exception, error:
                log.middleware.critical("failed to push request stats: %s" % error)
                traceback.print_exc(file=open("err_log.txt", "a"))
                
    def timing(self, zero):
        log.middleware.debug('returning time object')
        return time() - zero

