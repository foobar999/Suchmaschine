import numpy as np

# TODO vllt. numpy oder sowas?
class HistogramBuilder(object):
    
    def show_symm_mat_hist(self, mat, num_bins):
        mat = np.triu(mat, k=0) # setze doppelte Einträge 0
        hist, bin_edges = np.histogram(mat, bins=num_bins, range=(0,1))
        np.set_printoptions(formatter={'int_kind': lambda x:' {0:d}'.format(x)})
        print('histogram {} sum {} edges {}'.format(hist, sum(hist), bin_edges))
        