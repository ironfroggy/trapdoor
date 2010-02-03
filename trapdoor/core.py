import sys  
import os

import yaml

from PyQt4 import QtCore, QtGui, QtWebKit 

from trapdoor.extension import Extension


class TrapdoorCore(object):

    def main(self, argv):

        init_html_path = os.path.join(os.path.dirname(__file__), 'templates', 'init.html')

        app = QtGui.QApplication(sys.argv)
        webView = QtWebKit.QWebView()
        frame = webView.page().mainFrame() 

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

        webView.setHtml(open(init_html_path).read())

        for modname, mod in extensions.items():
            for extname in mod:
                if isinstance(mod[extname], type) and issubclass(mod[extname], Extension) and mod[extname] is not Extension:
                    ext = mod[extname]()
                    frame.addToJavaScriptWindowObject(extname, ext)
                    frame.evaluateJavaScript(ext.generateJSWrapper(extname))

     
        window = QtGui.QMainWindow()  
        window.setCentralWidget(webView)  
        window.show()  

        for js in js_scripts:
           frame.evaluateJavaScript(js)

        sys.exit(app.exec_())  

