import logging
import numpy as np
from scipy.sparse import coo_matrix
from sklearn.metrics.pairwise import pairwise_distances
from src.ranked_posting import RankedPosting
from collections import OrderedDict


class MembershipCalculator(object):
    
    # berechnet die Korrelationsmatrix c(t,u) für Terme aus index
    # mithilfe des Jaccard-Maßes
    # liefert 
    #   1. c(t,u) als numpy-Matrix 
    #   2. eine Matrix docs_ocurr_mat(t,D), die zu jedem Term t zu jedem Dokument D
    #      speichert, ob er darin vorkommt (nötig für build_fuzzy_index())
    # Einträge c(t,u) werden nur explizit gespeichert, falls das 
    # Jaccard-Maß einen Wert >= threshold ergibt
    def calc_correlation_mat(self, index, numdocs, threshold):
        logging.debug('keys {}'.format(index.keys())) 
        mat = []
        # erzeuge docs_ocurr_mat(t,D)
        for term, posting_list in index.items():
            posting_list_docs = [post.docID for post in posting_list.postings]
            docs_of_key = np.zeros(numdocs, dtype=np.dtype(bool))
            docs_of_key[posting_list_docs] = 1
            mat.append(docs_of_key)
        docs_ocurr_mat = np.reshape(mat, (len(index), numdocs))
        logging.debug('mat shape {}'.format(docs_ocurr_mat.shape))
    
        c = 1 - pairwise_distances(docs_ocurr_mat, metric = "jaccard")
        logging.debug('calculated jaccard values {}'.format(c))
        #c = np.triu(out, k=0)
        c[c < threshold] = 0    # kicke kleine Werte
        return c, docs_ocurr_mat
    
    # berechnet den Fuzzy-Index W(D,t) aus dem booleschen Index index
    # benötigt:
    #   Term-Term-Korrelationsmatrix corr 
    #   Schwelle threshold (nur Postings mit W(D,t) >= threshold werden gespeichert)
    #   die Matrix docs_ocurr_mat(t,D) aus calc_correlation_mat()
    # der Fuzzy-Index wird durch ein dict repräsentiert
    # das dict speichert zu jedem Term t eine RankedPosting-list
    # jedes RankedPosting speichert ein Dokument dok und den Fuzzy-Zugehörigkeitsgrad W(D,t)
    def build_fuzzy_index(self, index, corr, docs_ocurr_mat, threshold):
        
        # TODO sortiertes übergeben 
        terms = sorted([term.literal for term in index.keys()])        
        logging.debug('docs_ocurr_mat shape {}'.format(docs_ocurr_mat.shape))  
        logging.debug('corr shape {}'.format(corr.shape))         
                
        with np.errstate(divide='ignore'):  # log(0) = -inf -> ignoriere Warnung, da gewünscht
            one_minus_log = np.log(1 - corr)
        one_minus_log = np.nan_to_num(one_minus_log)    # ersetze -inf durch kleinstmöglichen zulässigen Wert
        logging.debug('one_minus_log {}'.format(one_minus_log))
        # Matrizenmultiplikation
        # one_minus_log speichert log(1-c(u,t)) als Matrix zwischen allen u, t
        # docs_ocurr_mat speichert zu jedem Term t zu jedem Dokument d, 
        # ob t in d vorkommt oder nicht
        # eine Zeilen-Spalten-Summe nach der elementweisen Multiplikation entspricht
        # einer Anwendung der Summenformel der log. Terme (Folie 16)
        sums = one_minus_log.dot(docs_ocurr_mat)    
        logging.debug('sums {}'.format(sums))
        res_mat = 1 - np.exp(sums)
        res_mat[res_mat < threshold] = 0
        logging.debug('res_mat {}'.format(res_mat))
        sparse_res = coo_matrix(res_mat)
        affiliation_mationary = OrderedDict([(term,[]) for term in terms])
        for term_index, docID, term_doc_value in zip(sparse_res.row, sparse_res.col, sparse_res.data):
            affiliation_mationary[terms[term_index]].append(RankedPosting(docID, term_doc_value)) 
                
        return affiliation_mationary
        