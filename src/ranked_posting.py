from src.posting import Posting

class RankedPosting(Posting):
    
    # speichert eine Dokument-ID docID und einen Zugehörigkeitswert rank
    def __init__(self, docID, rank, positions=None):
        super().__init__(docID, positions)
        self.rank = rank
        
    def __eq__(self, other):
        print("111")
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__ # Dictionary of class members
        else:
            return False

    def __repr__(self):
        return '{}({},{})' .format(type(self).__name__, str(self.docID), self.rank)
    
    def __hash__(self, *args, **kwargs):
        return hash(self.rank + self.docID)
    