# fail fail fail
class Term(object):
#    __slots__ = []
    
    literal = None
    
    def __init__(self, literal):
        self.literal = literal
        # Here be extensions (as per the task)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__ # Dictionary of class members
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
        
    def __str__(self):
        return str(self.literal)

    def __repr__(self):
        return str(self.literal)

    def __hash__(self, *args, **kwargs):
        return hash(self.literal)