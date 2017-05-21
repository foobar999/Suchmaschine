# -*- coding: utf-8 -*-
import logging
import os
import sys
import time
import pprint
import numpy as np
import heapq
from random import sample
from math import sqrt, floor
from enum import Enum, auto
from src.index_builder import IndexBuilder
from src.boolean_ir_handler import BooleanIRHandler
from src.fuzzy.membership_calculator import MembershipCalculator
from src.fuzzy.fuzzy_ir_handler import FuzzyIRHandler
from src.fuzzy.histogram_builder import HistogramBuilder
from src.vector.vector_ir_handler import VectorIRHandler
from src.vector.cos_score_calculator import CosScoreCalculator
from src.vector.weight_calculator import WeightCalculator


class IRMode(Enum):
    bool = auto()
    fuzzy = auto()
    vector = auto()
    

def generate_displayed_result(query_result, docs_dict):
    displayed_result = []
    for posting in query_result:
        post_dict = {
            'id': posting.docID,
            'name': docs_dict[posting.docID]
        }
        for opt_attr in ['rank', 'positions']:
            if hasattr(posting, opt_attr) and getattr(posting, opt_attr) is not None: 
                post_dict[opt_attr] = getattr(posting, opt_attr)
        displayed_result.append(post_dict)
        
    return displayed_result

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
    data_folder = os.path.join(os.path.join(os.getcwd(), "data"), "Märchen")
    index_build_start = time.time()
    index, docsDict = IndexBuilder().build_from_folder(data_folder)
    numdocs = len(docsDict)
    WeightCalculator().set_posting_weights(index, numdocs)
    WeightCalculator().normalize_posting_weights(index, numdocs)
    index_build_elapsed = time.time() - index_build_start
    print("built index in {0:.5f} seconds".format(index_build_elapsed))
    #print('number of terms in docs: {}'.format(docs_numterms))

    start_time = time.time()
    corr, docs_ocurr_mat = MembershipCalculator().calc_correlation_mat(index, numdocs, 0.5)
    elapsed_time = time.time() - start_time
    print("built correlation matrix in {0:.5f} seconds".format(elapsed_time))
    
    corr_hist, corr_bins = HistogramBuilder().calc_symm_mat_hist(corr, 10)        
    np.set_printoptions(formatter={'int_kind': lambda x:' {0:d}'.format(x)})
    print('correlation histogram {}'.format(corr_hist))
    print('histogram bins{}'.format(corr_bins))
    
    start_time = time.time()
    index_terms = [term.literal for term in index.keys()]
    fuzzy_index, fuzzy_mat = MembershipCalculator().build_fuzzy_index(index_terms, corr, docs_ocurr_mat, 0)
    elapsed_time = time.time() - start_time
    print("built fuzzy index in {0:.5f} seconds".format(elapsed_time))
    
    fuzzy_hist, fuzzy_bins = HistogramBuilder().calc_symm_mat_hist(fuzzy_mat, 10)
    print('fuzzy index histogram: {}'.format(fuzzy_hist))
    print('histogram bins{}'.format(fuzzy_bins))

    print("number of dict entries:", len(index))
    pprint.pprint(docsDict)
    #logging.info(index)
    print("number of fuzzy index entries: {}".format(len(fuzzy_index)))
    #pprint.pprint(fuzzy_index)
    
    
    doc_term_index = IndexBuilder().build_doc_term_index(index, numdocs)
    print("built doc_term_index index in {0:.5f} seconds".format(elapsed_time))
    print('doc_term_index')
    
    similarity_score = []
    
    for i in range(0, numdocs):
        doc_terms = doc_term_index[i]
        similarity_score.append(CosScoreCalculator().cosine_score(doc_terms, index, numdocs))

    print('doc similarities')
    #pprint.pprint(similarity_score)
    
    
    
    
    
    leaders = sorted(sample(docsDict.keys(), floor(sqrt(numdocs)))) # Auswahl von (n^0.5) Leadern
    followers = list(set(docsDict.keys()) - set(leaders))   # Follower sind alle nicht Leader
    leader_similarities = {i: [similarity_score[i][j] for j in leaders] for i in followers} # Ähnlichkeit Follower <=> Leader
#    pprint.pprint(leader_similarities)
    logging.debug('not leaders {}'.format(followers))
    logging.debug('leaders {}'.format(leaders))
    
    b1 = 6  # number of leaders per follower
    cluster = {leader: list() for leader in leaders}    # Dictionary of lists containing all followers for every leader
#    pprint.pprint(cluster)

    for doc in followers:   # finding b1 followers for each Leader
        doc_leaders = heapq.nlargest(b1, leader_similarities[doc], key=lambda post: post.rank)  # getting (n^0.5) most similar followers 
        
        pprint.pprint(doc_leaders)
        for leader in doc_leaders:
            cluster[leader].append(doc)
        print('doc_leaders {}:'.format(doc_leaders))
    
    
    
    b2 = 3  # number of Leaders considered for each query
    
    
    
    
    
    mode = IRMode.bool
    num_displayed_highest_elements = 10
    while True: # user input loop
        try:
            print("current logic: {}".format(mode.name))
            print("Please enter a query or command:")
            query = input().strip()
            if len(query) < 1:
                continue
            else:
                if query.startswith("/"):    # execute COMMAND
                    if query == "/q":
                        print('quit ir system')
                        break
                    try:
                        mode = IRMode[query[1:]]
                        #print("{} logic activated.".format(mode.name))
                    except:
                        print("Unknown command!", query)
                else:
                    print("processing query with {} logic.".format(mode.name))
                    start_time = time.time()    
                    
                    if mode == IRMode.bool:
                        query_result = BooleanIRHandler().handle_query(query, index, docsDict)                                              
                    elif mode == IRMode.fuzzy:
                        query_result = FuzzyIRHandler().handle_query(query, fuzzy_index, sorted(docsDict.keys()))                        
                    elif mode == IRMode.vector:
                        query_result = VectorIRHandler().handle_query(query, index, numdocs)
                    
                    elapsed_time = time.time() - start_time
                    if mode != IRMode.bool:
                        query_result = heapq.nlargest(num_displayed_highest_elements, query_result, key=lambda post: post.rank)
                        logging.debug('{} best results: {}'.format(num_displayed_highest_elements, query_result))
                        query_result = [res for res in query_result if res.rank > 0]
                    
                    logging.info('{} results: {}'.format(mode, query_result))
                    print('{} results -  '.format(len(query_result)), end='')
                    print('took {0:.5f} seconds:'.format(elapsed_time))
                    print('showing results 1 - {}'.format(len(query_result)))
                    for displayed_posting in generate_displayed_result(query_result, docsDict):
                        print(displayed_posting)
                    
        except KeyError as err:
            msg = '{} not found'.format(err)
            logging.error(msg)
            sys.stderr.write('{}\n'.format(msg))
            
