# -*- coding: utf-8 -*-
import unittest
import heapq
import numpy as np
from os import path, getcwd, pardir
from src.index_builder import IndexBuilder
from src.fuzzy.membership_calculator import MembershipCalculator
from src.fuzzy.fuzzy_ir_handler import FuzzyIRHandler

# dauert ein paar Sekunden
class MärchenFuzzyTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.thresh1, cls.thresh2 = 0.5, 0.5
        cls.num_results_tested = 10
        cls.num_decimal_places_tested = 2
        data_folder = path.join(getcwd(), pardir, "data", "Märchen")
        index, docs_dict = IndexBuilder().build_from_folder(data_folder)
        cls.docs = docs_dict.keys()
        corr, docs_ocurr_mat = MembershipCalculator().calc_correlation_mat(index, len(docs_dict), cls.thresh1)
        index_terms = [term.literal for term in index.keys()]
        cls.fuzzy_index, _fuzzy_mat = MembershipCalculator().build_fuzzy_index(index_terms, corr, docs_ocurr_mat, cls.thresh2)
        cls.handler = FuzzyIRHandler()
        print('{} ready'.format(cls.__name__))
           
           
    def _test_query(self, expected_res, q):
        res = [(entry.docID, entry.rank) for entry in self.handler.handle_query(q, self.fuzzy_index, self.docs)]
        res = heapq.nlargest(self.num_results_tested, res, key=lambda entry: entry[1])
        for res_entry, expected_res_entry in zip(res, expected_res):
            np.testing.assert_almost_equal(res_entry, expected_res_entry, decimal=self.num_decimal_places_tested)
        
    def test_0_operators(self):
        expected_res = [(6,1.0),(10,1.0),(12,1.0),(0,0.98),(1,0.75),(2,0.5),(5,0.5),(9,0.5),(13,0.5),(14,0.5)]
        self._test_query(expected_res, 'hexe')

    def test_1_or(self):
        expected_res = [(0,1.0),(2,1.0),(4,1.0),(7,1.0),(8,1.0),(18,1.0),(25,1.0),(1,0.99),(3,0.99),(23,0.98)]
        self._test_query(expected_res, 'prinz OR prinzessin')
    
    def test_1_and(self):
        expected_res = [(12,1.0),(0,0.99),(25,0.99),(3,0.99),(1,0.99),(13,0.98),(2,0.96),(8,0.93),(9,0.93),(22,0.93)]
        self._test_query(expected_res, 'hänsel AND gretel')
         
    
    def test_2_and_1_or(self):
        expected_res = [(6,1.0),(10,1.0),(12,1.0),(21,1.0),(0,0.98),(25,0.96),(1,0.93),(4,0.75),(11,0.75),(15,0.75)]
        self._test_query(expected_res, '(haus AND hexe AND wald) OR rumpelstilzchen)')
        

        
