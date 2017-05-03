import numpy as np

# TODO vllt. numpy oder sowas?
class HistogramBuilder(object):
    
    def calc_symm_mat_hist(self, mat, num_bins):
        mat = np.triu(mat, k=0) # setze doppelte Einträge 0
        return np.histogram(mat, bins=num_bins, range=(0,1))

        