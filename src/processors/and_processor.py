from src.processors.query_operator_processor import QueryOperatorProcessor

class AndProcessor(QueryOperatorProcessor):
    
    def __init__(self, dispatcher):
        super().__init__(dispatcher)
        
    def process(self, dispatcher, child_nodes):
        pass
    
    