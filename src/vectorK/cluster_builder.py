import logging
import heapq
import pprint
from math import sqrt, floor
from random import sample
from src.vector.cos_score_calculator import CosScoreCalculator


class ClusterBuilder(object):

    def build_cluster(self, b1, b2, index, numdocs, docsDict):   
        similarity_scores = CosScoreCalculator().fast_document_cosinus_scores(index, numdocs)        
        logging.info('calculated similarity scores, size {}^2'.format(len(similarity_scores)))
        
        leaders = sorted(sample(docsDict.keys(), floor(sqrt(numdocs)))) # Selection of (n^0.5) Leaders
        followers = list(set(docsDict.keys()) - set(leaders))   # Follower sind alle nicht Leader
        logging.debug('{} followers: {}'.format(len(followers), followers))
        logging.debug('{} leaders: {}'.format(len(leaders), leaders))
        
        cluster = {leader: list() for leader in leaders}    # Dictionary of lists containing all followers for every leader
        
        for fol in followers:
            # getting (b1) leaders for the current follower
            leaders_of_fol = heapq.nlargest(b1, leaders, key=lambda lead: similarity_scores[lead][fol])  
            for leader in leaders_of_fol:
                cluster[leader].append(fol)
        
        for leader in leaders:
            cluster[leader].append(leader)   # Adding leader as its own follower
            cluster[leader].sort()
        
        logging.debug('built cluster')
            
        return cluster

