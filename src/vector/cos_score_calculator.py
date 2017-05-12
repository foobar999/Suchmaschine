import posting
from math import sqrt

from src.term import Term
from ranked_posting import RankedPosting
from main import doc_term_index

class CosScoreCalculator(object):
    
    def cosine_score(self, doc_terms1, doc_terms2):
        score = 0
        i1, i2 = 0, 0
        while i1 < len(doc_terms1) and i2 < len(doc_terms2):
            term1, term2 = doc_terms1[i1][0], doc_terms2[i2][0]
            if term1 == term2:
                w1, w2 = doc_terms1[i1][1], doc_terms2[i2][1]
                score += w1 * w2
            elif term1 < term2:
                i1 += 1
            else:
                i2 += 2
        
        return score
    
    
    def fast_cosine_score(self, query, index, numdocs):
        scores = [0] * numdocs
        for term in query:
            posting_list = index[Term(term)].postings
            for posting in posting_list:
                wf_t_d = posting.rank
                scores[posting.docID] += wf_t_d
        return [RankedPosting(i,score) for i,score in enumerate(scores)]
                
        