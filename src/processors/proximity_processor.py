from src.processors.query_operator_processor import QueryOperatorProcessor

class ProximityProcessor(QueryOperatorProcessor):
    
    def __init__(self, dispatcher):
        super().__init__(dispatcher)
    
    def process(self, k, child_nodes):
        pass