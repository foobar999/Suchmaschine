from src.posting import Posting

class FuzzyPosting(Posting):
    
    # speichert eine Dokument-ID docID und einen Zugeh�rigkeitswert mem_val
    def __init__(self, docID, mem_val):
        super().__init__(docID, None)
        self.mem_val = mem_val