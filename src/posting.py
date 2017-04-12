
class Posting(object):
    
    def __init__(self, docID, positions):
        self.docID = docID
        # Here be extensions (as per the task)
        # TODO Positional Index
        self.positions = positions

    def __eq__(self, other):
        #=======================================================================
        # if isinstance(other, self.__class__):
        #     return self.__dict__ == other.__dict__  # Type safety? - Pffffff
        # else:
        #     return False
        #=======================================================================
        return self.docID == other.docID

    def __lt__(self, other):
        return self.docID < other.docID
    
    def __gt__(self, other):
        return self.docID > other.docID

    def __ne__(self, other):
        return not self.__eq__(other) 
    
    def __str__(self):
        return 'Posting({}@{})' .format(str(self.docID), self.positions)
    