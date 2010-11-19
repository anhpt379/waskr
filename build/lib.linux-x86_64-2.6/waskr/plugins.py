import sys

class Plugin(object):

    def __init__(self, 
            name,
            action='store_true',
            description="",
            config={}):
        self.name = name
        self.action = action 
        self.description = description
        self.config = config

    def command(self):
        return dict(
            option = self.name,
            action = self.action,
            description = self.description
            )

    def run(self, value):
        """A safe way to prevent tracebacks in the CLI
        output if a dev forgets to use "run" as a method
        in their plugin"""
        print """
If you see this text, it means you are *not* using
the "run()" method in your plugin code.
You should be defining such a method to be executed when 
your plugin is called.
"""
       
    def config_values(self):
        """Provides access to the already existing configuration
        stored in waskr. Returns a dictionary of values"""
        return self.config


def load_plugins(plugins):
    for plugin in plugins:
        try:
            __import__(plugin, None, None, [''])
        except ImportError:
            pass # probably a poorly configured plugin

def init_plugin_system(cfg):
    if not cfg['plugin_path'] in sys.path:
        sys.path.insert(0, cfg['plugin_path'])
    load_plugins(cfg['plugins'])
    

def find_plugins():
    return Plugin.__subclasses__()

