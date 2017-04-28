import logging
from src.ranked_posting import RankedPosting
from src.processors.query_operator_processor import QueryOperatorProcessor

class FuzzyNotProcessor(QueryOperatorProcessor):

    @staticmethod
    def append_if_nonzero_memval(posting_list, posting):
        if(posting.rank > 0):
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
            rankp = postp.rank
            if docu == docp:
                self.append_if_nonzero_memval(res, RankedPosting(docp, 1 - rankp))
                ip += 1
                iu += 1
            elif docu < docp:
                # das RankedPosting des Universums sollte den Zugehörigkeitswert 1 besitzen
                res.append(postu)
                iu += 1
        return res + self.universe[iu:]
        