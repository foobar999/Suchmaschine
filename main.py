
import logging
from src.tokenizer import Tokenizer
from src.boolean_query_parser import BooleanQueryParser

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    print(BooleanQueryParser().parse2("Hexe"))
    print(BooleanQueryParser().parse2("Hexe AND Prinzessin"))
    print(BooleanQueryParser().parse2("(Hexe AND Prinzessin) OR (Frosch AND Koenig AND Tellerlein)"))
    print(BooleanQueryParser().parse2("(Hexe AND Prinzessin) OR (NOT Hexe AND Koenig)"))
    print(Tokenizer().tok_lowercase('data/myfile.txt', ' |\t|\n|\.|,|;|:|!|\?|"|-'))
    