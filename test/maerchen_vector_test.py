# -*- coding: utf-8 -*-
import unittest
from os import path, getcwd, pardir
from src.index_builder import IndexBuilder
from src.vector.weight_calculator import WeightCalculator
from src.vector.vector_ir_handler import VectorIRHandler

class MärchenFuzzyTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.num_results_tested = 10
        cls.num_decimal_places_tested = 2
        data_folder = path.join(getcwd(), pardir, "data", "Märchen")
        cls.index, docs_dict = IndexBuilder().build_from_folder(data_folder)
        cls.numdocs = len(docs_dict)
        WeightCalculator().set_posting_weights(cls.index, cls.numdocs)
        WeightCalculator().normalize_posting_weights(cls.index, cls.numdocs)
        cls.handler = VectorIRHandler()
        
        
    def testitest(self):
        pass