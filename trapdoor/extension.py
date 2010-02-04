from PyQt4 import QtCore


class ExtensionType(type):

    def __init__(self, name, bases, attrs):
        pass


class Extension(QtCore.QObject):

    def __init__(self, node=None, *args, **kwargs):
        self.node = node
        super(Extension, self).__init__(*args, **kwargs)


    def generateJSWrapper(self, name):
        lines = [
            "var _%s = %s;" % (name, name),
            "var %s = {" % (name,),
        ]

        for attr in dir(type(self)):
            method = getattr(self, attr, None)
            if getattr(method, 'extension_method', False):
                try:
                    result_type = method.result_type.__name__
                except AttributeError:
                    result_line = ''
                else:
                    if issubclass(method.result_type, Extension):
                        # This returns an Extension object to be passed back to JS
                        result_line = "   return _result_extobject;"
                    else:
                        result_line = "   return _%s.result_%s;" % (name, result_type)

                lines.extend([
                    "%s: function () {" % (attr,),
                    "   _%s.%s.apply(_%s, arguments);" % (name, attr, name),
                    result_line,
                    "},",
                ])

        lines.append('};')
        code = '\n'.join(lines)
        return code

    @classmethod
    def returns(cls, type_):
        def decorator(f):
            f.result_type = type_
            return f
        return decorator

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

    def __get_result_int(self):
        return getattr(self, '_result', None)
    result_int = QtCore.pyqtProperty(int, fget=__get_result_int)

    def __get_result_str(self):
        return getattr(self, '_result', None)
    result_str = QtCore.pyqtProperty(str, fget=__get_result_str)

    def _get_result(self):
        self.__result
        return self.__result
    def _set_result(self, value):
        self.__result = value
        if isinstance(value, Extension):
            unique_name = self.node.add_nameless_extension(value)
            self.node.frame.evaluateJavaScript('_result_extobject = %s;' % (unique_name,))
    _result = property(_get_result, _set_result)

def Factory(cls):
    class ExtensionFactory(Extension):
        @Extension.method()
        @Extension.returns(cls)
        def create(self):
            self._result = cls(node=self.node)
    return ExtensionFactory
