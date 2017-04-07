
class Literal(object):
    
    def __init__(self, postings, is_positive):
        self.postings = postings
        self.is_positive = is_positive
        
    def __lt__(self, other):
        return len(self.postings) < len(other.postings)
    
    def __repr__(self):
        return "{}(postings={} is_positive={})".format(type(self).__name__, self.postings, self.is_positive)
    