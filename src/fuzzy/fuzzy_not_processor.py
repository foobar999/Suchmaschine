import logging
from src.processors.query_operator_processor import QueryOperatorProcessor

class FuzzyNotProcessor(QueryOperatorProcessor):

    def __init__(self, dispatcher, universe):
        super().__init__(dispatcher)
        self.universe = universe

    def process(self, nodes):
        pass

        