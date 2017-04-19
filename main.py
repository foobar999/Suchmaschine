# -*- coding: utf-8 -*-
import logging
import os
import sys
import time
import pprint
from src.index_builder import IndexBuilder
from src.boolean_ir_handler import BooleanIRHandler

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
    data_folder = os.path.join(os.getcwd(), "data")
    index_build_start = time.time()
    dictionary, docsDict = IndexBuilder().build_from_folder(data_folder)
    index_build_elapsed = time.time() - index_build_start
    print("built index in {0:.5f} seconds".format(index_build_elapsed))
     
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
                        res_docIDs = [posting.docID for posting in res_postings]
                        res_displayed = [(docID, docsDict[docID]) for docID in res_docIDs]
                        logging.info('results with postings {} '.format(res_postings))
                        print('{} results -  '.format(len(res_displayed)), end='')
                        print('took {0:.5f} seconds:'.format(query_handle_elapsed))
                        pprint.pprint(res_displayed)
                        
                        
                        
                    if mode == "fuzzy":
                        print("Processing query with fuzzy logic.")
        except KeyError as err:
            msg = '{} not found'.format(err)
            logging.error(msg)
            sys.stderr.write('{}\n'.format(msg))

# (hexe AND prinzessin) OR (frosch  AND tellerlein)

# Works:
# Gemüsehändlerin
    
    
    