
import logging
import os
from src.tokenizer import Tokenizer
from src.boolean_query_parser import BooleanQueryParser
from src.boolean_ir import BooleanIR
from src.boolean_ir import Literal

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.info(BooleanQueryParser().parse_dnf_query("Hexe"))
    logging.info('')
    logging.info(BooleanQueryParser().parse_dnf_query("NOT Hexe AND NOT Prinzessin AND HalloWelt"))
    logging.info('')
    logging.info(BooleanQueryParser().parse_dnf_query("Hexe OR Prinzessin OR (A AND NOT B AND NOT 78) OR NOT test OR (NOT A AND NOT B)"))
    logging.info('')
    logging.info(BooleanQueryParser().parse_dnf_query("(Hexe AND Prinzessin) OR (Frosch AND Koenig AND Tellerlein)"))
    logging.info('')
    logging.info(BooleanQueryParser().parse_dnf_query("(Hexe AND Prinzessin) OR (NOT Hexe AND Koenig)"))
    logging.info('')
    logging.info(Tokenizer().tok_lowercase('data/myfile.txt', ' |\t|\n|\.|,|;|:|!|\?|"|-'))
    
    logging.info('')
    logging.info(BooleanIR().intersect([4,5,6,9,10], [3,4,5,6,11,12]))
    logging.info('')
    logging.info(BooleanIR().union([4,5,6,9,10], [3,4,5,6,11,12]))
    logging.info('')
    logging.info(BooleanIR().complement([4,5,6,9,10], [3,4,5,6,9,10,11,12]))
    logging.info('')
    logging.info(BooleanIR().intersect_complement([4,5,6,9,10], [3,4,5,6,11,12]))   
    
    # Reading Files
    # This works even if subfolders are used
    data_folder = os.getcwd() + "/data/"
    for root, dirs, files in os.walk(data_folder):
        for file in files:
            if file.endswith(".txt"):    # Is there anything else?
                Tokenizer().tok_lowercase(os.path.join(root, file), ' |\t|\n|\.|,|;|:|!|\?|"|-')
                #logging.info(Tokenizer().tok_lowercase(os.path.join(root, file), ' |\t|\n|\.|,|;|:|!|\?|"|-'))
                #input("Press Enter to continue...")
          
    print("Done.")
    
    # Hexe OR Prinzessin OR (A AND NOT B AND NOT 78) OR NOT test OR (NOT A AND NOT B)
    # and_clause = [([1,5,6], True), ([6,8,9, True), [([2,3], True), ([7]], False), ([6,10], False)], ([1,9], False), [([3,4,6], False), ([8,9], False)]]
    # UNIVERSE = {1,2,3,4,5}
    universe = list(range(1,6))
    # {1,2} AND {1,2,3,4} AND NOT {2} = {1}
    and_clause = [Literal([1,2], True), Literal([1,2,3,4], True), Literal([2], False)]
    print(BooleanIR().intersect_literals(and_clause, universe))
    # {1} AND {1,2} AND NOT {1,2,3} = {}
    and_clause = [Literal([1], True), Literal([1,2], True), Literal([1,2,3], False)]
    print(BooleanIR().intersect_literals(and_clause, universe))
    # NOT {} AND {1,2,4} AND {1,2,3,5} = {1,2}
    and_clause = [Literal([], False), Literal([1,2,4], True), Literal([1,2,3,5], True)]
    print(BooleanIR().intersect_literals(and_clause, universe))
    
    # {1,2} OR {4,5} OR {1,4} = {1,2,4,5}
    or_clause = [Literal([1,2],True), Literal([4,5],True), Literal([1,4],True)]
    print(BooleanIR().union_literals(or_clause, universe))
    # {} OR {1,2,3} OR NOT {} = UNIVERSE
    or_clause = [Literal([],True), Literal([1,2,3],True), Literal([],False)]
    print(BooleanIR().union_literals(or_clause, universe))
    # NOT {1,2,3,4,5} OR NOT {1,2,3} OR {1} = {1,4,5}
    or_clause = [Literal([1,2,3,4,5],False), Literal([1,2,3],False), Literal([1],True)]
    print(BooleanIR().union_literals(or_clause, universe))
    
    