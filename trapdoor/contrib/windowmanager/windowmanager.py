from PyQt4 import QtGui

from trapdoor.extension import Extension

class WindowManager(Extension):

    @Extension.method()
    def createWindow(self):
        window = self.qtwindow = QtGui.QMainWindow()
        window.setCentralWidget(self.node.webview)
        window.show()

windowmanager = WindowManager()
