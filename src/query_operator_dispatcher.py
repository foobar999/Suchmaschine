from src.query_operator import QueryOp
from src.processors.and_processor import AndProcessor
from src.processors.or_processor import OrProcessor
from src.processors.not_processor import NotProcessor
from src.processors.proximity_processor import ProximityProcessor
from src.processors.phrase_processor import PhraseProcessor

class QueryOperatorDispatcher(object):

    def dispatch(self, node):
        op = node.key
        if op.name == QueryOp.PROXIMITY(None).name:
            return ProximityProcessor().process(op.val, node.children)
        elif op == QueryOp.NOT:
            return NotProcessor().process(node.children)
        elif op in (QueryOp.AND, QueryOp.OR, QueryOp.PHRASE):
            arbitrary_args_operators = {
                QueryOp.AND: AndProcessor(),
                QueryOp.OR: OrProcessor(),
                QueryOp.PHRASE: PhraseProcessor()
            }
            return arbitrary_args_operators[op].process(node.children)
        else:
            return node.key