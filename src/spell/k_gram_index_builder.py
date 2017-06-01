from sklearn.feature_extraction.text import CountVectorizer 



class k_gram_index_builder(object):

    def build_k_gramm(self, k, index):
    #    k_gramm_index = {}
        
        #vectorizer = CountVectorizer(ngram_range=(k,k), analyzer='char')
        #analyzer = vectorizer.build_analyzer()
        #return analyzer(text)
        test = []
        for term in index.keys():
            for i in range(len(term.literal) - k+1):
                test.append(term.literal[i:i+k])
        return test
        
        terms = index.keys()
        return [[term.literal[i:] for i in range(k)] for term in index.keys()]
        
    #    return k_gramm_index
    
