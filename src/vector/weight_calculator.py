from math import log

class WeightCalculator(object):
                    
    def calc_wt_f_d(self, term_freq, doc_freq, numdocs):
        return 0 if term_freq == 0 else (1 + log(term_freq, 10)) * log(numdocs / doc_freq, 10) 