# -*- coding: utf-8 -*-
import logging

class VectorKIRHandler(object):
    
    def handle_query(self, query, index, numdocs):
        logging.debug('handling query {}'.format(query))
        query_terms = [tok.lower() for tok in query.split()]
        logging.debug('split query to {}'.format(query_terms))
        
        # TODO
        # dist Query <=> Leaders
            # dist Query <=> Followers (of selected leaders)
            
        return -1