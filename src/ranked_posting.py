from src.posting import Posting

class RankedPosting(Posting):
    
    # speichert eine Dokument-ID docID und einen Zugehörigkeitswert rank
    def __init__(self, docID, rank, positions=None):
        super().__init__(docID, positions)
        self.rank = rank
        
    def __repr__(self):
        return '{}({},{})' .format(type(self).__name__, str(self.docID), self.rank)
    