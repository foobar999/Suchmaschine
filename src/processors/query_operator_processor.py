
class QueryOperatorProcessor(object):

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def process(self, child_nodes):
        raise NotImplementedError()
    
    def _process_all_nodes(self, nodes):
        return [self.dispatcher.dispatch(node) for node in nodes]
