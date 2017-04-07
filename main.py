
import logging
import os
from src.tokenizer import Tokenizer
from src.boolean_query_parser import BooleanQueryParser
from src.boolean_ir import BooleanIR

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
    # dnf_formula = [([1,5,6], True), ([6,8,9, True), [([2,3], True), ([7]], False), ([6,10], False)], ([1,9], False), [([3,4,6], False), ([8,9], False)]]
    # (A AND NOT B AND NOT 78)
    universe = list(range(1,11))
    dnf_formula = [([1,2,3,7,8], True), ([7,8,9,10], False), ([6,10], False)]
    print(BooleanIR().intersect_literals(dnf_formula, universe))
    dnf_formula = [([1,2,10], True), ([9,10], False), ([10], False), ([1,3,5,6,9], False)]
    print(BooleanIR().intersect_literals(dnf_formula, universe))