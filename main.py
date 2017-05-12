# -*- coding: utf-8 -*-
import logging
import os
import sys
import time
import pprint
import numpy as np
from src.index_builder import IndexBuilder
from src.boolean_ir_handler import BooleanIRHandler
from src.fuzzy.membership_calculator import MembershipCalculator
from src.fuzzy.fuzzy_ir_handler import FuzzyIRHandler
from src.fuzzy.histogram_builder import HistogramBuilder
from src.vector.vector_ir_handler import VectorIRHandler

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
    
    data_folder = os.path.join(os.getcwd(), "data")
    index_build_start = time.time()
    index, docsDict, docs_numterms = IndexBuilder().build_from_folder(data_folder)
    numdocs = len(docsDict)
    IndexBuilder().calc_normalized_tf_idf(index, docs_numterms)
    index_build_elapsed = time.time() - index_build_start
    print("built index in {0:.5f} seconds".format(index_build_elapsed))
    print('number of terms in docs: {}'.format(docs_numterms))

    start_time = time.time()
    corr, docs_ocurr_mat = MembershipCalculator().calc_correlation_mat(index, numdocs, 0.5) # last run: built correlation matrix in 1588.62204 seconds (~26min)
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
#    logging.info(index)
    print("number of fuzzy index entries: {}".format(len(fuzzy_index)))
#    pprint.pprint(fuzzy_index)
    
    modes = ('bool', 'fuzzy', 'vector')
    mode = "bool"
    print("Boolean logic activated.")
    while True: # user input loop
        try:
            print("Please enter a query or command:")
            query = input().strip()
            if len(query) < 1:
                continue    # ask for input again
            else:
                if query.startswith("/"):    # execute COMMAND
                    query_mode = query[1:]
                    if query_mode in modes:
                        print("{} logic activated.".format(query_mode))
                        mode = query_mode
                    elif query == "/q":
                        break     
                    else:
                        print("Unknown command!", query)
                else:
                    # TODO refactore query handling
                    print("Processing query with {} logic.".format(mode))
                    if mode == "bool":
                        start_time = time.time()
                        query_result = BooleanIRHandler().handle_query(query, index, docsDict)
                        elapsed_time = time.time() - start_time
                                              
                    elif mode == "fuzzy":
                        start_time = time.time()
                        query_result = FuzzyIRHandler().handle_query(query, fuzzy_index, sorted(docsDict.keys()))
                        elapsed_time = time.time() - start_time
                        query_result = sorted(query_result, key=lambda post: post.rank, reverse=True)
                        
                    elif mode == 'vector':
                        start_time = time.time()
                        query_result = VectorIRHandler().handle_query(query, index)
                        elapsed_time = time.time() - start_time
                        
                    
                    logging.info('{} results: {}'.format(mode, query_result))
                    print('{} results -  '.format(len(query_result)), end='')
                    print('took {0:.5f} seconds:'.format(elapsed_time))
                    query_result = query_result[:10]
                    print('showing results 1 - {}'.format(len(query_result)))
                    for displayed_posting in generate_displayed_result(query_result, docsDict):
                        print(displayed_posting)
                    
        except KeyError as err:
            msg = '{} not found'.format(err)
            logging.error(msg)
            sys.stderr.write('{}\n'.format(msg))
