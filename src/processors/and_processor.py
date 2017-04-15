import logging
from src.query_operator import QueryOp
from src.tree_node import TreeNode
from src.processors.query_operator_processor import QueryOperatorProcessor
from src.processors.not_processor import NotProcessor

class AndProcessor(QueryOperatorProcessor):
    
    class Literal(object):
    
        def __init__(self, postings, is_positive):
            self.postings = postings
            self.is_positive = is_positive
            
        def __lt__(self, other):
            return len(self.postings) < len(other.postings)
        
        def __repr__(self):
            return "{}(postings={} is_positive={})".format(type(self).__name__, self.postings, self.is_positive)
        
    def __init__(self, dispatcher):
        super().__init__(dispatcher)
        
    # erzeugt aus Knoten Literale
    # jedes Literal ist entweder positiv und enthält das Ergebnis der Auswertung des Knotens
    # oder es ist negatic und es enthält das Ergebnis der Auswertung des 1 Kindsknotens vom NOT-Knoten
    def _process_nodes_by_complement(self, nodes):
        results = []
        for node in nodes:
            is_positive = node.key != QueryOp.NOT
            postings = self._process_node(node) if is_positive else self._process_node(node.children[0])
            results.append(AndProcessor.Literal(postings, is_positive))
        return results
    
    def process(self, nodes, universe):
        logging.debug("intersect nodes {}, universe {}".format(nodes, universe))
        if len(nodes) == 0:
            return []
        elif len(nodes) == 1:
            return self._process_node(nodes[0])
        literals = self._process_nodes_by_complement(nodes)
        logging.debug("expanded positive nodes, and children of negative nodes: {}".format(literals))
        sorted_literals = sorted(literals)
        logging.debug("sorted intersect literals {}".format(sorted_literals, universe))
        
        current_res = sorted_literals[0]
        for i in range(1, len(sorted_literals)):
            literal = sorted_literals[i]
            logging.debug("current intersect result: {}".format(current_res))        
            current_res = self._intersect_2_literals(current_res, literal, universe)      
            # falls leere Menge das Zwischenergebnis => gib es direkt zurück    
            if len(current_res.postings) == 0:
                logging.debug("returning empty postings immediately")
                break
    
        return current_res.postings
    
    
    def _intersect_2_literals(self, lit1, lit2, universe):
        res_postings = None
        if lit1.is_positive and lit2.is_positive:
            res_postings = self._intersect(lit1.postings, lit2.postings)
        elif lit1.is_positive and not lit2.is_positive:
            res_postings = self._intersect_complement(lit1.postings, lit2.postings)
        elif not lit1.is_positive and lit2.is_positive:
            res_postings = self._intersect_complement(lit2.postings, lit1.postings)
        else:
            not_processor = NotProcessor(self.dispatcher)
            complement1 = not_processor.complement(lit1.postings, universe)
            complement2 = not_processor.complement(lit2.postings, universe)
            res_postings = self._intersect(complement1, complement2)
        return AndProcessor.Literal(res_postings, True)

    def _intersect(self, postings1, postings2):
        logging.debug("intersect of {}, {}".format(postings1, postings2))        
        res = []
        i1, i2 = 0, 0
        while i1 < len(postings1) and i2 < len(postings2):
            post1, post2 = postings1[i1], postings2[i2]
            doc1, doc2 = post1.docID, post2.docID
            if doc1 == doc2:
                res.append(post1)
                i1 += 1
                i2 += 1
            elif doc1 < doc2:
                i1 += 1
            else:
                i2 += 1
        return res
    
    # postings1 positiv, postings2 negativ
    def _intersect_complement(self, posting1, posting2):
        logging.debug("intersect_complement of {}, {}".format(posting1, posting2))
        res = []
        i1, i2 = 0, 0
        while i1 < len(posting1) and i2 < len(posting2):
            doc1, doc2 = posting1[i1], posting2[i2]
            if doc1 == doc2:
                i1 += 1
                i2 += 1
            elif doc1 < doc2:
                res.append(doc1)
                i1 += 1
            else:
                i2 += 1
        return res + posting1[i1:]
        