import logging
from tokenizer import Tokenizer
from boolean_query_parser import BooleanQueryParser

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    print(BooleanQueryParser().parse("Hexe"))
    print(BooleanQueryParser().parse("Hexe AND Prinzessin"))
    print(BooleanQueryParser().parse("(Hexe AND Prinzessin) OR (Frosch AND Koenig AND Tellerlein)"))
    print(BooleanQueryParser().parse("(Hexe AND Prinzessin) OR (NOT Hexe AND Koenig)"))
    print(Tokenizer().tok_lowercase('data/myfile.txt', ' |\t|\n|\.|,|;|:|!|\?|"|-'))