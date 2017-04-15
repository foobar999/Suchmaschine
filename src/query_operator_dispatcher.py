from src.query_operator import QueryOp
from src.processors.and_processor import AndProcessor
from src.processors.or_processor import OrProcessor
from src.processors.not_processor import NotProcessor
from src.processors.proximity_processor import ProximityProcessor
from src.processors.phrase_processor import PhraseProcessor

class QueryOperatorDispatcher(object):

    def __init__(self, universe):
        self.universe = universe

    def dispatch(self, node):
        op = node.key
        # Blattknoten
        if isinstance(op, list):
            return op
        elif op.name == QueryOp.PROXIMITY(None).name:
            return ProximityProcessor(self).process(node.children, op.val)
        elif op == QueryOp.NOT:
            return NotProcessor(self).process(node.children, self.universe)
        elif op in (QueryOp.AND, QueryOp.OR, QueryOp.PHRASE):
            arbitrary_args_operators = {
                QueryOp.AND: AndProcessor(self),
                QueryOp.OR: OrProcessor(self),
                QueryOp.PHRASE: PhraseProcessor(self)
            }
            return arbitrary_args_operators[op].process(node.children, self.universe)
        else:
            raise KeyError()