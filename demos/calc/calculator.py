from PyQt4 import QtCore

from trapdoor import extension

class Calculator(QtCore.QObject):

    @QtCore.pyqtSlot(int, int)
    def add(self, a, b):
        self._result = a + b

    def _result(self):
        return self._result
    result = QtCore.pyqtProperty(int, fget=_result)

@extension
def calculator(**kwargs):
    return Calculator()
