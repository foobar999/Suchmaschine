
class QueryOperatorProcessor(object):

    def process(self, child_nodes):
        raise NotImplementedError()
    
    def _process_child_nodes(self, child_nodes):
        return []