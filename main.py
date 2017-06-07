# -*- coding: utf-8 -*-
import logging
import os
import sys
import time
import pprint
import numpy as np
import heapq
import src.spell.levenshtein as lev
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
from src.spell.k_gram_index_builder import k_gram_index_builder


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
    logging.basicConfig(level=logging.DEBUG)
    
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
    print("{} terms, {} docs".format(len(index), numdocs))
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
    b2 = 5  # number of Leaders considered for each query
    start_time = time.time()
    leaders, leaders_of_docs = ClusterBuilder().build_cluster(b1, b2, index, numdocs, docsDict)
    elapsed_time = time.time() - start_time
    print("built leader/follower cluster in {0:.5f} seconds:".format(elapsed_time))
    logging.info('{} leaders: {}'.format(len(leaders), leaders))
    logging.info('leaders of documents:\n{}'.format(pprint.pformat(leaders_of_docs)))     
    
    print('building leader, follower indices...')
    leader_start_time = time.time()
    leader_index = ClusterBuilder().build_leader_index(index, set(leaders))
    leader_elapsed_time = time.time() - leader_start_time
    print("built leader index in {0:.5f} seconds:".format(leader_elapsed_time))
    
    follower_start_time = time.time()
    follower_index = ClusterBuilder().build_follower_index(index, leaders, leaders_of_docs)        
    follower_elapsed_time = time.time() - follower_start_time
    print("built follower indices in {0:.5f} seconds".format(follower_elapsed_time))
    #print('follower index:\n{}'.format(pprint.pformat(follower_index)))    
    
    
    
    k_gram_index = k_gram_index_builder().build_k_gram(2, index)
    #k_gram_index_builder().build_k_gram(2, index)
    
    print(lev.levenshtein_mat('somewordilike', 'anotherwordilike'))
    print(lev.levenshtein_wiki('somewordilike', 'anotherwordilike'))
    
    '''
    import timeit
    print(timeit.timeit("lev.levenshtein_mat('somewordilike', 'anotherwordilike')",setup="import src.spell.levenshtein as lev"))
    print(timeit.timeit("lev.levenshtein_numpy('somewordilike', 'anotherwordilike')",setup="import src.spell.levenshtein as lev"))
    print(timeit.timeit("lev.levenshtein_wiki('somewordilike', 'anotherwordilike')",setup="import src.spell.levenshtein as lev"))
    '''
    
    
    total_elapsed_time = time.time() - total_start_time
    print("total offline duration {0:.5f} seconds".format(total_elapsed_time))
    
#    mode = IRMode.bool
    mode = IRMode.vectork
    num_displayed_highest_elements = 10
    r = num_displayed_highest_elements
    j = 0.4
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
                        
                        ##############################################
                        # changed default mode to test spelling here #
                        ##############################################
                        
                        #if len(query_result) < r:
                        
                        corrected_Query = ''
                        for word in query.lower().split():
                            possible_words = set()
                            bi_grams = sorted(list(set(k_gram_index_builder().get_k_grams(2, word))))
                            for bi_gram in bi_grams:
                                possible_words.update(k_gram_index[bi_gram])

                            remaining_possible_words = []
                            for possible_word in possible_words:
                                #logging.debug('comparing {}, {}'.format(word, possible_word))
                                possible_bi_grams = sorted(list(set(k_gram_index_builder().get_k_grams(2, possible_word))))
                                
                                intersect_count = k_gram_index_builder().intersect_grams(bi_grams, possible_bi_grams)
                                union_count = len(possible_bi_grams) + len(bi_grams) - intersect_count
                                
                                jac = intersect_count / union_count
                                
                                if(jac > j):
                                    remaining_possible_words.append(possible_word)
                                    print('{} x {} -> {}'.format(word, possible_word, jac))
                            
                            
                            winner = min(remaining_possible_words, key=lambda candidate: lev.levenshtein_mat(word, candidate))
                            corrected_Query += (winner + ' ')
                            
                        print('Meinten sie: {}?'.format(corrected_Query))
                        
                        
                        # TODO
                        # if len(query_result) < r:
                            # Jaccard-Coefficient(X,Y) = |X n Y| / |X u Y|        # intersection / union
                            
                            # select from k_gram_index AND with Jac > j
                            
                            # use levenshtein-distance to rank the found words
                            # print(lev.levenshtein_numpy('somewordilike', 'anotherwordilike'))
                        
                    
                    elapsed_time = time.time() - start_time
                    
                    if mode != IRMode.bool:
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
            
