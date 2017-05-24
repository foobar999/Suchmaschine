# -*- coding: utf-8 -*-
import logging

class VectorKIRHandler(object):
    
    def handle_query(self, query, cluster, index, numdocs):
        logging.debug('handling query {}'.format(query))
        query_terms = [tok.lower() for tok in query.split()]
        logging.debug('split query to {}'.format(query_terms))
        
        # TODO
        # dist Query <=> Leaders
            # dist Query <=> Followers (of selected leaders)
            
        #=======================================================================
        # Ok. I have no idea how to do this.
        #
        # for pos in range(0, len(terms)):
        #     t = Term(terms[pos])
        #     if t not in index:
        #         index[t] = TermPostings()
        #     index[t].postings.append(Posting(docID, positions_of_term[t]))
        #                 
        #=======================================================================
            
            
            
            
        return -1