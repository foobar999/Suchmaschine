# -*- coding: utf-8 -*-
import logging
from src.vector.cos_score_calculator import CosScoreCalculator
import pprint
import heapq

class VectorKIRHandler(object):
    
    def handle_query(self, query, b2, leader_index, follower_index, numdocs):
        logging.debug('handling query {}'.format(query))
        query_terms = [tok.lower() for tok in query.split()]
        logging.debug('split query to {}'.format(query_terms))        
        
        leader_scores = CosScoreCalculator().fast_cosine_score(query_terms, leader_index, numdocs)
        logging.debug('leader_scores: {}'.format(leader_scores))
              
        selected_leaders = heapq.nlargest(b2, leader_scores, key=lambda post: post.rank)       
        logging.info('selected_leaders: {}'.format(selected_leaders))
        
        res = []
        for leader in selected_leaders:
            logging.debug('process leader {}'.format(leader))
            res.extend(CosScoreCalculator().fast_cosine_score(query_terms, follower_index[leader.docID], numdocs))
        #pprint.pprint(res)
        
        # TODO
            # dist Query <=> Followers (of selected leaders)
        
            
            
            
        return list(set(res))
    