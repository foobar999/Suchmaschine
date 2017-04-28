from math import floor

# TODO vllt. numpy oder sowas?
class HistogramBuilder(object):
    
    def build_corr_hist(self, corr, index_terms, num_bins):
        corr_values = []
        for t1 in range(0, len(index_terms)):
            for t2 in range(t1 + 1, len(index_terms)):
                term1, term2 = index_terms[t1], index_terms[t2]
                corr_value = corr.get(term1).get(term2)
                corr_values.append(corr_value or 0) # setzt Wert auf 0, falls corr_value None
        
        return self._build(corr_values, num_bins)
    
    def build_fuzzy_index_hist(self, fuzzy_index, num_bins):
        fuzzy_index_values = []
        number_of_documents = 6 # TODO auf Länge von docsDict ändern
        for posting_list in fuzzy_index.values():
            fuzzy_index_values.extend([0] * (number_of_documents - len(posting_list))) # zähle fehlende Postings als 0en
            fuzzy_index_values.extend([posting.mem_val for posting in posting_list])
        
        return self._build(fuzzy_index_values, num_bins)
    
    # geht von Wertebereich 0...1 aus
    def _build(self, values, num_bins):
        hist = num_bins * [0]
        for val in values:
            bin_id = min(num_bins-1, floor(num_bins * val))
            hist[bin_id] += 1
        return hist
    
    