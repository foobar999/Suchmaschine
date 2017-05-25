import logging
import numpy as np
from src.term import Term
from src.ranked_posting import RankedPosting

class CosScoreCalculator(object):
    
    def fast_document_cosinus_scores(self, index, numdocs):
        logging.debug('creating matrix from index, {} terms, {} docs'.format(len(index), numdocs))
        index_mat = self._index_to_mat(index, numdocs)
        logging.debug('calculated document similarity scores')
        res = index_mat.T.dot(index_mat)
        return res.tolist()
        #pprint.pprint(res)
        
    
    def cosine_score(self, queryDoc, index, numdocs):
        #logging.debug('calculating cosine(DxD), query {}, numdocs {}'.format(queryDoc, numdocs))
        scores = [0] * numdocs
        
        for termAndW in queryDoc:
            posting_list = index[termAndW[0]].postings
            for posting in posting_list:
                wf_t_d = posting.rank
                scores[posting.docID] += wf_t_d * termAndW[1]
                
        return [RankedPosting(docID,score) for docID,score in enumerate(scores)]
        
    
    def fast_cosine_score(self, query, index, numdocs):
        logging.info('calculating fast cosine, query {}, numdocs {}'.format(query, numdocs))
        scores = [0] * numdocs
        for term in query:
            logging.debug('fast cos: proc term {}'.format(term))
            posting_list = index[Term(term)].postings
            for posting in posting_list:
                wf_t_d = posting.rank
                scores[posting.docID] += wf_t_d
        return [RankedPosting(docID,score) for docID,score in enumerate(scores)]
                
      
    def _index_to_mat(self, index, numdocs):
        mat = []
        for posting_list in index.values():
            weights_of_term = [0] * numdocs
            for posting in posting_list.postings:
                weights_of_term[posting.docID] = posting.rank
            mat.append(weights_of_term)
        return np.matrix(mat)
    