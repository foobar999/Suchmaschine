# -*- coding: utf-8 -*-
import unittest
from os import path, getcwd, pardir
from src.index_builder import IndexBuilder
from src.boolean_ir_handler import BooleanIRHandler

class BooleanIRHandlerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        data_folder = path.join(getcwd(), pardir, "data", "Märchen")
        cls.index, cls.docs_dict = IndexBuilder().build_from_folder(data_folder)
        cls.handler = BooleanIRHandler()
        
    def _test_query(self, expected_res, q):
        res = [entry.docID for entry in self.handler.handle_query(q, self.index, self.docs_dict)]
        self.assertEqual(expected_res, res)
        
    def test_0_operators(self):
        self._test_query([6, 10, 12], 'hexe')
        
    def test_1_and(self):
        self._test_query([], 'hexe AND prinzessin')
        
    def test_3_ands_1_or(self):
        self._test_query([6], '(hexe AND prinzessin) OR (frosch AND könig AND tellerlein)')
        
    def test_1_not_2_ands_1_or(self):
        self._test_query([0, 2, 3, 4, 7, 9, 15, 18, 21, 22, 25], '(hexe AND prinzessin) OR (NOT hexe AND könig)')
        
    def test_prox_5(self):
        self._test_query([9, 20], 'KuchEn /5 WEIN')

    def test_phrase_2(self):
        self._test_query([22], '"sieben Zwerge"')
        
    def test_phrase_3(self):
        self._test_query([12], '"Hänsel und Gretel"')