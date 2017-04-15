from src.processors.query_operator_processor import QueryOperatorProcessor

class NotProcessor(QueryOperatorProcessor):
    
    def __init__(self, dispatcher):
        super().__init__(dispatcher)
    
    def process(self, child_nodes):
        pass