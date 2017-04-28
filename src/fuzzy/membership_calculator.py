from src.ranked_posting import RankedPosting

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
    # das dict speichert zu jedem Term t eine RankedPosting-list
    # jedes RankedPosting speichert ein Dokument dok und den Fuzzy-Zugehörigkeitsgrad W(D,t)
    # nur Postings mit W(D,t) >= threshold werden gespeichert
    # ggf. später TermPostings statt list ????????????????????
    def build_fuzzy_index(self, index, corr, threshold):
        return {'a': [RankedPosting(1, 1), RankedPosting(3, 0.6), RankedPosting(4, 0.01)],
                'b': [RankedPosting(2, 0.8), RankedPosting(4, 1)],
                'c': [RankedPosting(1, 0.01), RankedPosting(3, 0.75)]}
        