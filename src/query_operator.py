
class QueryOp(object):
    
    @staticmethod
    def PROXIMITY(val):
        return QueryOp('PROXIMITY', val)

    def __init__(self, name, val = None):
        self.name = name
        self.val = val

    def __repr__(self):
        return 'Op.{}{}'.format(self.name, '({})'.format(self.val) if self.val != None else '')
    
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.name == other.name and self.val == other.val

    def __ne__(self, other):
        return not self.__eq__(other)

QueryOp.AND = QueryOp('AND')
QueryOp.OR = QueryOp('OR')
QueryOp.NOT = QueryOp('NOT')
QueryOp.PHRASE = QueryOp('PHRASE')
