from sklearn.feature_extraction.text import CountVectorizer 
from collections import defaultdict


class k_gram_index_builder(object):

    def build_k_gram(self, k, index):
        k_gram_index = defaultdict(list)     # avoids if/else construct
        
        for term in index.keys():                               # for every term
            for i in range(len(term.literal) - k+1):            # build every k-gram
                k_gram_index[term.literal[i:i+k]].append(term)  # insert into dict
        return k_gram_index
        
