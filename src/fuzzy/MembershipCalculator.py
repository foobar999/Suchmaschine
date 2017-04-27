
class MembershipCalculator(object):
    
    # berechnet die Korrelationsmatrix c(t,u) f�r Terme aus index
    # mithilfe des Jaccard-Ma�es
    # die Matrix wird durch ein dict repr�sentiert, welches zu jedem Term t
    # ein dict speichert, welches zu jedem Term u den Wert c(t,u) speichert
    # t ist stets kleiner als u (zur Dublettenvermeidung) ???????????
    # Eintr�ge c(t,u) werden nur explizit gespeichert, falls das 
    # Jaccard-Ma� einen Wert >= threshold ergibt
    def calc_correlation_mat(self, index, threshold):
        pass
    
    # berechnet den Fuzzy-Index aus dem booleschen Index index
    # ben�tigt die Korrelationsmatrix corr und eine Schwelle threshold
    # der Fuzzy-Index wird durch ein dict repr�sentiert
    # das dict speichert zu jedem Term t eine list von FuzzyPosting,
    # welches jeweils ein Dokument dok und den Fuzzy-Zugeh�rigkeitsgrad W(D,t) speichert
    # nur Postings mit W(D,t) >= threashold werden gespeichert
    def build_fuzzy_index(self, index, corr, threshold):
        pass