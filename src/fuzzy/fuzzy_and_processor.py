import logging
from src.processors.query_operator_processor import QueryOperatorProcessor

class FuzzyAndProcessor(QueryOperatorProcessor):

    def __init__(self, dispatcher):
        super().__init__(dispatcher)
        
    def process(self, nodes, universe):
        pass

        