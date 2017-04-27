
class MembershipCalculator(object):
    
    # berechnet die Korrelationsmatrix c(t,u) für Terme aus index
    # mithilfe des Jaccard-Maßes
    # die Matrix wird durch ein dict repräsentiert, welches zu jedem Term t
    # ein dict speichert, welches zu jedem Term u den Wert c(t,u) speichert
    # t ist stets kleiner als u (zur Dublettenvermeidung) ???????????
    # Einträge c(t,u) werden nur explizit gespeichert, falls das 
    # Jaccard-Maß einen Wert >= threshold ergibt
    def calc_correlation_mat(self, index, threshold):
        pass
    
    # berechnet den Fuzzy-Index aus dem booleschen Index index
    # benötigt die Korrelationsmatrix corr und eine Schwelle threshold
    # der Fuzzy-Index wird durch ein dict repräsentiert
    # das dict speichert zu jedem Term t eine list von FuzzyPosting,
    # welches jeweils ein Dokument dok und den Fuzzy-Zugehörigkeitsgrad W(D,t) speichert
    # nur Postings mit W(D,t) >= threashold werden gespeichert
    def build_fuzzy_index(self, index, corr, threshold):
        pass