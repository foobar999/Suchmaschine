import logging
import os
from src.boolean_query_parser import BooleanQueryParser
from src.boolean_ir import BooleanIR
from src.boolean_ir import Literal
from src.term import Term
from src.indexterm_postings_reader import IndextermPostingsReader

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
    # 
    # # Hexe OR Prinzessin OR (A AND NOT B AND NOT 78) OR NOT test OR (NOT A AND NOT B)
    # # and_clause = [([1,5,6], True), ([6,8,9, True), [([2,3], True), ([7]], False), ([6,10], False)], ([1,9], False), [([3,4,6], False), ([8,9], False)]]
    # # UNIVERSE = {1,2,3,4,5}
    # universe = list(range(1,6))
    # # {1,2} AND {1,2,3,4} AND NOT {2} = {1}
    # and_clause = [Literal([1,2],True), Literal([1,2,3,4],True), Literal([2],False)]
    # print(BooleanIR().intersect_literals(and_clause, universe))
    # # {1} AND {1,2} AND NOT {1,2,3} = {}
    # and_clause = [Literal([1],True), Literal([1,2],True), Literal([1,2,3],False)]
    # print(BooleanIR().intersect_literals(and_clause, universe))
    # # NOT {} AND {1,2,4} AND {1,2,3,5} = {1,2}
    # and_clause = [Literal([],False), Literal([1,2,4],True), Literal([1,2,3,5],True)]
    # print(BooleanIR().intersect_literals(and_clause, universe))
    # 
    # # {1,2} OR {4,5} OR {1,4} = {1,2,4,5}
    # or_clause = [Literal([1,2],True), Literal([4,5],True), Literal([1,4],True)]
    # print(BooleanIR().union_literals(or_clause, universe))
    # # {} OR {1,2,3} OR NOT {} = UNIVERSE
    # or_clause = [Literal([],True), Literal([1,2,3],True), Literal([],False)]
    # print(BooleanIR().union_literals(or_clause, universe))
    # # NOT {1,2,3,4,5} OR NOT {1,2,3} OR {1} = {1,4,5}
    # or_clause = [Literal([1,2,3,4,5],False), Literal([1,2,3],False), Literal([1],True)]
    # print(BooleanIR().union_literals(or_clause, universe))
    #===========================================================================
    
    
    data_folder = os.path.join(os.getcwd(), "data")
    dictionary, docsDict = IndextermPostingsReader().read_from_folder(data_folder)
     
    print("number of dict entries:", len(dictionary))
    print(docsDict)
    print(dictionary)
#    alaList = dictionary["und"]
#    print(alaList)
#    print(dictionary["und"].len)
    print("Done.")
    
    # currently the classes 'term' and 'posting' only contain a String and an int respectively but as per the task the can now be extended
    
    mode = "bool"
    print("Boolean logic activated.")
    while True: # user input loop
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
                else:
                    print("Unknown command!", query)
            else:                           # process QUERY
                if mode == "bool":
                    print("Processing query with boolean logic.")
                    parse_result = BooleanQueryParser().parse_query(query)
                    print(parse_result)
                    for inner_list in parse_result:
                        for literal in inner_list:
                            key = literal.postings
                            term_postings = dictionary[key]
                            literal.postings = term_postings.get_postings_list()
                    print(parse_result)
                    universe = list(docsDict.keys())
                    and_result = [BooleanIR().intersect_literals(inner_clause, universe) for inner_clause in parse_result]
                    print('ergebbbnis', and_result)
                    total_result = BooleanIR().union_literals(and_result, universe).postings
                    print('result', total_result, [docsDict[key] for key in total_result])
                    
                if mode == "fuzzy":
                    print("Processing query with fuzzy logic.")


# (hexe AND prinzessin) OR (frosch  AND tellerlein)

    
    
    
    
    