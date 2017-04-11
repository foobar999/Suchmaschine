from singly_linked_list import SingleList

class TermPostings(object):

    def __init__(self):
        self.postings = SingleList()
        
    def __repr__(self):
        return 'TermPostings(postings={})'.format(self.postings)
    
    def get_postings_list(self):
        return [posting.docID for posting in self.postings]