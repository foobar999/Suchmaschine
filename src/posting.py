
class Posting(object):
    
    def __init__(self, docID):
        self.docID = docID
        # Here be extensions (as per the task)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__  # Type safety? - Pffffff
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other) 
    
    def __str__(self):
        return str(self.docID)
    