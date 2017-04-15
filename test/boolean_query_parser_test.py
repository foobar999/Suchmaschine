import unittest
from src.tree_node import TreeNode
from src.query_operator import QueryOp
from src.boolean_query_parser import BooleanQueryParser
from src.query_operator import QueryOp

class BooleanQueryParserTest(unittest.TestCase):

    def to_tree(self, key):
        if isinstance(key, str):
            return TreeNode(key)
        else:
            children = [self.to_tree(ch) for ch in key[1]]
            node = TreeNode(key[0], children)
            node.set_self_as_parent()
            return node

    def test_queries(self):
        parser = BooleanQueryParser()
        queries = [
            'HaLlO',
            'A AND B AND C',
            'A OR B OR C',
            'A AND (B OR C)',
            '"A B C" AND "D" AND E',
            "A /3 B",
            'A /6 B AND " C  D"',
            'NOT A',
            'NOT A AND B',
            'NOT "A B" OR NOT A /3 B'
            ]
        results = [
            self.to_tree(('hallo')),
            self.to_tree((QueryOp.AND, ['a', 'b', 'c'])),
            self.to_tree((QueryOp.OR, ['a', 'b', 'c'])),
            self.to_tree((QueryOp.AND, ['a', (QueryOp.OR, ['b', 'c'])])),
            self.to_tree((QueryOp.AND, [(QueryOp.PHRASE, ['a','b','c']), (QueryOp.PHRASE, ['d']), 'e'])),
            self.to_tree((QueryOp.PROXIMITY(3), ['a', 'b'])),
            self.to_tree((QueryOp.AND, [(QueryOp.PROXIMITY(6), ['a', 'b']), (QueryOp.PHRASE, ['c', 'd'])])),
            self.to_tree((QueryOp.NOT, ['a'])),
            self.to_tree((QueryOp.AND, [(QueryOp.NOT, ['a']), 'b'])),
            self.to_tree((QueryOp.OR, [(QueryOp.NOT, [(QueryOp.PHRASE, ['a', 'b'])]),(QueryOp.NOT, [(QueryOp.PROXIMITY(3), ['a', 'b'])])]))
            ]
        for q, res in zip(queries, results):
            self.assertEqual(res, parser.parse(q))