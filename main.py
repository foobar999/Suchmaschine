import logging
import tokenizer

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    print(tokenizer.Tokenizer().tok_lowercase('data/myfile.txt', ' |\t|\n|\.|,|;|:|!|\?|"|-'))