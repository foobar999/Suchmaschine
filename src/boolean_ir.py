import logging

class BooleanIR(object):

    #===========================================================================
    # erwartet Postings von Dokumenten, wobei die Dokumente je Liste sortiert
    # und eindeutig sein müssen
    #===========================================================================

    def intersect(self, posting1, posting2):
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
    
    def union(self, posting1, posting2):
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
    
    def complement(self, posting, universe):
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
    
    def intersect_complement(self, posting1, posting2):
        logging.debug("union complement of {}, {}".format(posting1, posting2))
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
    
    def intersect_literals(self, literals, universe):
        logging.debug("union literals {}, universe {}".format(literals, universe))
        # TODO vllt doc in-place?
        # sortiere nach Größe der Postinglisten
        sorted_literals = sorted(literals, key=lambda literal: len(literal[0]))
        while len(sorted_literals) > 1:
            logging.debug("sorted literals {}".format(sorted_literals))
            lit1, lit2 = sorted_literals[0], sorted_literals[1]            
            is_lit1_pos, is_lit2_pos = (lit1[1] == True), (lit2[1] == True)
            res = None
            if is_lit1_pos and is_lit2_pos:
                res = (self.intersect(lit1[0], lit2[0]), True)
            elif is_lit1_pos and not is_lit2_pos:
                res = (self.intersect_complement(lit1[0], lit2[0]), True)
            elif not is_lit1_pos and is_lit2_pos:
                res = (self.intersect_complement(lit2[0], lit1[0]), True)
            else:
                res = (self.intersect(self.complement(lit1[0], universe), self.complement(lit2[0], universe)), True)
            sorted_literals[0:2] = [res]
            sorted_literals = sorted(sorted_literals, key=lambda literal: len(literal[0]))
        return sorted_literals