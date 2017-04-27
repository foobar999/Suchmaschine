from src.fuzzy.fuzzy_posting import FuzzyPosting

class MembershipCalculator(object):
    
    # berechnet die Korrelationsmatrix c(t,u) für Terme aus index
    # mithilfe des Jaccard-Maßes
    # die Matrix wird durch ein dict repräsentiert, welches zu jedem Term t
    # ein dict speichert, welches zu jedem Term u den Wert c(t,u) speichert
    # t ist stets kleiner als u (zur Dublettenvermeidung) ???????????
    # Einträge c(t,u) werden nur explizit gespeichert, falls das 
    # Jaccard-Maß einen Wert >= threshold ergibt
    def calc_correlation_mat(self, index, threshold):
        return {'a': {'b': 0.1, 'c': 0.4}, 'b':{'c': 0.7}}
    
    # berechnet den Fuzzy-Index aus dem booleschen Index index
    # benötigt die Korrelationsmatrix corr und eine Schwelle threshold
    # der Fuzzy-Index wird durch ein dict repräsentiert
    # das dict speichert zu jedem Term t eine FuzzyPosting-list
    # jedes FuzzyPosting speichert ein Dokument dok und den Fuzzy-Zugehörigkeitsgrad W(D,t)
    # nur Postings mit W(D,t) >= threshold werden gespeichert
    # ggf. später TermPostings statt list ????????????????????
    def build_fuzzy_index(self, index, corr, threshold):
        return {'a': [FuzzyPosting(1, 0.1), FuzzyPosting(3, 0.6), FuzzyPosting(4, 0.01)],
                'b': [FuzzyPosting(2, 0.8), FuzzyPosting(4, 0.9)],
                'c': [FuzzyPosting(1, 0.01), FuzzyPosting(4, 0.75)]}
        