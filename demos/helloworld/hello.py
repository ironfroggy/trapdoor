from PyQt4 import QtCore, QtGui

from trapdoor import extension

class Messager(QtCore.QObject):

    @QtCore.pyqtSlot(str)
    def showMessage(self, msg):
        print "called showMessage()"
        QtGui.QMessageBox.information(None, "Info", msg)

@extension
def messager(**kwargs):
    return Messager()
