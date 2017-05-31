import logging
import heapq
from math import sqrt, floor
from random import sample
from collections import defaultdict
from src.term_postings import TermPostings
from src.vector.cos_score_calculator import CosScoreCalculator


class ClusterBuilder(object):

    def build_cluster(self, b1, b2, index, numdocs, docsDict):   
        similarity_scores = CosScoreCalculator().fast_document_cosinus_scores(index, numdocs)        
        logging.info('calculated similarity scores, size {}^2'.format(len(similarity_scores)))
        for row in similarity_scores:
            logging.debug(row)
        
        leaders = sorted(sample(docsDict.keys(), floor(sqrt(numdocs)))) # Selection of (n^0.5) Leaders
        followers = list(set(docsDict.keys()) - set(leaders))   # Follower sind alle nicht Leader
        logging.debug('{} followers: {}'.format(len(followers), followers))
        logging.debug('{} leaders: {}'.format(len(leaders), leaders))         
        
        logging.debug('building clusters')
        leaders_of_docs = {}        
        for follower in followers:
            # getting (b1) leaders for the current follower
            leaders_of_follower = heapq.nlargest(b1, leaders, key=lambda leader: similarity_scores[leader][follower])
            logging.debug('leaders_of_follower of {}: {}'.format(follower, leaders_of_follower))
            leaders_of_docs[follower] = leaders_of_follower
        
        # set every leader as its own leader
        for leader in leaders:
            leaders_of_docs[leader] = [leader]
        
        # for each documents: sort its leaders by docID 
        for leaders_of_follower in leaders_of_docs.values():
            leaders_of_follower.sort()
            
        return (leaders, leaders_of_docs)
    
    
    def build_leader_index(self, index, leaders):
        leader_index = {}
        for term, term_postings in index.items():
            leader_index[term] = TermPostings([post for post in term_postings.postings if post.docID in leaders])
        
        return leader_index

    
    def build_follower_index(self, index, leaders, leaders_of_docs):
        follower_index = {leader: defaultdict(TermPostings) for leader in leaders}
        for term, term_postings in index.items():
            for posting in term_postings.postings:
                for leader in leaders_of_docs[posting.docID]:
                    follower_index[leader][term].postings.append(posting)
                    
        # cast inner defaultdicts to dicts (to prevent later accessing of non-exiting terms)
        for leader, inner_index in follower_index.items():
            follower_index[leader] = dict(inner_index)

        return follower_index
