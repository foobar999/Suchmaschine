from math import floor

# TODO vllt. numpy oder sowas?
class HistogramBuilder(object):
    
    # geht von Wertebereich
    def build(self, values, num_bins):
        hist = num_bins * [0]
        for val in values:
            bin_id = min(num_bins-1, floor(num_bins * val))
            hist[bin_id] += 1
        return hist