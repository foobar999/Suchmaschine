import logging
from src.processors.query_operator_processor import QueryOperatorProcessor

class NotProcessor(QueryOperatorProcessor):
    
    def __init__(self, dispatcher):
        super().__init__(dispatcher)
    
    def process(self, nodes, universe):
        assert len(nodes) == 1
        return self.complement(self._process_all_nodes(nodes)[0], universe)
    
    def complement(self, postings, universe):
        logging.debug("complement of {}, universe {}".format(postings, universe))
        res = []
        ip, iu = 0, 0
        while ip < len(postings):
            postp, postu = postings[ip], universe[iu]
            docp, docu = postp.docID, postu.docID
            if docu == docp:
                ip += 1
                iu += 1
            if docu < docp:
                res.append(postu)
                iu += 1
        return res + universe[iu:]
    