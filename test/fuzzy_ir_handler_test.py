# -*- coding: utf-8 -*-
import unittest
from src.fuzzy.fuzzy_ir_handler import FuzzyIRHandler
from src.ranked_posting import RankedPosting

class FuzzyIRHandlerTest(unittest.TestCase):

    def setUp(self):
        self.hdl = FuzzyIRHandler()
        self.index = {'a': [RankedPosting(1, 1), RankedPosting(3, 0.6), RankedPosting(4, 0.01)],
                      'b': [RankedPosting(2, 0.8), RankedPosting(4, 1)],
                      'c': [RankedPosting(1, 0.01), RankedPosting(3, 0.75)]}
        self.doc_ids = list(range(0, 6))
        
    def _test_query(self, expected_res, query):
        res = self.hdl.handle_query(query, self.index, self.doc_ids)
        tuple_res = [(post.docID, round(post.mem_val, 2)) for post in res]
        self.assertEqual(expected_res, tuple_res)
        
    def test_a(self):
        self._test_query([(1,1), (3,0.6), (4,0.01)], 'a')
        
    def test_not_a(self):
        self._test_query([(0,1), (2,1), (3,0.4), (4,0.99), (5,1)], 'NOT a')
        
    def test_not_c(self):
        self._test_query([(0,1), (1,0.99), (2,1), (3,0.25), (4,1), (5,1)], 'NOT C')
        
    def test_a_or_b_or_c(self):
        self._test_query([(1,1), (2,0.8), (3,0.75), (4,1)], 'a OR b OR c')
        
    def test_not_a_or_b_or_not_c(self):
        self._test_query([(0,1), (1,0.99), (2,1), (3,0.4), (4,1), (5,1)], 'NOT a OR b OR NOT c')
        
    def test_a_and_b_and_c(self):
        self._test_query([], 'a AND b AND c')
        
    def test_not_a_and_not_b_and_not_c(self):
        self._test_query([(0,1), (2,0.2), (3,0.25), (5,1)], 'NOT a AND NOT b AND NOT c')
        
    def test_not_b_c_not_a(self):
        self._test_query([(3,0.4)], 'NOT b AND c AND NOT a')
        
        
        