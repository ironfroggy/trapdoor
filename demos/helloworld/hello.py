from PyQt4 import QtGui

from trapdoor.extension import Extension

class Messager(Extension):

    @Extension.method(str)
    def showMessage(self, msg):
        QtGui.QMessageBox.information(None, "Info", msg)

