import log
from ConfigParser import ConfigParser
from os.path import isfile
from logging import basicConfig, INFO, DEBUG


def options(config=None, framework_config=None):
    """Instead of calling ConfigParser all over the place
    we gather, read, parse and return valid configuration
    values for any waskr log.utility here, config should
    always be a file object or None and config_options
    always returns a dictionary with values"""
    
    # If all fails we will always have default values
    configuration = defaults()
    converted_opts = {}

    # Options comming from the config file have
    # longer names, hence the need to map them correctly
    opt_mapper = {
            'waskr.db.engine':'db_engine',
			'waskr.db.location':'db_location',
            'waskr.db.host':'db_host',
            'waskr.db.port':'db_port',
            'waskr.web.host':'web_host',
            'waskr.web.port':'web_port',
            'waskr.web.user':'web_user',
            'waskr.middleware.application':'application',
            'waskr.middleware.server_id':'server_id',
            'waskr.cache':'cache',
            'waskr.plugins':'plugins',
            'waskr.plugin.path':'plugin_path',
            'waskr.log.level':'log_level',
            'waskr.log.format':'log_format',
            'waskr.log.datefmt':'log_datefmt'
            }

    # framework_config takes precedence before anything else
    # since it is a ready-to-go config dictionary 
    if framework_config:
        for key, value in opt_mapper.items():
            try:
                file_value = framework_config[key]
                converted_opts[value] = file_value
            except KeyError:
                pass 
        try:
            configuration = defaults(converted_opts)
        except Exception, e:
            log.util.error(e)

        log.util.debug("valid full configuration returned")
        return configuration

    try:
        if config == None or isfile(config) == False:
            configuration = defaults()
            return configuration

    except TypeError:
        if type(config) is dict:
            configuration = defaults(config)
    
    else:
        try:
            parser = ConfigParser()
            parser.read(config)
            file_options = parser.defaults()
        
            # Add support for custom configuration
            for key, value in file_options.items():
                if 'waskr.custom' in key:
                    try:
                        underscored = '_'.join(key.split('.')[2:])
                        if underscored:
                            opt_mapper[key] = underscored
                    except IndexError:
                        pass # badly configured 
            # we are not sure about the section so we 
            # read the whole thing and loop through the items
            for key, value in opt_mapper.items():
                try:
                    file_value = file_options[key]
                    converted_opts[value] = file_value
                except KeyError:
                    pass # we will fill any empty values later with config_defaults
            try:
                configuration = defaults(converted_opts)
            except Exception, e:
                log.util.error(e)

        except Exception, e:
            pass
            log.util.error("couldn't map configuration: %s" % e)

    log.util.debug("valid full configuration returned")
    return configuration

def defaults(config=None):
    """From the config dictionary it checks missing values and
    adds the defaul ones for them if any"""
    if config == None:
        config = {}
    defaults = {
            'server_id': '1',
            'db_engine': 'mongodb',
            'db_host': 'localhost',
            'db_port': 27017,
            'application': 'main',
            'web_host': 'localhost',
            'web_port': '8081',
            'web_user': 'foo@bar.com',
            'cache': '10',
            'plugins': None,
            'plugin_path': False,
            'log_level': 'DEBUG',
            'log_format': '%(asctime)s %(levelname)s %(name)s  %(message)s',
            'log_datefmt' : '%H:%M:%S'
            }

    for key in defaults:
        try:
            config[key]
        except KeyError:
            config[key] = defaults[key]
    log.util.debug("returning basic configuration defaults")
    return config

def setlogging(config=None):
    if config == None:
        config = defaults()
    levels = {
            'debug': DEBUG,
           'info': INFO
            }
    
    level = levels.get(config['log_level'].lower())
    log_format = config['log_format']
    datefmt = config['log_datefmt']

    basicConfig(
            level   = level,
            format  = log_format,
           datefmt = datefmt)



