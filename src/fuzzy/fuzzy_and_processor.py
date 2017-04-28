import logging
from src.processors.and_processor import AndProcessor
from src.fuzzy.fuzzy_not_processor import FuzzyNotProcessor
from src.ranked_posting import RankedPosting

class FuzzyAndProcessor(AndProcessor):

    def __init__(self, dispatcher, universe):
        super().__init__(dispatcher)
        self.universe = universe
        
    def process(self, nodes):    
        return super().process(nodes, self.universe)
    
    def _intersect_2_literals(self, lit1, lit2, universe):
        res_postings = None
        if lit1.is_positive and lit2.is_positive:
            res_postings = self._intersect(lit1.postings, lit2.postings)
        elif lit1.is_positive and not lit2.is_positive:
            res_postings = self._intersect_complement(lit1.postings, lit2.postings)
        elif not lit1.is_positive and lit2.is_positive:
            res_postings = self._intersect_complement(lit2.postings, lit1.postings)
        else:
            not_processor = FuzzyNotProcessor(self.dispatcher, self.universe)
            complement1 = not_processor.complement(lit1.postings)
            res_postings = self._intersect_complement(complement1, lit2.postings)
        return AndProcessor.Literal(res_postings, True)

    def _intersect(self, postings1, postings2):
        logging.debug("fuzzy intersect of {}, {}".format(postings1, postings2))        
        res = []
        i1, i2 = 0, 0
        while i1 < len(postings1) and i2 < len(postings2):
            post1, post2 = postings1[i1], postings2[i2]
            doc1, doc2 = post1.docID, post2.docID
            rank1, rank2 = post1.rank, post2.rank            
            if doc1 == doc2:
                res.append(RankedPosting(doc1, min(rank1, rank2)))
                i1 += 1
                i2 += 1
            elif doc1 < doc2:
                i1 += 1
            else:
                i2 += 1
        return res
    
    # postings1 positiv, postings2 negativ
    def _intersect_complement(self, posting1, posting2):
        logging.debug("fuzzy intersect_complement of {}, {}".format(posting1, posting2))
        res = []
        i1, i2 = 0, 0
        while i1 < len(posting1) and i2 < len(posting2):
            post1, post2 = posting1[i1], posting2[i2]
            doc1, doc2 = post1.docID, post2.docID
            rank1, rank2 = post1.rank, post2.rank  
            if doc1 == doc2:      
                FuzzyNotProcessor.append_if_nonzero_memval(res, RankedPosting(doc1, min(rank1, 1 - rank2)))
                i1 += 1
                i2 += 1
            elif doc1 < doc2:
                res.append(post1)
                i1 += 1
            else:
                i2 += 1
        return res + posting1[i1:]
