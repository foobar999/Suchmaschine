# -*- coding: utf-8 -*-
import unittest
import heapq
import numpy as np
from os import path, getcwd, pardir
from src.index_builder import IndexBuilder
from src.vector.weight_calculator import WeightCalculator
from src.vector.vector_ir_handler import VectorIRHandler


class MärchenFuzzyTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.num_results_tested = 10
        cls.num_decimal_places_tested = 3
        data_folder = path.join(getcwd(), pardir, "data", "Märchen")
        cls.index, docs_dict = IndexBuilder().build_from_folder(data_folder)
        cls.numdocs = len(docs_dict)
        WeightCalculator().set_posting_weights(cls.index, cls.numdocs)
        WeightCalculator().normalize_posting_weights(cls.index, cls.numdocs)
        cls.handler = VectorIRHandler()
        
    def _test_query(self, expected_res, q):
        res = [(entry.docID, entry.rank) for entry in self.handler.handle_query(q, self.index, self.numdocs)]
        res = heapq.nlargest(self.num_results_tested, res, key=lambda entry: entry[1])
        for res_entry, expected_res_entry in zip(res, expected_res):
            np.testing.assert_almost_equal(res_entry, expected_res_entry, decimal=self.num_decimal_places_tested)
        
    def test_haus(self):
        expected_res = [(17,0.021),(11,0.018),(20,0.018),(15,0.015),(12,0.015),(21,0.014),(23,0.013),(19,0.012),(2,0.011),(22,0.011)]
        self._test_query(expected_res, 'haus')
    
    def test_böser_wolf(self):
        expected_res = [(17,0.1),(24,0.09),(20,0.087),(4,0.05),(7,0.031),(0,0.016),(25,0.011)]
        self._test_query(expected_res, 'böser wolf')
        
    def test_hänsel_gretel(self):
        expected_res = [(12,0.283)]
        self._test_query(expected_res, 'hänsel gretel')
        
    def test_die_gabel_links_vom_teller(self):
        expected_res = [(23,0.079),(9,0.045),(25,0.037),(8,0.036),(3,0.029),(0,0.018),(16,0.004),(18,0.004),(20,0.004),(21,0.002)]
        self._test_query(expected_res, 'die gabel links vom teller')
        
    