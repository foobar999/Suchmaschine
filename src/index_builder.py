# -*- coding: utf-8 -*-
import os
import logging
from collections import OrderedDict
from math import log
from src.tokenizer import Tokenizer
from src.term_postings import TermPostings
from src.term import Term
from ranked_posting import RankedPosting
from src.posting import Posting
from singly_linked_list import SingleList

class IndexBuilder(object):

    def build_from_folder(self, data_folder):
        
        index = {} # matches a Term with an occurrence mylist
        docsDict = {}   # matches DocID and DocName
        docs_numterms = []
        docID = 0
        # Reading Files
        # This works even if subfolders are used
        logging.info('building index')
        for root, dirs, files in os.walk(data_folder):
            for file in sorted(files, key=lambda s: s.lower()):
                if file.endswith(".txt"):    # Is there anything else?
                    if docID not in docsDict:
                        docsDict[docID] = file
                    terms = Tokenizer().tok_lowercase(os.path.join(root, file), '\s|\.|,|;|:|!|\?|"|-|´|`')
                    docs_numterms.append(len(terms))
                    
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
                                    
        return (OrderedDict(sorted(index.items())), docsDict, docs_numterms)
    
    
    def calc_normalized_tf_idf(self, index, docs_numterms):
        N = len(docs_numterms)
        logging.info('calculating tf-idf weights ({} docs)'.format(N))
        logging.info('number of terms per doc {}'.format(docs_numterms))
        for term in index:
            df = index[term].postings.len
            newlist = SingleList()
            for posting in index[term].postings:
                tf = len(posting.positions)
                #logging.debug('term {} doc {} df {} tf {}'.format(term,posting.docID,df,tf))
                rank = (1 + log(tf, 10)) * log(N / df, 10) / docs_numterms[posting.docID]
                newlist.append(RankedPosting(posting.docID, rank, posting.positions))
            index[term].postings = newlist
        

        