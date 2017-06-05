from sklearn.feature_extraction.text import CountVectorizer 
from collections import defaultdict


class k_gram_index_builder(object):

    def build_k_gram(self, k, index):
    #    k_gram_index = {}
        
        #vectorizer = CountVectorizer(ngram_range=(k,k), analyzer='char')
        #analyzer = vectorizer.build_analyzer()
        #return analyzer(text)
        
        
        
        k_gram_index = defaultdict(list)     # avoids if/else construct
        
        test = []
        for term in index.keys():
            for i in range(len(term.literal) - k+1):
                k_gram_index[term.literal[i:i+k]].append(term)
                print(term.literal[i:i+k])
                test.append(term.literal[i:i+k])
            print('plop----------------------------------------')
        return k_gram_index
        
        terms = index.keys()
        return [[term.literal[i:] for i in range(k)] for term in index.keys()]
        
    #    return k_gram_index
    
