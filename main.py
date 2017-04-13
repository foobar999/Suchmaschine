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
    
    #===========================================================================
    # logging.info(BooleanQueryParser().parse_query("Hexe"))
    # logging.info('')
    # logging.info(BooleanQueryParser().parse_query("NOT Hexe AND NOT Prinzessin AND HalloWelt"))
    # logging.info('')
    # logging.info(BooleanQueryParser().parse_query("Hexe OR Prinzessin OR (A AND NOT B AND NOT 78) OR NOT test OR (NOT A AND NOT B)"))
    # logging.info('')
    # logging.info(BooleanQueryParser().parse_query("(Hexe AND Prinzessin) OR (Frosch AND Koenig AND Tellerlein)"))
    # logging.info('')
    # logging.info(BooleanQueryParser().parse_query("(Hexe AND Prinzessin) OR (NOT Hexe AND Koenig)"))
    # logging.info('')
    # logging.info(Tokenizer().tok_lowercase('data/myfile.txt', ' |\t|\n|\.|,|;|:|!|\?|"|-'))
    # logging.info('')
    # logging.info(BooleanIR().intersect([4,5,6,9,10], [3,4,5,6,11,12]))
    # logging.info('')
    # logging.info(BooleanIR().union([4,5,6,9,10], [3,4,5,6,11,12]))
    # logging.info('')
    # logging.info(BooleanIR().complement([4,5,6,9,10], [3,4,5,6,9,10,11,12]))
    # logging.info('')
    # logging.info(BooleanIR().intersect_complement([4,5,6,9,10], [3,4,5,6,11,12]))   
    #===========================================================================

    #===========================================================================
    # from src.literal import Literal
    # from src.boolean_ir import BooleanIR
    # 
    # universe = list(range(1,6))    
    # # {1,2} AND {1,2,3,4} AND NOT {2} = {1}
    # and_clause = [Literal([1,2],True), Literal([1,2,3,4],True), Literal([2],False)]
    # logging.info(BooleanIR().intersect_literals(and_clause, universe))
    # # {1} AND {1,2} AND NOT {1,2,3} = {}
    # and_clause = [Literal([1],True), Literal([1,2],True), Literal([1,2,3],False)]
    # logging.info(BooleanIR().intersect_literals(and_clause, universe))
    # # NOT {} AND {1,2,4} AND {1,2,3,5} = {1,2}
    # and_clause = [Literal([],False), Literal([1,2,4],True), Literal([1,2,3,5],True)]
    # logging.info(BooleanIR().intersect_literals(and_clause, universe))
    # # NOT {} AND {} = {}
    # and_clause = [Literal([],False), Literal([],True)]
    # logging.info(BooleanIR().intersect_literals(and_clause, universe))
    # # NOT {3} = {1,2,4,5}
    # and_clause = [Literal([3],False)]
    # logging.info(BooleanIR().intersect_literals(and_clause, universe))
    # # {3} = {3}
    # and_clause = [Literal([3],True)]
    # logging.info(BooleanIR().intersect_literals(and_clause, universe))
    # # {} = {}
    # and_clause = [Literal([],True)]
    # logging.info(BooleanIR().intersect_literals(and_clause, universe))
    # # NOT {} = UNIVERSE
    # and_clause = [Literal([],False)]
    # logging.info(BooleanIR().intersect_literals(and_clause, universe))
    #  
    # # {1,2} OR {4,5} OR {1,4} = {1,2,4,5}
    # or_clause = [Literal([1,2],True), Literal([4,5],True), Literal([1,4],True)]
    # logging.info(BooleanIR().union_literals(or_clause, universe))
    # # {} OR {1,2,3} OR NOT {} = UNIVERSE
    # or_clause = [Literal([],True), Literal([1,2,3],True), Literal([],False)]
    # logging.info(BooleanIR().union_literals(or_clause, universe))
    # # NOT {1,2,3,4,5} OR NOT {1,2,3} OR {1} = {1,4,5}
    # or_clause = [Literal([1,2,3,4,5],False), Literal([1,2,3],False), Literal([1],True)]
    # logging.info(BooleanIR().union_literals(or_clause, universe))
    # exit() 
    #===========================================================================
    
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
                        res_docIDs = BooleanIRHandler().handle_query(query, dictionary, docsDict)
                        query_handle_elapsed = time.time() - query_handle_start
                        res_displayed = [(docID, docsDict[docID]) for docID in res_docIDs]
                        
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
    
    
    