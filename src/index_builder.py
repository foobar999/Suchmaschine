# -*- coding: utf-8 -*-
import os
import logging
from math import sqrt
from collections import OrderedDict
from src.tokenizer import Tokenizer
from src.term_postings import TermPostings
from src.term import Term
from src.ranked_posting import RankedPosting
from src.posting import Posting
from src.singly_linked_list import SingleList
from src.vector.weight_calculator import WeightCalculator

class IndexBuilder(object):

    def build_from_folder(self, data_folder):
        
        index = {} # matches a Term with an occurrence mylist
        docsDict = {}   # matches DocID and DocName
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
    
    
    def calc_tf_idf(self, index, numdocs):
        N = numdocs
        logging.info('calculating tf-idf weights ({} docs)'.format(N))
        for term in index:
            df = index[term].postings.len
            newlist = SingleList()
            for posting in index[term].postings:
                tf = len(posting.positions)
                #rank = WeightCalculator().calc_wt_f_d(tf, df, N) / docs_numterms[posting.docID]
                rank = WeightCalculator().calc_wt_f_d(tf, df, N)
                logging.debug('term {} doc {} df {} tf {} rank {}'.format(term,posting.docID,df,tf,rank))
                newlist.append(RankedPosting(posting.docID, rank, posting.positions))
            index[term].postings = newlist
        
        
    def normalize_weights(self, index, numdocs):
        logging.info('normalizing tf-idf weights ({} docs)'.format(numdocs))
        doc_norm_factors = [0] * numdocs
        for term_postings in index.values():
            for posting in term_postings.postings:
                doc_norm_factors[posting.docID] += pow(posting.rank, 2)
        doc_norm_factors = [sqrt(factor) for factor in doc_norm_factors]
        for term_postings in index.values():
            for posting in term_postings.postings:
                posting.rank /= doc_norm_factors[posting.docID]
        

    # TODO nicht als tupel speichern??
    def build_doc_term_index(self, index, numdocs):
        doc_term_index = [list() for _i in range(numdocs)]
        for term in index:
            for posting in index[term].postings:
                doc_term_index[posting.docID].append((term, posting.rank))
        
        return doc_term_index
        