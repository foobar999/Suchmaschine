
class TreeNode(object):
    
    def __init__(self, key = None, children = None, parent = None):
        self.key = key
        self.parent = parent
        self.children = [] if children == None else children
    
    def set_self_as_parent(self):
        for child in self.children:
            child.parent = self
            
    def set_self_as_parent_recursively(self):
        self.set_self_as_parent()
        for child in self.children:
            child.set_self_as_parent_recursively()

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.key == other.key and self.children == other.children

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '{}{}'.format(self.key, self.children)
        #return '{}{}->{}'.format(self.key, self.children, self.parent)

    #def puts(self):
        #return str(vars(self))
    #    return "key={} childs={}".format(self.key, self.children)
