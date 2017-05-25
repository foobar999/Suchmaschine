import logging
from math import log, sqrt
from src.ranked_posting import RankedPosting
from src.singly_linked_list import SingleList

class WeightCalculator(object):    
    
    def set_posting_weights(self, index, numdocs):
        N = numdocs
        logging.info('calculating tf-idf weights ({} docs)'.format(N))
        for term in index:
            df = len(index[term].postings)
            #newlist = SingleList()
            newlist = []
            for posting in index[term].postings:
                tf = len(posting.positions)
                rank = self._calc_wt_f_d(tf, df, N)
                #logging.debug('term {} doc {} df {} tf {} rank {}'.format(term,posting.docID,df,tf,rank))
                newlist.append(RankedPosting(posting.docID, rank, posting.positions))
            index[term].postings = newlist
        
        
    def normalize_posting_weights(self, index, numdocs):
        logging.info('normalizing tf-idf weights ({} docs)'.format(numdocs))
        doc_norm_factors = [0] * numdocs
        for term_postings in index.values():
            for posting in term_postings.postings:
                doc_norm_factors[posting.docID] += pow(posting.rank, 2)
        doc_norm_factors = [sqrt(factor) for factor in doc_norm_factors]
        for term_postings in index.values():
            for posting in term_postings.postings:
                posting.rank /= doc_norm_factors[posting.docID]
                
                         
    def _calc_wt_f_d(self, term_freq, doc_freq, numdocs):
        return 0 if term_freq == 0 else (1 + log(term_freq, 10)) * log(numdocs / doc_freq, 10) 
    