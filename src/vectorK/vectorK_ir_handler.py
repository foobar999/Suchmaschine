# -*- coding: utf-8 -*-
import logging
import pprint
import heapq
from src.vector.cos_score_calculator import CosScoreCalculator

class VectorKIRHandler(object):
    
    def handle_query(self, query, b2, leader_index, follower_index, numdocs):
        logging.debug('handling query {}'.format(query))
        query_terms = [tok.lower() for tok in query.split()]
        logging.debug('split query to {}'.format(query_terms))        
        
        leader_scores = CosScoreCalculator().fast_cosine_score(query_terms, leader_index, numdocs)
        logging.debug('leader_scores: {}'.format(leader_scores))
        #leader_scores = [leader for leader in leader_scores if leader.rank > 0]
        #logging.debug('filtered leader_scores: {}'.format(leader_scores))
              
        selected_leaders = heapq.nlargest(b2, leader_scores, key=lambda post: post.rank)       
        logging.info('selected_leaders:\n{}'.format(pprint.pformat(selected_leaders)))
        
        res = []
        for leader in selected_leaders:
            logging.debug('processing leader {}'.format(leader))
            res.extend(CosScoreCalculator().fast_cosine_score(query_terms, follower_index[leader.docID], numdocs))          
            
        return list(set(res))
    