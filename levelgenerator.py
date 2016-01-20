from utility import * # noqa
from importer import * # noqa

level_dict = ['bridge', 'flat', 'maze', 'puzzle', 'shop']
node_dict = ['right', 'left', 'up', 'down']


class Treenode(object):
    def __init__(self):
        self.number = None
        self.type = None
        self.left = None
        self.right = None
        self.up = None
        self.down = None

    def setup(self):
        self.type = level_dict[random.randint(0, len(level_dict) - 1)]

    def available(self):
        child = []
        if self.left is None:
            child.append('left')
        if self.right is None:
            child.append('right')
        if self.up is None:
            child.append('up')
        if self.down is None:
            child.append('down')
        if len(child) is 0:
            return False
        else:
            return child

    def printobject(self):
        print str(self.number) + " " + str(self.type) + "   begin"

        try:
            self.left.printobject()
        except:
            pass
        try:
            self.down.printobject()
        except:
            pass
        try:
            self.up.printobject()
        except:
            pass
        try:
            self.right.printobject()
        except:
            pass
        print str(self.number) + " " + str(self.type) + "   end"


class LevelTree(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.up = None
        self.down = None
        self.parent = None
        self.nodes = []

    def setup(self):
        self.parent = Treenode()
        self.parent.number = 0
        self.parent.setup()
        self.nodes.append(self.parent)

    def populate(self):
        for i in range(16):
            flag = True
            while flag:
                node = self.nodes[random.randint(0, len(self.nodes) - 1)]
                child = node.available()
                if child is False:
                    self.nodes.remove(node)
                else:
                    flag = False
                    selection = child[random.randint(0, len(child) - 1)]
                    newnode = Treenode()
                    newnode.setup()
                    newnode.number = i + 1
                    self.nodes.append(newnode)
                    if selection == 'up':
                        node.up = newnode
                    if selection == 'down':
                        node.down = newnode
                    if selection == 'right':
                        node.right = newnode
                    if selection == 'left':
                        node.left = newnode


tree = LevelTree()
tree.setup()
tree.populate()
tree.parent.printobject()
