import logging
from src.posting import Posting
from src.processors.query_operator_processor import QueryOperatorProcessor

class OrProcessor(QueryOperatorProcessor):
    
    def __init__(self, dispatcher):
        super().__init__(dispatcher)
    
    def process(self, nodes, universe):
        nodes_postings = self._process_all_nodes(nodes)
        logging.debug("union nodes_postings {}, universe {}".format(nodes_postings, universe))
        curr_result = []
        for curr_postings in nodes_postings:
            logging.debug("current union result: {}".format(curr_result))        
            curr_result = self._union(curr_result, curr_postings)      
            # falls Universum das Zwischenergebnis => gib es direkt zurück    
            if len(curr_result) == len(universe):
                logging.debug("returning universe immediately")
                break
        return curr_result
    
    def _union(self, postings1, postings2):
        logging.debug("union of {}, {}".format(postings1, postings2))    
        res = []
        i1, i2 = 0, 0
        while i1 < len(postings1) and i2 < len(postings2):
            post1, post2 = postings1[i1], postings2[i2]
            doc1, doc2 = post1.docID, post2.docID
            if doc1 == doc2:
                res.append(Posting(doc1))
                i1 += 1
                i2 += 1
            elif doc1 < doc2:
                res.append(Posting(doc1))
                i1 += 1
            else:
                res.append(Posting(doc2))
                i2 += 1
        # hänge den Rest der Liste an, bei der i nicht am Ende ist
        return res + postings1[i1:] + postings2[i2:]

        