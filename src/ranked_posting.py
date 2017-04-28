from src.posting import Posting

class RankedPosting(Posting):
    
    # speichert eine Dokument-ID docID und einen Zugehörigkeitswert mem_val
    def __init__(self, docID, mem_val):
        super().__init__(docID, None)
        self.mem_val = mem_val
        
    def __repr__(self):
        return '{}({},{})' .format(type(self).__name__, str(self.docID), self.mem_val)