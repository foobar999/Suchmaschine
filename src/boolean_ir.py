import logging
import bisect
from src.literal import Literal    

class BooleanIR(object):

    #===========================================================================
    # erwartet Postings von Dokumenten, wobei die Dokumente je Liste sortiert
    # und eindeutig sein müssen
    #===========================================================================
    
    def union_literals(self, literals, universe):
        logging.debug("union literals {}, universe {}".format(literals, universe))
        current_res = Literal([], True)
        for literal in literals:
            logging.debug("current union result: {}".format(current_res))        
            current_res = self._union_2_literals(universe, current_res, literal)      
            # falls Universum das Zwischenergebnis => gib es direkt zurück    
            if len(current_res.postings) == len(universe):
                logging.debug("returning universe immediately")
                break          
        return current_res
    
    def intersect_literals(self, literals, universe):
        logging.debug("intersect literals {}, universe {}".format(literals, universe))
        if len(literals) == 0:
            return Literal([], True)
        sorted_literals = sorted(literals)
        logging.debug("sorted intersect literals {}".format(sorted_literals, universe))
        current_res = sorted_literals[0]
        
        # füge Komplement hier durch, falls nur 1 Element, da  kein "Partner" vorhanden
        if len(sorted_literals) == 1 and not current_res.is_positive:
            current_res = Literal(self._complement(current_res.postings, universe), True)
        
        for i in range(1, len(sorted_literals)):
            literal = sorted_literals[i]
            logging.debug("current intersect result: {}".format(current_res))        
            current_res = self._intersect_2_literals(universe, current_res, literal)      
            # falls leere Menge das Zwischenergebnis => gib es direkt zurück    
            if len(current_res.postings) == 0:
                logging.debug("returning empty postings immediately")
                break
    
        return current_res
    
    def _union_2_literals(self, universe, lit1, lit2):
        postings1 = lit1.postings if lit1.is_positive else self._complement(lit1.postings, universe)
        postings2 = lit2.postings if lit2.is_positive else self._complement(lit2.postings, universe)
        return Literal(self._union(postings1, postings2), True)
    
    def _intersect_2_literals(self, universe, lit1, lit2):
        if lit1.is_positive and lit2.is_positive:
            return Literal(self._intersect(lit1.postings, lit2.postings), True)
        elif lit1.is_positive and not lit2.is_positive:
            return Literal(self._intersect_complement(lit1.postings, lit2.postings), True)
        elif not lit1.is_positive and lit2.is_positive:
            return Literal(self._intersect_complement(lit2.postings, lit1.postings), True)
        else:
            complement1 = self._complement(lit1.postings, universe)
            complement2 = self._complement(lit2.postings, universe)
            return Literal(self._intersect(complement1, complement2), True)
    
    def _intersect(self, posting1, posting2):
        logging.debug("intersect of {}, {}".format(posting1, posting2))        
        res = []
        i1, i2 = 0, 0
        while i1 < len(posting1) and i2 < len(posting2):
            doc1, doc2 = posting1[i1], posting2[i2]
            if doc1 == doc2:
                res.append(doc1)
                i1 += 1
                i2 += 1
            elif doc1 < doc2:
                i1 += 1
            else:
                i2 += 1
        return res
    
    def _union(self, posting1, posting2):
        logging.debug("union of {}, {}".format(posting1, posting2))    
        res = []
        i1, i2 = 0, 0
        while i1 < len(posting1) and i2 < len(posting2):
            doc1, doc2 = posting1[i1], posting2[i2]
            if doc1 == doc2:
                res.append(doc1)
                i1 += 1
                i2 += 1
            elif doc1 < doc2:
                res.append(doc1)
                i1 += 1
            else:
                res.append(doc2)
                i2 += 1
        # hänge den Rest der Liste an, bei der i nicht am Ende ist
        return res + posting1[i1:] + posting2[i2:]
    
    def _complement(self, posting, universe):
        logging.debug("complement of {}, universe {}".format(posting, universe))
        res = []
        ip, iu = 0, 0
        while ip < len(posting):
            docp, docu = posting[ip], universe[iu]
            if docu == docp:
                ip += 1
                iu += 1
            if docu < docp:
                res.append(docu)
                iu += 1
        return res + universe[iu:]
    
    # posting1 positiv, posting2 negativ
    def _intersect_complement(self, posting1, posting2):
        logging.debug("intersect_complement of {}, {}".format(posting1, posting2))
        res = []
        i1, i2 = 0, 0
        while i1 < len(posting1) and i2 < len(posting2):
            doc1, doc2 = posting1[i1], posting2[i2]
            if doc1 == doc2:
                i1 += 1
                i2 += 1
            elif doc1 < doc2:
                res.append(doc1)
                i1 += 1
            else:
                i2 += 1
        return res + posting1[i1:]
        