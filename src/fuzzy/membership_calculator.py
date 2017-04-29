from src.ranked_posting import RankedPosting
from src.term import Term
from src.processors.or_processor import OrProcessor
from bs4.1631353 import doc


def union(posting1, posting2):
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
    return res + posting1[i1:] + posting2[i2:]

def intersect(posting1, posting2):
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


class MembershipCalculator(object):
    
    # berechnet die Korrelationsmatrix c(t,u) für Terme aus index
    # mithilfe des Jaccard-Maßes
    # die Matrix wird durch ein dict repräsentiert, welches zu jedem Term t
    # ein dict speichert, welches zu jedem Term u den Wert c(t,u) speichert
    # t ist stets kleiner als u (zur Dublettenvermeidung) ???????????
    # Ja schein sinnvoll!!!!!!!!!einseinself
    # Einträge c(t,u) werden nur explizit gespeichert, falls das 
    # Jaccard-Maß einen Wert >= threshold ergibt
    def calc_correlation_mat(self, index, threshold):
        correlation_mationary = {}
        
        for t in index.keys():                  # t can be every term
            for u in index.keys():                  # u can be every term
                if len(t.literal) < len(u.literal):     # only if t < u is c(t,u) calculated
                                                        # Ha! This saves us half a matrix!(?) - and the diagonal (special case t == u)
                    t_postings = []
                    u_postings = []
                    for entry in index[t].postings:
                        t_postings.append(entry.docID)
                    for entry in index[u].postings:
                        u_postings.append(entry.docID)
                    jaccard = len(intersect(t_postings, u_postings)) / len(union(t_postings, u_postings))
                    
                    if jaccard > threshold:     # '>' || '>=' ???
                        if t not in correlation_mationary:
                            correlation_mationary[t] = {}
                        (correlation_mationary[t])[u] = jaccard
        
        return correlation_mationary
    
    # berechnet den Fuzzy-Index aus dem booleschen Index index
    # benötigt die Korrelationsmatrix corr und eine Schwelle threshold
    # der Fuzzy-Index wird durch ein dict repräsentiert
    # das dict speichert zu jedem Term t eine RankedPosting-list
    # jedes RankedPosting speichert ein Dokument dok und den Fuzzy-Zugehörigkeitsgrad W(D,t)    # also genau anderes als in der vorlesung ;) (W(t,D)) [macht aber auch sinn]
    # nur Postings mit W(D,t) >= threshold werden gespeichert
    # ggf. später TermPostings statt list ????????????????????
    def build_fuzzy_index(self, index, corr, threshold):
        affiliation_mationary = {}
        
        '''
        for t in index.keys():          # every term
            for doc in documents:        # every document
                
                prod = 0
                for u in doc
                    prod *= 1 - (corr[t])[u]    # every term in that document
                affiliation = 1 - prod
                
                if affiliation > threshold:
                    if t not in affiliation_mationary:
                        affiliation_mationary[t] = []
                    affiliation_mationary[t] = RankedPosting(doc, affiliation)
        
        return affiliation_mationary
        '''
        
        return {'a': [RankedPosting(1, 1), RankedPosting(3, 0.6), RankedPosting(4, 0.01)],
                'b': [RankedPosting(2, 0.8), RankedPosting(4, 1)],
                'c': [RankedPosting(1, 0.01), RankedPosting(3, 0.75)]}
        