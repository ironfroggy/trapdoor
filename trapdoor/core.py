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

        app = QtGui.QApplication(sys.argv)
        self.nodes = [Node()]
        node = self.prime_node

        self.plugins = {}
        self.extensions = {}
        self.main_plugin = PlugIn(self.appname)
        self.plugins[self.appname] = self.main_plugin

        for name in self.main_plugin.manifest.get('plugins', ()):
            self.plugins[name] = plugin = PlugIn(name)
            self.extensions.update( plugin.load_extensions() )

        self.extensions.update( self.main_plugin.load_extensions() )
        node.add_extensions(self.extensions)

        node.add_default_scripts()
        for plugin in self.plugins.values():
            node.add_scripts_from_plugin(plugin)

        sys.exit(app.exec_())

    prime_node = property(lambda self: self.nodes[0])

class Node(Extension):

    def __init__(self, **kwargs):
        super(Node, self).__init__(**kwargs)

        self.webview = QtWebKit.QWebView()
        self.frame = self.webview.page().mainFrame()


        init_html_path = os.path.join(os.path.dirname(__file__), 'templates', 'init.html')
        self.load_file(init_html_path)

    def load_file(self, path):
        self.webview.setHtml(open(path).read())

    def add_extension(self, extname, extension):
        print "Adding extension:", extname, repr(extension)
        self.frame.addToJavaScriptWindowObject(extname, extension)
        self.frame.evaluateJavaScript(extension.generateJSWrapper(extname))

    def add_extensions(self, extensions):
        for modname, mod in extensions.items():
            for extname in mod:
                if isinstance(mod[extname], Extension):
                    extension = mod[extname]
                    extension.register_node(self)
                    self.add_extension(extname, extension)

    def add_script(self, path):
        self.frame.evaluateJavaScript(open(path).read())

    def add_default_scripts(self):
        for js_file in ('jquery_dev.js', 'trapdoor.js'):
            self.add_script(os.path.join(os.path.dirname(__file__), 'js', js_file))
    
    def add_scripts(self, paths):
        for path in paths:
            self.add_script(path)
    
    def add_scripts_from_plugin(self, plugin):
        for js in plugin.manifest.get('js', ()):
            self.add_script(os.path.join(plugin.path, js))


