import sys  
import os

import yaml

from PyQt4 import QtCore, QtGui, QtWebKit 

from trapdoor.extension import Extension
from trapdoor.plugin import PlugIn
from trapdoor.utils import importlib


class TrapdoorCore(object):

    def main(self, argv):
        self.appname = argv[1]
        self.manifest = yaml.load(open(os.path.join(self.appname, 'manifest.yaml')))

        app = QtGui.QApplication(sys.argv)
        self.nodes = [Node()]
        node = self.prime_node

        self.plugins = {}
        self.extensions = {}

        for name in self.manifest.get('plugins', ()):
            self.plugins[name] = plugin = PlugIn(name)
            self.extensions.update( plugin.load_extensions() )

        self.extensions.update( self.load_extensions() )
        node.add_extensions(self.extensions)

        node.add_default_scripts()
        for js in self.manifest['js']:
            node.add_script(os.path.join(self.appname, js))

        sys.exit(app.exec_())

    def load_extensions(self):
        extensions = {}

        for ext in self.manifest['extensions']:
            ext_globals = self.load_library(self.appname, ext)
            extensions[ext] = ext_globals
        return extensions

    def load_library(self, app, extlibrary):
        library_globals = {}
        execfile(os.path.join(app, extlibrary + '.py'), library_globals)
        return library_globals
        

    prime_node = property(lambda self: self.nodes[0])

class Node(object):

    def __init__(self):
        self.webview = QtWebKit.QWebView()
        self.frame = self.webview.page().mainFrame()


        init_html_path = os.path.join(os.path.dirname(__file__), 'templates', 'init.html')
        self.load_file(init_html_path)

    def load_file(self, path):
        self.webview.setHtml(open(path).read())

    def add_extension(self, extname, extension):
        self.frame.addToJavaScriptWindowObject(extname, extension)
        self.frame.evaluateJavaScript(extension.generateJSWrapper(extname))

    def add_extensions(self, extensions):
        for modname, mod in extensions.items():
            for extname in mod:
                if isinstance(mod[extname], type) and issubclass(mod[extname], Extension) and mod[extname] is not Extension:
                    extension = mod[extname](node=self)
                    self.add_extension(extname, extension)

    def add_script(self, path):
        self.frame.evaluateJavaScript(open(path).read())

    def add_default_scripts(self):
        for js_file in ('jquery_dev.js', 'trapdoor.js'):
            self.add_script(os.path.join(os.path.dirname(__file__), 'js', js_file))
    
    def add_scripts(self, paths):
        for path in paths:
            self.add_script(path)
            
