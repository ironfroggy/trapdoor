import sys  
import os
from PyQt4 import QtCore, QtGui, QtWebKit 

import yaml

init_html_path = os.path.join(os.path.dirname(__file__), 'templates', 'init.html')


def extension(f):
    f.trapdoor_extension = True
    return f


def main(argv):
    app = QtGui.QApplication(sys.argv)  
  
    webView = QtWebKit.QWebView()  

    appname = argv[1]
    manifest = yaml.load(open(os.path.join(appname, 'manifest.yaml')))
    extensions = {}
    for ext in manifest['extensions']:
        ext_globals = {}
        execfile(os.path.join(appname, ext + '.py'), ext_globals)
        extensions[ext] = ext_globals
        print "ext globals", ext_globals
    js_scripts = []
    for js in manifest['js']:
        js_scripts.append(open(os.path.join(appname, js)).read())

    frame = webView.page().mainFrame() 

    webView.setHtml(open(init_html_path).read())

    for modname, mod in extensions.items():
        for extname in mod:
            if getattr(mod[extname], 'trapdoor_extension', False):
                frame.addToJavaScriptWindowObject(extname, mod[extname]())

 
    window = QtGui.QMainWindow()  
    window.setCentralWidget(webView)  
    window.show()  

    for js in js_scripts:
       frame.evaluateJavaScript(js)

    sys.exit(app.exec_())  

