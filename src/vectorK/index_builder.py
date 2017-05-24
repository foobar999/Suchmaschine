# -*- coding: utf-8 -*-
import os
import logging
from collections import OrderedDict
from src.tokenizer import Tokenizer
from src.term_postings import TermPostings
from src.term import Term
from src.posting import Posting

class IndexBuilderK(object):

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
                    
                    positions_of_term = {}
                    for pos in range(0, len(terms)):
                        t = Term(terms[pos])
                        if t not in positions_of_term:
                            positions_of_term[t] = []
                        positions_of_term[t].append(pos)
                    
                    for pos in range(0, len(terms)):
                        t = Term(terms[pos])
                        if t not in index:
                            index[t] = TermPostings()
                        index[t].postings.append(Posting(docID, positions_of_term[t]))
                        
                        # dindexTerm(t)].postings.at(docID).data.positions.append(pos)
                        # dindexTerm(t)].append(docID)    # class Term would need to be immutable
                    docID += 1
                                    
        return (OrderedDict(sorted(index.items())), docsDict)
    

    # TODO nicht als tupel speichern??
    def build_doc_term_index(self, index, numdocs):
        doc_term_index = [list() for _i in range(numdocs)]
        for term in index:
            for posting in index[term].postings:
                doc_term_index[posting.docID].append((term, posting.rank))
        
        return doc_term_index
        