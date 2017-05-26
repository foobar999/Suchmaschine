# -*- coding: utf-8 -*-
import os
import logging
import time
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
        # TODO zeit raus
        t1,t2,t3 = 0,0,0
        for root, _dirs, files in os.walk(data_folder):
            for file in sorted(files, key=lambda s: s.lower()):
                if file.endswith(".txt"):    # Is there anything else?
                    if docID not in docsDict:
                        docsDict[docID] = file
                    t1s = time.time()
                    terms = Tokenizer().tok_lowercase(os.path.join(root, file), '\s|\.|,|;|:|!|\?|"|-|´|`')
                    t1 += time.time() - t1s
                    
                    t2s = time.time()
                    positions_of_terms = {}
                    for pos, term in enumerate(terms):
                        t = Term(term)
                        entry = positions_of_terms.get(t)
                        if entry is None:
                            entry = positions_of_terms[t] = []
                        entry.append(pos)
                    t2 += time.time() - t2s
                    
                    t3s = time.time()
                    for term, term_positions in positions_of_terms.items():
                        entry = index.get(term)
                        if entry is None:
                            entry = index[term] = TermPostings()
                            # beachte: sortiertes Einfügen nicht nötig, da docID ja stets inkrementiert
                            # TODO als .postings normale list() nehmen (beachte u.A. newlist in weight_calculator.set_posting_weights()) ?
                        entry.postings.append(Posting(docID, term_positions)) 
                    t3 += time.time() - t3s
                        
                    docID += 1
                               
        print('times: {}, {}, {}'.format(t1,t2,t3))
                                    
        return (OrderedDict(sorted(index.items())), docsDict)
    

    # TODO kann raus
    def build_doc_term_index(self, index, numdocs):
        doc_term_index = [list() for _i in range(numdocs)]
        for term in index:
            for posting in index[term].postings:
                doc_term_index[posting.docID].append((term, posting.rank))
                        
        return doc_term_index
        