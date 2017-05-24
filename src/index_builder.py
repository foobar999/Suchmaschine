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
                    positions_of_term = {}
                    for pos in range(0, len(terms)):
                        t = Term(terms[pos])
                        if t not in positions_of_term:
                            positions_of_term[t] = []
                        positions_of_term[t].append(pos)
                    t2 += time.time() - t2s
                    
                    t3s = time.time()
                    for pos in range(0, len(terms)):
                        t = Term(terms[pos])
                        if t not in index:
                            index[t] = TermPostings()
                        index[t].postings.append(Posting(docID, positions_of_term[t]))
                    t3 += time.time() - t3s
                        
                        # dindexTerm(t)].postings.at(docID).data.positions.append(pos)
                        # dindexTerm(t)].append(docID)    # class Term would need to be immutable
                    docID += 1
                               
        print('times: {}, {}, {}'.format(t1,t2,t3))
                                    
        return (OrderedDict(sorted(index.items())), docsDict)
    

    # TODO nicht als tupel speichern??
    def build_doc_term_index(self, index, numdocs):
        doc_term_index = [list() for _i in range(numdocs)]
        for term in index:
            for posting in index[term].postings:
                doc_term_index[posting.docID].append((term, posting.rank))
        
        return doc_term_index
        