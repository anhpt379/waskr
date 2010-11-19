from logging import getLogger

## Set logger objects for all modules
middleware  = getLogger('waskr.middleware')
util        = getLogger('waskr.util')
database    = getLogger('waskr.database')
server      = getLogger('waskr.web.server')
model       = getLogger('waskr.web.model')

