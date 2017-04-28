# -*- coding: utf-8 -*-
import unittest
from src.fuzzy.fuzzy_ir_handler import FuzzyIRHandler
from src.fuzzy.fuzzy_posting import FuzzyPosting

class FuzzyIRHandlerTest(unittest.TestCase):

    def setUp(self):
        self.hdl = FuzzyIRHandler()
        self.index = {'a': [FuzzyPosting(1, 1), FuzzyPosting(3, 0.6), FuzzyPosting(4, 0.01)],
                      'b': [FuzzyPosting(2, 0.8), FuzzyPosting(4, 1)],
                      'c': [FuzzyPosting(1, 0.01), FuzzyPosting(3, 0.75)]}
        self.doc_ids = list(range(0, 6))
        
    def _test_query(self, expected_res, query):
        res = self.hdl.handle_query(query, self.index, self.doc_ids)
        tuple_res = [(post.docID, post.mem_val) for post in res]
        self.assertEqual(expected_res, tuple_res)
        
    def test_a(self):
        self._test_query([(1,1), (3,0.6), (4,0.01)], 'a')
        
    def test_not_a(self):
        self._test_query([(0,1), (2,1), (3,0.4), (4,0.99), (5,1)], 'NOT a')
        
    def test_not_c(self):
        self._test_query([(0,1), (1,0.99), (2,1), (3,0.25), (4,1), (5,1)], 'NOT C')
        