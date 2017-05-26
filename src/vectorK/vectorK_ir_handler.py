# -*- coding: utf-8 -*-
import logging
import pprint
import heapq
from src.vector.cos_score_calculator import CosScoreCalculator
import time

class VectorKIRHandler(object):
    
    def handle_query(self, query, b2, leader_index, follower_index, numdocs):
        
        logging.debug('handling query {}'.format(query))
        query_terms = [tok.lower() for tok in query.split()]
        logging.debug('split query to {}'.format(query_terms))        
        
        scores = CosScoreCalculator().fast_cosine_score(query_terms, leader_index, numdocs)
        logging.debug('scores:\n{}'.format(pprint.pformat(scores)))
        
        # keep only leaders of scores (they're allowed to be ranked 0)
        leader_scores = [scores[leader] for leader in follower_index.keys()]
        logging.debug('filtered leader_scores:\n{}'.format(pprint.pformat(leader_scores)))
        
        # find b2 best leaders (rank 0 still allowed)      
        selected_leaders = heapq.nlargest(b2, leader_scores, key=lambda post: post.rank)       
        logging.info('selected_leaders:\n{}'.format(pprint.pformat(selected_leaders)))
        
        all_leaders_results = []
        for leader in selected_leaders:
            logging.debug('processing leader {}'.format(leader))
            leader_results = CosScoreCalculator().fast_cosine_score(query_terms, follower_index[leader.docID], numdocs)
            logging.debug('leader results {}'.format(leader_results))
            all_leaders_results.extend(leader_results)
                    
        return list(set(all_leaders_results))
    