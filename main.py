
import logging
import os
from src.tokenizer import Tokenizer
from src.boolean_query_parser import BooleanQueryParser

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