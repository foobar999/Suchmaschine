from src.query_operator import QueryOp
from src.fuzzy.fuzzy_and_processor import FuzzyAndProcessor
from src.fuzzy.fuzzy_or_processor import FuzzyOrProcessor
from src.fuzzy.fuzzy_not_processor import FuzzyNotProcessor

class FuzzyOperatorDispatcher(object):
    
    def __init__(self):
        self.processors = {
            QueryOp.AND: FuzzyAndProcessor(self),
            QueryOp.OR: FuzzyOrProcessor(self),
            QueryOp.NOT: FuzzyNotProcessor(self)
        }
    
    def dispatch(self, node, universe):
        
        op = node.key
        # Blattknoten
        if isinstance(op, list):
            return op
        elif op in self.processors.keys():
            return self.processors[op].process(node.children, universe)
        else:
            raise KeyError()
        