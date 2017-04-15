import logging
from src.processors.query_operator_processor import QueryOperatorProcessor

class PhraseProcessor(QueryOperatorProcessor):
    
    def __init__(self, dispatcher):
        super().__init__(dispatcher)
    
    # "a b"
    def process(self, nodes, universe):
        nodes_postings = self._process_all_nodes(nodes) 
        logging.debug('processing phrase operator on postings {}, universe{}'.format(nodes_postings, universe))
        