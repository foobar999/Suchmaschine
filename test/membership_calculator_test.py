# -*- coding: utf-8 -*-
import unittest
from src.fuzzy.membership_calculator import MembershipCalculator
from term_postings import TermPostings
from term import Term
from posting import Posting
import numpy as np


class MembershipCalculatorTest(unittest.TestCase):

    def setUp(self):
        # TODO constructor SInglyLinkedList, TermPostings
        self.numdocs = 3
        verans, sehensw, tipp, krefeld = Term('veranstaltung'), Term('sehenswürdigkeit'), Term('tipp'), Term('krefeld')
        self.index = {
            krefeld: TermPostings(),
            sehensw: TermPostings(),
            tipp: TermPostings(),
            verans: TermPostings()
        }
        self.index[verans].postings.append(Posting(0, []))
        self.index[verans].postings.append(Posting(1, []))
        self.index[verans].postings.append(Posting(2, []))
        self.index[sehensw].postings.append(Posting(0, []))
        self.index[sehensw].postings.append(Posting(1, []))
        self.index[tipp].postings.append(Posting(0, []))
        self.index[tipp].postings.append(Posting(2, []))
        self.index[krefeld].postings.append(Posting(1, []))
        self.calc = MembershipCalculator()
        
    def test_calc_correlation_mat(self):
        mat, docs_ocurr_mat = self.calc.calc_correlation_mat(self.index, self.numdocs, 0)
        expected_mat = np.matrix([[1,0.5,0,0.33],[0.5,1,0.33,0.67],[0,0.33,1,0.67],[0.33,0.67,0.67,1]])
        np.testing.assert_almost_equal(mat, expected_mat, decimal=2)
        
    def _ranked_to_list_dict(self, ranked_dict):
        return {key: [round(val.rank, 1) for val in value] for key,value in ranked_dict.items()}
        
        
    def test_build_fuzzy_index(self):
        corr, docs_ocurr_mat = self.calc.calc_correlation_mat(self.index, self.numdocs, 0)
        terms = [term.literal for term in self.index.keys()]
        res = self.calc.build_fuzzy_index(terms, corr, docs_ocurr_mat, 0)
        res = self._ranked_to_list_dict(res)
        expected = {
            'krefeld': [0.7, 1.0, 0.3], 
            'sehenswürdigkeit': [1.0, 1.0, 0.8],
            'tipp': [1.0, 0.8, 1.0],
            'veranstaltung': [1.0, 1.0, 1.0]
        }
        self.assertDictEqual(res, expected)

        