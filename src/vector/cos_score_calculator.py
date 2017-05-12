import posting
from math import sqrt

from src.term import Term
from ranked_posting import RankedPosting

class CosScoreCalculator(object):
    
    #===========================================================================
    # def cosine_score(self, query, index, numdocs):
    #     scores = [0] * numdocs
    #     w_t_q = 1 / sqrt(len(query))    # TODO soll das so sein ????
    #     for term in query:
    #         posting_list = index[Term(term)].postings
    #         for posting in posting_list:
    #             wf_t_d = posting.rank
    #             scores[posting.docID] += w_t_q * wf_t_d
    #===========================================================================
    
    def fast_cosine_score(self, query, index, numdocs):
        scores = [0] * numdocs
        for term in query:
            posting_list = index[Term(term)].postings
            for posting in posting_list:
                wf_t_d = posting.rank
                
                scores[posting.docID] += wf_t_d
        return [RankedPosting(i,score) for i,score in enumerate(scores)]
                
                