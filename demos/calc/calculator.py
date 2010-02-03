from trapdoor import extension
from trapdoor.extension import Extension

__all__ = ['Calculator']

class Calculator(Extension):

    @Extension.method(int, int)
    def add(self, a, b):
        self._result = a + b

