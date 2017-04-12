# -*- coding: utf-8 -*-
import os
from src.tokenizer import Tokenizer
from src.term_postings import TermPostings
from src.posting import Posting
from src.term import Term

class IndexBuilder(object):
    
    def build_from_folder(self, data_folder):
        
        dictionary = {} # matches a Term with an occurrence mylist
        docsDict = {}   # matches DocID and DocName
        # dictionary = defaultdict(SingleList)    # this does not do what I want!
        docID = 0
        # Reading Files
        # This works even if subfolders are used
        print("Start:")
        for root, dirs, files in os.walk(data_folder):
            for file in sorted(files, key=lambda s: s.lower()):
                if file.endswith(".txt"):    # Is there anything else?
                    if docID not in docsDict:
                        docsDict[docID] = file
                    terms = Tokenizer().tok_lowercase(os.path.join(root, file), ' |\t|\n|\.|,|;|:|!|\?|"|-|´|`')
                    
                    positions_of_term = {}
                    for pos in range(0, len(terms)):
                        t = Term(terms[pos])
                        if t not in positions_of_term:
                            positions_of_term[t] = []
                        positions_of_term[t].append(pos)
                    
                    for pos in range(0, len(terms)):
                        t = Term(terms[pos])
                        if t not in dictionary:
                            dictionary[t] = TermPostings()
                        dictionary[t].postings.append(Posting(docID, positions_of_term[t]))
#                        dictionary[Term(t)].postings.at(docID).data.positions.append(pos)
                        # dictionary[Term(t)].append(docID)    # class Term would need to be immutable
                    docID += 1
                    
        return (dictionary, docsDict)
        