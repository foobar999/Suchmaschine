import logging
from src.posting import Posting
from src.processors.query_operator_processor import QueryOperatorProcessor

class OrProcessor(QueryOperatorProcessor):
    
    def __init__(self, dispatcher):
        super().__init__(dispatcher)
    
    def process(self, child_nodes, universe):
        postings = self._get_postings_of_nodes(self._process_all_nodes(child_nodes))
        logging.debug("union postings {}, universe {}".format(postings, universe))
        current_res = []
        for posting in postings:
            logging.debug("current union result: {}".format(current_res))        
            current_res = self._union(current_res, posting)      
            # falls Universum das Zwischenergebnis => gib es direkt zurück    
            if len(current_res) == len(universe):
                logging.debug("returning universe immediately")
                break
        return current_res
    
    def _union(self, posting1, posting2):
        logging.debug("union of {}, {}".format(posting1, posting2))    
        res = []
        i1, i2 = 0, 0
        while i1 < len(posting1) and i2 < len(posting2):
            doc1, doc2 = posting1[i1].docID, posting2[i2].docID
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
        return res + posting1[i1:] + posting2[i2:]

        