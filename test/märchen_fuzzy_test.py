# -*- coding: utf-8 -*-
import unittest
import heapq
import numpy as np
from os import path, getcwd, pardir
from src.index_builder import IndexBuilder
from src.fuzzy.membership_calculator import MembershipCalculator
from src.fuzzy.fuzzy_ir_handler import FuzzyIRHandler

# hexe:
#===============================================================================
# {'id': 6, 'name': 'Der Froschkönig.txt', 'rank': 1.0}
# {'id': 10, 'name': 'Die Loreley.txt', 'rank': 1.0}
# {'id': 12, 'name': 'Haensel und Gretel.txt', 'rank': 1.0}
# {'id': 0, 'name': 'Aladin und die Wunderlampe.txt', 'rank': 0.984375}
# {'id': 1, 'name': 'Ali Baba und die 40 R�uber.txt', 'rank': 0.75}
# {'id': 2, 'name': 'Aschenputtel.txt', 'rank': 0.5}
# {'id': 5, 'name': 'Der fliegende Holl�nder.txt', 'rank': 0.5}
# {'id': 9, 'name': 'Die goldene Gans.txt', 'rank': 0.5}
# {'id': 13, 'name': 'Hans im Gl�ck.txt', 'rank': 0.5}
# {'id': 14, 'name': 'Hase und Igel.txt', 'rank': 0.5}
#===============================================================================

# prinz OR prinzessin:
#===============================================================================
# {'id': 0, 'name': 'Aladin und die Wunderlampe.txt', 'rank': 1.0}
# {'id': 2, 'name': 'Aschenputtel.txt', 'rank': 1.0}
# {'id': 4, 'name': 'Der Drachent�ter.txt', 'rank': 1.0}
# {'id': 7, 'name': 'Der gestiefelte Kater.txt', 'rank': 1.0}
# {'id': 8, 'name': 'Die drei Musikanten.txt', 'rank': 1.0}
# {'id': 18, 'name': 'Prinzessin auf der Erbse.txt', 'rank': 1.0}
# {'id': 25, 'name': 'Zwerg Nase.txt', 'rank': 1.0}
# {'id': 1, 'name': 'Ali Baba und die 40 R�uber.txt', 'rank': 0.99999984985885393}
# {'id': 3, 'name': 'Das tapfere Schneiderlein.txt', 'rank': 0.9991629464285714}
# {'id': 23, 'name': 'Tischlein deck dich.txt', 'rank': 0.98469387755102045}
#===============================================================================

# h�nsel AND gretel:
#===============================================================================
# {'id': 12, 'name': 'Haensel und Gretel.txt', 'rank': 1.0}
# {'id': 0, 'name': 'Aladin und die Wunderlampe.txt', 'rank': 0.9999847412109375}
# {'id': 25, 'name': 'Zwerg Nase.txt', 'rank': 0.9990234375}
# {'id': 3, 'name': 'Das tapfere Schneiderlein.txt', 'rank': 0.99609375}
# {'id': 1, 'name': 'Ali Baba und die 40 R�uber.txt', 'rank': 0.9921875}
# {'id': 13, 'name': 'Hans im Gl�ck.txt', 'rank': 0.984375}
# {'id': 2, 'name': 'Aschenputtel.txt', 'rank': 0.96875}
# {'id': 8, 'name': 'Die drei Musikanten.txt', 'rank': 0.9375}
# {'id': 9, 'name': 'Die goldene Gans.txt', 'rank': 0.9375}
# {'id': 22, 'name': 'Schneewittchen.txt', 'rank': 0.9375}
#===============================================================================

# (haus AND hexe AND wald) OR rumpelstilzchen)
#===============================================================================
# {'id': 6, 'name': 'Der Froschkönig.txt', 'rank': 1.0}
# {'id': 10, 'name': 'Die Loreley.txt', 'rank': 1.0}
# {'id': 12, 'name': 'Haensel und Gretel.txt', 'rank': 1.0}
# {'id': 21, 'name': 'Rumpelstilzchen.txt', 'rank': 1.0}
# {'id': 0, 'name': 'Aladin und die Wunderlampe.txt', 'rank': 0.984375}
# {'id': 25, 'name': 'Zwerg Nase.txt', 'rank': 0.96875}
# {'id': 1, 'name': 'Ali Baba und die 40 R�uber.txt', 'rank': 0.9375}
# {'id': 4, 'name': 'Der Drachent�ter.txt', 'rank': 0.75}
# {'id': 11, 'name': 'Frau Holle.txt', 'rank': 0.75}
# {'id': 15, 'name': 'Koenig Drosselbart.txt', 'rank': 0.75}
#===============================================================================


# dauert ein paar Sekunden
class MärchenFuzzyTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        data_folder = path.join(getcwd(), pardir, "data", "Märchen")
        index, cls.docs_dict = IndexBuilder().build_from_folder(data_folder)
        corr, docs_ocurr_mat = MembershipCalculator().calc_correlation_mat(index, len(cls.docs_dict), 0.5)
        index_terms = [term.literal for term in index.keys()]
        cls.fuzzy_index, _fuzzy_mat = MembershipCalculator().build_fuzzy_index(index_terms, corr, docs_ocurr_mat, 0.5)
        cls.handler = FuzzyIRHandler()
        print('{} ready'.format(cls.__name__))
           
           
    def _test_query(self, expected_res, q):
        res = [(entry.docID, entry.rank) for entry in self.handler.handle_query(q, self.fuzzy_index, sorted(self.docs_dict.keys()))]
        res = heapq.nlargest(10, res, key=lambda entry: entry[1])
        for res_entry, expected_res_entry in zip(res, expected_res):
            np.testing.assert_almost_equal(res_entry, expected_res_entry, decimal=2)
        
    def test_0_operators(self):
        expected_res = [(6,1.0),(10,1.0),(12,1.0),(0,0.98),(1,0.75),(2,0.5),(5,0.5),(9,0.5),(13,0.5),(14,0.5)]
        self._test_query(expected_res, 'hexe')

        
