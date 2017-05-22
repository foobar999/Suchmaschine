import logging
import heapq
from math import sqrt, floor
from random import sample
from src.index_builder import IndexBuilder
from src.vector.cos_score_calculator import CosScoreCalculator


class ClusterBuilder(object):

    def build_cluster(self, b1, b2, index, numdocs, docsDict):
        doc_term_index = IndexBuilder().build_doc_term_index(index, numdocs)
        
        similarity_score = []
        
        for i in range(0, numdocs):
            doc_terms = doc_term_index[i]
            similarity_score.append(CosScoreCalculator().cosine_score(doc_terms, index, numdocs))
    
        print('doc similarities')
        # pprint.pprint(similarity_score)
        
        leaders = sorted(sample(docsDict.keys(), floor(sqrt(numdocs)))) # Selection of (n^0.5) Leaders
        followers = list(set(docsDict.keys()) - set(leaders))   # Follower sind alle nicht Leader
        leader_similarities = {i: [similarity_score[i][j] for j in leaders] for i in followers} # Similarity Follower <=> Leader
        # pprint.pprint(leader_similarities)
        logging.debug('not leaders {}'.format(followers))
        logging.debug('leaders {}'.format(leaders))
        
        cluster = {leader: list() for leader in leaders}    # Dictionary of lists containing all followers for every leader
        # pprint.pprint(cluster)
    
        for fol in followers:   # finding b1 followers for each Leader
            leaders_for_fol = heapq.nlargest(b1, leader_similarities[fol], key=lambda post: post.rank)  # getting (b1) leader for the current follower # something strange for b1 >= 6, only returns 5 elements!?
            for leader in leaders_for_fol:
                cluster[leader.docID].append(fol)
                
        # pprint.pprint(cluster)
        
            
        return b1

