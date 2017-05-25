import logging
import heapq
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
        
        logging.debug('building clusters')
        leaders_of_docs = {}        
        for follower in followers:
            # getting (b1) leaders for the current follower
            leaders_of_follower = heapq.nlargest(b1, leaders, key=lambda leader: similarity_scores[leader][follower])
            leaders_of_docs[follower] = leaders_of_follower
        
        # set every leader as its own leader
        for leader in leaders:
            leaders_of_docs[leader] = [leader]
        
            
        return (set(leaders), followers, leaders_of_docs)

