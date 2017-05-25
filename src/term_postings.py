from src.singly_linked_list import SingleList

class TermPostings(object):

    def __init__(self, postings = None):
        #self.postings = SingleList(postings)
        self.postings = [] if postings is None else postings
    
    def get_postings_list(self):
        return [posting.docID for posting in self.postings]
            
    def __repr__(self):
        return 'TermPostings(postings={})'.format(self.postings)
      
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__ # Dictionary of class members
        else:
            return False
        
    def __neq__(self, other):
        return not self.__eq__(other)