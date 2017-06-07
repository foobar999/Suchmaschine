import logging
from sklearn.feature_extraction.text import CountVectorizer 
from collections import defaultdict


class k_gram_index_builder(object):

    # TODO REFACTOR EVERYTHING!!!

    def build_k_gram(self, k, index):
        k_gram_index = defaultdict(list)     # avoids if/else construct
        
        for term in index.keys():                               # for every term
            for i in range(len(term.literal) - k+1):            # build every k-gram
                k_gram_index[term.literal[i:i+k]].append(term.literal)  # insert into dict
        return k_gram_index
        
        
    def get_k_grams(self, k, word):
        for i in range(len(word) - k+1):                # build every k-gram
            yield word[i:i+k]


    def intersect_grams(self, grams1, grams2):
        #logging.debug("intersect of {}, {}".format(grams1, grams2))
        res = 0
        i1, i2 = 0, 0
        while i1 < len(grams1) and i2 < len(grams2):
            gram1, gram2 = grams1[i1], grams2[i2]
            if gram1 == gram2:
                res+=1
                i1 += 1
                i2 += 1
            elif gram1 < gram2:
                i1 += 1
            else:
                i2 += 1
        return res
    
    
    
    
    
    
    
    