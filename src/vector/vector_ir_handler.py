# -*- coding: utf-8 -*-
import logging
from src.vector.cos_score_calculator import CosScoreCalculator

class VectorIRHandler(object):
    
    def handle_query(self, query, index, numdocs):
        logging.debug('handling query {}'.format(query))
        query_terms = [tok.lower() for tok in query.split()]
        logging.debug('split query to {}'.format(query_terms))
        return CosScoreCalculator().fast_cosine_score(query_terms, index, numdocs)