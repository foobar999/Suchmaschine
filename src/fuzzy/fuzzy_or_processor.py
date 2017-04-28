import logging
from src.processors.query_operator_processor import QueryOperatorProcessor
from src.ranked_posting import RankedPosting

class FuzzyOrProcessor(QueryOperatorProcessor):

    def __init__(self, dispatcher):
        super().__init__(dispatcher)

    def process(self, nodes):
        nodes_postings = self._process_all_nodes(nodes)
        logging.debug("fuzzy union nodes_postings {}".format(nodes_postings))
        curr_result = []
        for curr_postings in nodes_postings:
            logging.debug("current union result: {}".format(curr_result))        
            curr_result = self._union(curr_result, curr_postings)      
        return curr_result
    
    def _union(self, postings1, postings2):
        logging.debug("union of {}, {}".format(postings1, postings2))    
        res = []
        i1, i2 = 0, 0
        while i1 < len(postings1) and i2 < len(postings2):
            post1, post2 = postings1[i1], postings2[i2]
            doc1, doc2 = post1.docID, post2.docID
            mem_val1, mem_val2 = post1.mem_val, post2.mem_val
            if doc1 == doc2:
                res.append(RankedPosting(doc1, max(mem_val1, mem_val2)))
                i1 += 1
                i2 += 1
            elif doc1 < doc2:
                res.append(post1)
                i1 += 1
            else:
                res.append(post2)
                i2 += 1
        # hänge den Rest der Liste an, bei der i nicht am Ende ist
        return res + postings1[i1:] + postings2[i2:]

        