
class BooleanIR(object):

    def intersect(self, posting1, posting2):
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