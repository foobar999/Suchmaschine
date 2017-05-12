from src.singly_linked_list import SingleList

class TermPostings(object):

    def __init__(self, values = None):
        self.postings = SingleList(values)
            
        
    def __repr__(self):
        return 'TermPostings(postings={})'.format(self.postings)
    
    def get_postings_list(self):
        return [posting.docID for posting in self.postings]