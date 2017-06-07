import src.spell.levenshtein as lev
from src.spell.k_gram_index_builder import k_gram_index_builder

class SpellFixer(object):
    
    def fix(self, query, k_gram_index, j):
        corrected_Query = ''
        for word in query.lower().split():
            possible_words = set()
        
        #if len(query_result) < r: set()
            bi_grams = sorted(list(set(k_gram_index_builder().get_k_grams(2, word))))
            for bi_gram in bi_grams:
                possible_words.update(k_gram_index[bi_gram])

            remaining_possible_words = []
            for possible_word in possible_words:
                #logging.debug('comparing {}, {}'.format(word, possible_word))
                possible_bi_grams = sorted(list(set(k_gram_index_builder().get_k_grams(2, possible_word))))
                
                intersect_count = k_gram_index_builder().intersect_grams(bi_grams, possible_bi_grams)
                union_count = len(possible_bi_grams) + len(bi_grams) - intersect_count
                
                jac = intersect_count / union_count
                
                if(jac > j):
                    remaining_possible_words.append(possible_word)
                    print('{} x {} -> {}'.format(word, possible_word, jac))                            
            
            
            winner = min(remaining_possible_words, key=lambda candidate: lev.levenshtein_mat(word, candidate))
            corrected_Query += (winner + ' ')
        
        return corrected_Query