import logging
from scipy.sparse import coo_matrix
from src.term import Term
from src.ranked_posting import RankedPosting

class CosScoreCalculator(object):
    
    def fast_document_cosinus_scores(self, index, numdocs):
        logging.debug('creating matrix from index, {} terms, {} docs'.format(len(index), numdocs))
        index_mat = self._index_to_sparse_mat(index, numdocs)
        logging.debug('calculating document similarity scores')
        res = index_mat.T.dot(index_mat)
        return res.todense().tolist()        
    
    # TODO irgendwann raus
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
        logging.debug('calculating fast cosine, query {}, numdocs {}'.format(query, numdocs))
        scores = [0] * numdocs
        for term in query:
            logging.debug('fast cos: proc term {} (type {})'.format(term, type(term)))
            term_postings = index.get(Term(term))
            if term_postings is not None:
                for posting in term_postings.postings:
                    wf_t_d = posting.rank
                    scores[posting.docID] += wf_t_d
            else:
                logging.debug('term {} not present in this index'.format(term))
        return [RankedPosting(docID,score) for docID,score in enumerate(scores)]
                
      
    def _index_to_sparse_mat(self, index, numdocs):
        logging.debug('converting index to sparse matrix')
        rows, cols, values = [], [], []
        for i, posting_list in enumerate(index.values()):
            for posting in posting_list.postings:
                rows.append(i)
                cols.append(posting.docID)
                values.append(posting.rank)
        return coo_matrix((values, (rows, cols))).tocsr()
              
    