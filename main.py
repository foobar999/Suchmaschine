# -*- coding: utf-8 -*-
import logging
import os
import sys
import time
import pprint
import numpy as np
import heapq
from collections import defaultdict
from enum import Enum, auto
from src.index_builder import IndexBuilder
from src.boolean_ir_handler import BooleanIRHandler
from src.fuzzy.membership_calculator import MembershipCalculator
from src.fuzzy.fuzzy_ir_handler import FuzzyIRHandler
from src.fuzzy.histogram_builder import HistogramBuilder
from src.vector.vector_ir_handler import VectorIRHandler
from src.vector.weight_calculator import WeightCalculator
from src.vectorK.vectorK_ir_handler import VectorKIRHandler
from src.vectorK.cluster_builder import ClusterBuilder
from src.term_postings import TermPostings

class IRMode(Enum):
    bool = auto()
    fuzzy = auto()
    vector = auto()
    vectork = auto()
    

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
    logging.basicConfig(level=logging.INFO)
    
    total_start_time = time.time()
    #data_folder = os.path.join(os.getcwd(), "data", "mini_mantxt")
    #data_folder = os.path.join(os.getcwd(), "data", "mantxt")
    data_folder = os.path.join(os.getcwd(), "data", "Märchen")
    print('building index from "{}" ...'.format(data_folder))
    index_build_start = time.time()
    index, docsDict = IndexBuilder().build_from_folder(data_folder)
    index_build_elapsed = time.time() - index_build_start
    print("built index in {0:.5f} seconds".format(index_build_elapsed))
    numdocs = len(docsDict)
    print('calculating weights...')
    weight_calc_start = time.time()
    WeightCalculator().set_posting_weights(index, numdocs)
    WeightCalculator().normalize_posting_weights(index, numdocs)
    weight_calc_elapsed = time.time() - weight_calc_start
    print("calculated weights in {0:.5f} seconds".format(weight_calc_elapsed))
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
    fuzzy_index, fuzzy_mat = MembershipCalculator().build_fuzzy_index(index_terms, corr, docs_ocurr_mat, 0.5)
    elapsed_time = time.time() - start_time
    print("built fuzzy index in {0:.5f} seconds".format(elapsed_time))
    print("number of fuzzy index entries: {}".format(len(fuzzy_index)))
       
    fuzzy_hist, fuzzy_bins = HistogramBuilder().calc_symm_mat_hist(fuzzy_mat, 10)
    print('fuzzy index histogram: {}'.format(fuzzy_hist))
    print('histogram bins{}'.format(fuzzy_bins))

    print("number of dict entries:", len(index))
    pprint.pprint(docsDict)
    #pprint.pprint(fuzzy_index)

    #print('index:\n{}'.format(pprint.pformat(dict(index))))
    
    print('building clusters...')
    b1 = 3  # number of leaders per follower
    b2 = 3  # number of Leaders considered for each query
    start_time = time.time()
    leaders, leaders_of_docs = ClusterBuilder().build_cluster(b1, b2, index, numdocs, docsDict)
    elapsed_time = time.time() - start_time
    print("built leader/follower cluster in {0:.5f} seconds:".format(elapsed_time))
    logging.info('{} leaders: {}'.format(len(leaders), leaders))
    logging.info('leaders of documents:\n{}'.format(pprint.pformat(leaders_of_docs)))     
    
    print('building leader, follower indices...')
    leader_follower_start_time = time.time()
    leader_index = {}
    leaders_set = set(leaders)
    for term, term_postings in index.items():
        leader_index[term] = TermPostings([post for post in term_postings.postings if post.docID in leaders_set])
    print('built leader index')
    
    follower_index = {leader: defaultdict(TermPostings) for leader in leaders}
    for term, term_postings in index.items():
        for posting in term_postings.postings:
            for leader in leaders_of_docs[posting.docID]:
                follower_index[leader][term].postings.append(posting)
                
    # cast inner defaultdicts to dicts (to prevent later accessing of non-exiting terms)
    for leader, inner_index in follower_index.items():
        follower_index[leader] = dict(inner_index)
        
    leader_follower_elapsed_time = time.time() - leader_follower_start_time
    print("built follower indices, total duration {0:.5f} seconds".format(leader_follower_elapsed_time))
    
    #print('follower index:\n{}'.format(pprint.pformat(follower_index)))    
    
    total_elapsed_time = time.time() - total_start_time
    print("total offline duration {0:.5f} seconds".format(total_elapsed_time))
    
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
                    elif mode == IRMode.vectork:
                        query_result = VectorKIRHandler().handle_query(query, b2, leader_index, follower_index, numdocs)
                    
                    elapsed_time = time.time() - start_time
                    if mode != IRMode.bool:
                        # TODO kicken von ergebnissen mit rank = 0 sinnvoll?
                        query_result = [res for res in query_result if res.rank > 0]
                        query_result = heapq.nlargest(num_displayed_highest_elements, query_result, key=lambda post: post.rank)
                        logging.debug('{} best results: {}'.format(num_displayed_highest_elements, query_result))
                    
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
            
