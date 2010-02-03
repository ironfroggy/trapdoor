import sys  
import os

import yaml

from PyQt4 import QtCore, QtGui, QtWebKit 

from trapdoor.extension import Extension


class TrapdoorCore(object):

    def main(self, argv):
        app = QtGui.QApplication(sys.argv)
        self.nodes = [Node()]

        node = self.prime_node

        appname = argv[1]
        manifest = yaml.load(open(os.path.join(appname, 'manifest.yaml')))
        extensions = {}
        for ext in manifest['extensions']:
            ext_globals = {}
            execfile(os.path.join(appname, ext + '.py'), ext_globals)
            extensions[ext] = ext_globals
        js_scripts = []
        for js_file in ('jquery_dev.js', 'trapdoor.js'):
            js_scripts.append(open(os.path.join(os.path.dirname(__file__), 'js', js_file)).read())
        for js in manifest['js']:
            js_scripts.append(open(os.path.join(appname, js)).read())

        for modname, mod in extensions.items():
            for extname in mod:
                if isinstance(mod[extname], type) and issubclass(mod[extname], Extension) and mod[extname] is not Extension:
                    ext = mod[extname]()
                    node.frame.addToJavaScriptWindowObject(extname, ext)
                    node.frame.evaluateJavaScript(ext.generateJSWrapper(extname))

     
        window = QtGui.QMainWindow()  
        window.setCentralWidget(node.webview)  
        window.show()  

        for js in js_scripts:
           node.frame.evaluateJavaScript(js)

        sys.exit(app.exec_())  

    prime_node = property(lambda self: self.nodes[0])

class Node(object):

    def __init__(self):
        self.webview = QtWebKit.QWebView()
        self.frame = self.webview.page().mainFrame()


        init_html_path = os.path.join(os.path.dirname(__file__), 'templates', 'init.html')
        self.load_file(init_html_path)

    def load_file(self, path):
        self.webview.setHtml(open(path).read())
