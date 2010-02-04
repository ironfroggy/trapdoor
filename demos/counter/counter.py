from trapdoor.extension import Extension

class Counter(Extension):

    value = 0

    @Extension.method()
    @Extension.returns(int)
    def get(self):
        self._result = self.value

    @Extension.method()
    def incr(self):
        self.value += 1

counter = Counter()
