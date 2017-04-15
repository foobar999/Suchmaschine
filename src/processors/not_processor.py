import logging
from src.processors.query_operator_processor import QueryOperatorProcessor

class NotProcessor(QueryOperatorProcessor):
    
    def __init__(self, dispatcher):
        super().__init__(dispatcher)
    
    def process(self, child_nodes):
        assert len(child_nodes) == 1
        return self._complement(self._process_all_nodes(child_nodes)[0], self.dispatcher.universe)
    
    def _complement(self, posting, universe):
        logging.debug("complement of {}, universe {}".format(posting, universe))
        res = []
        ip, iu = 0, 0
        while ip < len(posting):
            postp, postu = posting[ip], universe[iu]
            docp, docu = postp.docID, postu.docID
            if docu == docp:
                ip += 1
                iu += 1
            if docu < docp:
                res.append(postu)
                iu += 1
        return res + universe[iu:]