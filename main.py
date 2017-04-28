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


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
    data_folder = os.path.join(os.getcwd(), "data")
    index_build_start = time.time()
    dictionary, docsDict = IndexBuilder().build_from_folder(data_folder)
    index_build_elapsed = time.time() - index_build_start
    print("built index in {0:.5f} seconds".format(index_build_elapsed))

    start_time = time.time()
    corr = MembershipCalculator().calc_correlation_mat(dictionary, 123)
    elapsed_time = time.time() - start_time
    print("built correlation matrix in {0:.5f} seconds".format(elapsed_time))
    start_time = time.time()
    fuzzy_index = MembershipCalculator().build_fuzzy_index(dictionary, corr, 456)
    elapsed_time = time.time() - start_time
    print("built fuzzy index in {0:.5f} seconds".format(elapsed_time))
    
    index_terms = list(fuzzy_index)
    num_bins = 10
    corr_hist = HistogramBuilder().build_corr_hist(corr, index_terms, num_bins)
    print('correlation histogram: {}'.format(corr_hist))
    fuzzy_index_hist = HistogramBuilder().build_fuzzy_index_hist(fuzzy_index, num_bins)
    print('fuzzy index histogram: {}'.format(fuzzy_index_hist))

    print("number of dict entries:", len(dictionary))
    pprint.pprint(docsDict)
    logging.info(dictionary)
    print("Done.")
    
    # currently the classes 'term' and 'posting' only contain a String and an int respectively but as per the task the can now be extended
    
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
                    if mode == "bool":
                        print("Processing query with boolean logic.")
                        query_handle_start = time.time()
                        res_postings = BooleanIRHandler().handle_query(query, dictionary, docsDict)
                        query_handle_elapsed = time.time() - query_handle_start
                        res_displayed = [(docsDict[p.docID], p.docID, p.positions if p.positions != None else '') for p in res_postings]
                        logging.info('results with postings {} '.format(res_postings))
                        print('{} results -  '.format(len(res_displayed)), end='')
                        print('took {0:.5f} seconds:'.format(query_handle_elapsed))
                        pprint.pprint(res_displayed, width=2000)
                                                
                    if mode == "fuzzy":
                        print("Processing query with fuzzy logic.")
                        start_time = time.time()
                        #res = FuzzyIRHandler().handle_query(query, fuzzy_index, docsDict)
                        dummy_fuzzy_doc_ids = list(range(0, 6))
                        res = FuzzyIRHandler().handle_query(query, fuzzy_index, dummy_fuzzy_doc_ids)
                        elapsed_time = time.time() - start_time
                        print('fuzzy result: {}'.format(res))
                    
        except KeyError as err:
            msg = '{} not found'.format(err)
            logging.error(msg)
            sys.stderr.write('{}\n'.format(msg))
