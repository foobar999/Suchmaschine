import logging
import re
import unicodedata
import codecs

class Tokenizer(object):

    def tok_lowercase(self, filename, tokens):     
        content = codecs.open(filename, "r", "utf-8").read()
        unicodedata.normalize('NFC', content)
        logging.debug("read content of " + filename)
        tokens = re.split(tokens, content)
        logging.debug("split content of " + filename + " " + str(len(tokens)) + " tokens")
        non_empty_tokens = list(filter(None, tokens))
        logging.debug("removed empty tokens (now " + str(len(non_empty_tokens)) + " tokens)")
        return [token.lower() for token in non_empty_tokens]
        
        
        