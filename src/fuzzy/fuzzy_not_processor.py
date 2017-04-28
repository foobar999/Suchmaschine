import logging
from src.fuzzy.fuzzy_posting import FuzzyPosting
from src.processors.query_operator_processor import QueryOperatorProcessor

class FuzzyNotProcessor(QueryOperatorProcessor):

    @staticmethod
    def append_if_nonzero_memval(posting_list, posting):
        if(posting.mem_val > 0):
            posting_list.append(posting)
            
    def __init__(self, dispatcher, universe):
        super().__init__(dispatcher)
        self.universe = universe

    def process(self, nodes):
        assert len(nodes) == 1
        return self.complement(self._process_all_nodes(nodes)[0])
    
    def complement(self, postings):
        logging.debug("fuzzy complement of {}, universe {}".format(postings, self.universe))
        res = []
        ip, iu = 0, 0
        while ip < len(postings):
            postp, postu = postings[ip], self.universe[iu]
            docp, docu = postp.docID, postu.docID
            mem_valp = postp.mem_val
            if docu == docp:
                self.append_if_nonzero_memval(res, FuzzyPosting(docp, 1 - mem_valp))
                ip += 1
                iu += 1
            elif docu < docp:
                # das FuzzyPosting des Universums sollte den Zugehörigkeitswert 1 besitzen
                res.append(postu)
                iu += 1
        return res + self.universe[iu:]
        