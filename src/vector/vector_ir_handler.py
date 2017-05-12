# -*- coding: utf-8 -*-
import logging

class VectorIRHandler(object):
    
    def handle_query(self, query, index):
        logging.debug('handling query {}'.format(query))
        query_terms = [tok.lower() for tok in query.split()]
        logging.debug('split query to {}'.format(query_terms))
        return 'bä'