from os import path

from bottle import response, request, redirect, route, run, view, send_file, local, TEMPLATE_PATH 
from waskr import log
from waskr.config import options, setlogging
from waskr.database import Stats

# Fixes a call from a different path
CWD = path.abspath(__file__)
APP_CWD = path.dirname(CWD)
view_dir = APP_CWD+'/views'
TEMPLATE_PATH.append(view_dir)

# Initialize the CONF with proper values
CONF = options()

# Initialize logging
setlogging(CONF)
log.server.debug("initialized logging")


@route('/')
@view('index')
def index():
    logged_in()
    return dict(last_received=local.db.last_insert(),
                apps=local.db.apps_nodes())


@route('/application/:name')
@route('/application/:name/:minutes')
@view('stats')
def interacting(name, minutes=120):
    logged_in()
    return dict(
            app_name=name,
            time_response=local.db.response_time(minutes),
            requests_second=local.db.request_time(minutes))


@route('/login', method=['GET', 'POST'])
@view('login')
def login():
    if request.method == "POST":
        password = request.forms.get('password')
        authorized_password = CONF['web_password']
        if authorized_password and authorized_password == password:
            try:
                set_cookie(password)
                return dict()
            finally:
                redirect('/')
        else:
            redirect('/login')
    else:
      return dict()


@route('/static/:filename')
def static(filename):
    send_file(filename, root=APP_CWD+'/static')


@route('/favicon.ico')
def favicon():
    send_file('favicon.ico', root='static')


@route('/flot/:filename')
def flot(filename):
    send_file(filename, root=APP_CWD+'/static/flot/')


def logged_in():
    cookie = request.COOKIES.get('logged_in')
    if cookie == 'True':
        pass
    else:
        redirect("/login")


def set_cookie(password):
    response.set_cookie('logged_in', 'True', expires=+99500)


def main(config=CONF):
    try:
        # Initialize the DB
        local.db = Stats(config)

        # Start the waskr server
        run(host=config['web_host'], port=config['web_port'])
    except Exception, e:
        print "Couldn't start the waskr server:\n%s" % e


if __name__ == '__main__':
    main()

