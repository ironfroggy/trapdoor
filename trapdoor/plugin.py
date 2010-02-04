import os
import yaml

from trapdoor.utils import importlib

class PlugIn(object):

    def __init__(self, plugin_name):
        self.plugin_name = plugin_name

        plugin_module = importlib.import_module(plugin_name)
        plugin_path = self.path = os.path.dirname(plugin_module.__file__)
        self.manifest = yaml.load(open(os.path.join(plugin_path, 'manifest.yaml')))

        self.module = plugin_module

    def load_extensions(self):
        extensions = {}

        for extpath in self.manifest.get('extensions', ()):
            library, extname = extpath.rsplit('.', 1)
            mod = importlib.import_module('.'.join((self.plugin_name, library)))
            extensions[extpath] = getattr(mod, extname)
        return extensions

    def load_library(self, app, extlibrary):
        library_globals = {}
        execfile(os.path.join(app, extlibrary + '.py'), library_globals)
        return library_globals
