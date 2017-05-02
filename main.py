# -*- coding: utf-8 -*-
import logging
import os
import sys
import time
import pprint
from src.index_builder import IndexBuilder
from src.boolean_ir_handler import BooleanIRHandler
from src.fuzzy.membership_calculator import MembershipCalculator
from src.fuzzy.fuzzy_ir_handler import FuzzyIRHandler
from src.fuzzy.histogram_builder import HistogramBuilder

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
    index, docsDict = IndexBuilder().build_from_folder(data_folder)
    numdocs = len(docsDict)
    index_build_elapsed = time.time() - index_build_start
    print("built index in {0:.5f} seconds".format(index_build_elapsed))

    start_time = time.time()
    corr, docs_ocurr_mat = MembershipCalculator().calc_correlation_mat(index, numdocs, 0.5) # last run: built correlation matrix in 1588.62204 seconds (~26min)
    elapsed_time = time.time() - start_time
    print("built correlation matrix in {0:.5f} seconds".format(elapsed_time))
    start_time = time.time()
    index_terms = [term.literal for term in index.keys()]
    fuzzy_index = MembershipCalculator().build_fuzzy_index(index_terms, corr, docs_ocurr_mat, 0.5)
    elapsed_time = time.time() - start_time
    print("built fuzzy index in {0:.5f} seconds".format(elapsed_time))
    
    index_terms = list(fuzzy_index)
    num_bins = 10
    corr_hist = HistogramBuilder().build_corr_hist(corr, index_terms, num_bins)
    print('correlation histogram: {}'.format(corr_hist))
    fuzzy_index_hist = HistogramBuilder().build_fuzzy_index_hist(fuzzy_index, num_bins)
    print('fuzzy index histogram: {}'.format(fuzzy_index_hist))

    print("number of dict entries:", len(index))
    pprint.pprint(docsDict)
#    logging.info(index)
    print("number of fuzzy index entries: {}".format(len(fuzzy_index)))
#    pprint.pprint(fuzzy_index)
    

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
                    if query == "/bool":
                        print("Boolean logic activated.")   # fake :D
                        mode = "bool"
                    elif query == "/fuzzy":
                        print("Fuzzy logic activated.")
                        mode = "fuzzy"
                    elif query == "/q":
                        break
                    
                    else:
                        print("Unknown command!", query)
                else:                           # process QUERY
                    #query_result, elapsed_time = None, None
                    if mode == "bool":
                        print("Processing query with boolean logic.")
                        start_time = time.time()
                        query_result = BooleanIRHandler().handle_query(query, index, docsDict)
                        elapsed_time = time.time() - start_time
                                              
                    elif mode == "fuzzy":
                        print("Processing query with fuzzy logic.")
                        dummy_fuzzy_doc_ids = list(range(0, 6))
                        start_time = time.time()
                        query_result = FuzzyIRHandler().handle_query(query, fuzzy_index, dummy_fuzzy_doc_ids)
                        elapsed_time = time.time() - start_time
                        query_result.sort(key=lambda post: post.rank, reverse=True)
                    
                    logging.info('{} results: {}'.format(mode, query_result))
                    print('{} results -  '.format(len(query_result)), end='')
                    print('took {0:.5f} seconds:'.format(elapsed_time))
                    for displayed_posting in generate_displayed_result(query_result, docsDict):
                        print(displayed_posting)
                    
        except KeyError as err:
            msg = '{} not found'.format(err)
            logging.error(msg)
            sys.stderr.write('{}\n'.format(msg))
