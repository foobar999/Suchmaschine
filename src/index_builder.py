# -*- coding: utf-8 -*-
import os
import logging
from collections import OrderedDict
from src.tokenizer import Tokenizer
from src.term_postings import TermPostings
from src.term import Term
from src.posting import Posting

class IndexBuilder(object):

    def build_from_folder(self, data_folder):
        
        index = {} # matches a Term with an occurrence mylist
        docsDict = {}   # matches DocID and DocName
        docID = 0
        # Reading Files
        # This works even if subfolders are used
        logging.info('building index')
        for root, _dirs, files in os.walk(data_folder):
            for file in sorted(files, key=lambda s: s.lower()):
                if file.endswith(".txt"):    # Is there anything else?
                    if docID not in docsDict:
                        docsDict[docID] = file
                    terms = Tokenizer().tok_lowercase(os.path.join(root, file), '\s|\.|,|;|:|!|\?|"|-|´|`')
                    
                    positions_of_terms = {}
                    for pos, term in enumerate(terms):
                        t = Term(term)
                        entry = positions_of_terms.get(t)
                        if entry is None:
                            entry = positions_of_terms[t] = []
                        entry.append(pos)

                    for term, term_positions in positions_of_terms.items():
                        entry = index.get(term)
                        if entry is None:
                            entry = index[term] = TermPostings()
                            # beachte: sortiertes Einfügen nicht nötig, da docID ja stets inkrementiert
                            # TODO als .postings normale list() nehmen (beachte u.A. newlist in weight_calculator.set_posting_weights()) ?
                        entry.postings.append(Posting(docID, term_positions)) 
                        
                    docID += 1
                                    
        return (OrderedDict(sorted(index.items())), docsDict)
    

    # TODO kann raus
    def build_doc_term_index(self, index, numdocs):
        doc_term_index = [list() for _i in range(numdocs)]
        for term in index:
            for posting in index[term].postings:
                doc_term_index[posting.docID].append((term, posting.rank))
                        
        return doc_term_index
        