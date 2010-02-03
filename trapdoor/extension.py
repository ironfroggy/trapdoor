from PyQt4 import QtCore


class ExtensionType(type):

    def __init__(self, name, bases, attrs):
        pass


class Extension(QtCore.QObject):

    def generateJSWrapper(self, name):
        lines = [
            "var _%s = %s;" % (name, name),
            "var %s = {" % (name,),
        ]

        for attr in dir(type(self)):
            if getattr(getattr(self, attr, None), 'extension_method', False):
                lines.extend([
                    "%s: function () {" % (attr,),
                    "   _%s.%s.apply(_%s, arguments);" % (name, attr, name),
                    "   return _%s.result;" % (name,),
                    "},",
                ])

        lines.append('};')
        code = '\n'.join(lines)

        return code

    @classmethod
    def method(cls, *types):
        """Creates a decorator for an extension method taking a sequence of types."""

        def decorator(f):
            f.extension_method = True
            def _(self, *args, **kwargs):
                result = f(self, *args, **kwargs)
                self.result = result
                return result

            f_slot = QtCore.pyqtSlot(*types)(f)
            return f_slot

        return decorator

    def __get_result(self):
        return getattr(self, '_result', None)
    result = QtCore.pyqtProperty(int, fget=__get_result)

