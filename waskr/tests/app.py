from waskr.middleware import RequestStatsMiddleware

def application(environ, start_response):
    start_response('200 OK', [
        ('Content-Type', 'text/html')
    ])
    return ['Hello World']

app = RequestStatsMiddleware(application)
from wsgiref.simple_server import make_server
httpd = make_server('', 1234, app)
