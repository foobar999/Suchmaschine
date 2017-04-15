# -*- coding: utf-8 -*-
import unittest
from os import path, getcwd, pardir
from src.index_builder import IndexBuilder
from boolean_ir_handler import BooleanIRHandler

class BooleanIRHandlerTest(unittest.TestCase):

    def test_queries(self):
        data_folder = path.join(path.join(getcwd(), pardir), "data")
        index, docs_dict = IndexBuilder().build_from_folder(data_folder)
        handler = BooleanIRHandler()
        queries = [
            'hexe',
            'hexe AND prinzessin',
            '(hexe AND prinzessin) OR (frosch AND könig AND tellerlein)',
            '(hexe AND prinzessin) OR (NOT hexe AND könig)'
            ]
        results = [
            [6, 10, 14],
            [],
            [6],
            [0, 2, 3, 4, 7, 9, 15, 18, 21, 22, 25]
            ]
        for q, res in zip(queries, results):
            handler_res = handler.handle_query(q, index, docs_dict)
            doc_ids = [entry.docID for entry in handler_res]
            self.assertEqual(res, doc_ids)