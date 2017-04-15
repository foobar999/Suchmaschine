import logging
from src.posting import Posting
from src.processors.query_operator_processor import QueryOperatorProcessor

class ProximityProcessor(QueryOperatorProcessor):
    
    def __init__(self, dispatcher):
        super().__init__(dispatcher)
    
    def process(self, nodes, k):
        # assert len(nodes) == 2 ???
        nodes_postings = self._process_all_nodes(nodes) 
        logging.debug('processing proximity: k {}, postings {}'.format(k, nodes_postings))
        return self._positional_intersect(nodes_postings[0], nodes_postings[1], k)
        
    # mann /3 frau
    def _positional_intersect(self, postings1, postings2, k):
        answer = []
        p1, p2 = 0, 0
        while p1 < len(postings1) and p2 < len(postings2):
            posting1, posting2 = postings1[p1], postings2[p2]
            docID1, docID2 = posting1.docID, posting2.docID
            if docID1 == docID2:
                logging.debug('terms appearing both in doc {}'.format(docID1)) 
                # TODO verkettete Liste?
                l = []
                pos1, pos2 = posting1.positions, posting2.positions
                pp1, pp2 = 0, 0
                while pp1 < len(pos1):
                    while pp2 < len(pos2):
                        if abs(pos1[pp1] - pos2[pp2]) <= k:
                            l.append(pos1[pp1])
                        elif pos2[pp2] > pos1[pp1]:
                            break
                        pp2 += 1
                    while len(l) > 0 and abs(l[0] - pos1[pp1]) > k:
                        del l[0]
                    answer.extend([Posting(docID1, [pos1[pp1], ps]) for ps in l])
                    pp1 += 1
            if docID1 <= docID2:
                p1 += 1
            if docID2 >= docID1:
                p2 += 1
        return answer