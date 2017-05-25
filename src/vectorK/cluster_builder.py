import logging
import heapq
import pprint
from math import sqrt, floor
from random import sample
from src.index_builder import IndexBuilder
from src.vector.cos_score_calculator import CosScoreCalculator


class ClusterBuilder(object):

    def build_cluster(self, b1, b2, index, numdocs, docsDict):   
        
        #################     
        doc_term_index = IndexBuilder().build_doc_term_index(index, numdocs)
        logging.info('build doc-term-index, size {}'.format(len(doc_term_index)))
        similarity_scores = []
        for i in range(0, numdocs):
            logging.debug('processing terms of doc {} (numdocs {})'.format(i, numdocs))
            doc_terms = doc_term_index[i]
            similarity_scores.append(CosScoreCalculator().cosine_score(doc_terms, index, numdocs))
        logging.info('calculated document similarity scores')
        
        ###########################
        similarity_scores2 = CosScoreCalculator().fast_document_cosinus_scores(index, numdocs)        
        logging.info('calculated similarity scores, size {}^2'.format(len(similarity_scores2)))
        
        ###############################
        leaders = sorted(sample(docsDict.keys(), floor(sqrt(numdocs)))) # Selection of (n^0.5) Leaders
        followers = list(set(docsDict.keys()) - set(leaders))   # Follower sind alle nicht Leader
        logging.debug('{} followers: {}'.format(len(followers), followers))
        logging.debug('{} leaders: {}'.format(len(leaders), leaders))
        
        
        #######################
        #######################
        leader_similarities = {i: [similarity_scores[i][j] for j in leaders] for i in followers} # Similarity Follower <=> Leader
        # pprint.pprint(leader_similarities)
        
        cluster = {leader: list() for leader in leaders}    # Dictionary of lists containing all followers for every leader
        # pprint.pprint(cluster)
        
        for fol in followers:   # finding b1 followers for each Leader
            leaders_for_fol = heapq.nlargest(b1, leader_similarities[fol], key=lambda post: post.rank)  # getting (b1) leader for the current follower
            print('leaders: {}'.format(leaders_for_fol))
            for leader in leaders_for_fol:
                cluster[leader.docID].append(fol)
            
        for leader in leaders:
            cluster[leader].append(leader)   # Adding leader as its own follower
            cluster[leader].sort()
             
        pprint.pprint(cluster)
    
        ###############################################################
        ###############################################################
        leader_similarities = {i: [similarity_scores2[i][j] for j in leaders] for i in followers} # Similarity Follower <=> Leader
        # pprint.pprint(leader_similarities)
        cluster2 = {leader: list() for leader in leaders}    # Dictionary of lists containing all followers for every leader
        # pprint.pprint(cluster)
    
        for fol in followers:   # finding b1 followers for each Leader
            # list of tuples: [(leader_index_1, similarity_1), (leader_index_2, similarity_2), ...]
            leaders_for_fol = heapq.nlargest(b1, leaders, key=lambda l: similarity_scores2[l][fol])  # getting (b1) leader for the current follower
            for leader in leaders_for_fol:
                cluster2[leader].append(fol)
        
        for leader in leaders:
            cluster2[leader].append(leader)   # Adding leader as its own follower
            cluster2[leader].sort()
        
        pprint.pprint(cluster2)
            
        return cluster2

