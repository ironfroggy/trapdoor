from trapdoor.core import Node
from trapdoor.extension import Extension


class NodeManager(Extension):

    @Extension.method()
    @Extension.returns(Node)
    def createNode(self):
         self._result = Node()


    @Extension.method(str)
    def debug(self, msg):
        print "[JS]", msg
