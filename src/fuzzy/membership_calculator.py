import logging
import numpy as np
from scipy.sparse import coo_matrix
from sklearn.metrics.pairwise import pairwise_distances
from src.ranked_posting import RankedPosting
from collections import OrderedDict
from scipy.sparse.csr import csr_matrix


class MembershipCalculator(object):
    
    # berechnet die Korrelationsmatrix c(t,u) f�r Terme aus index
    # mithilfe des Jaccard-Ma�es
    # liefert 
    #   1. c(t,u) als numpy-Matrix 
    #   2. eine Matrix docs_ocurr_mat(t,D), die zu jedem Term t zu jedem Dokument D
    #      speichert, ob er darin vorkommt (n�tig f�r build_fuzzy_index())
    # Eintr�ge c(t,u) werden nur explizit gespeichert, falls das 
    # Jaccard-Ma� einen Wert >= threshold ergibt
    def calc_correlation_mat(self, index, numdocs, threshold):
        logging.debug('keys {}'.format(index.keys())) 
        mat = []
        # erzeuge docs_ocurr_mat(t,D)
        for posting_list in index.values():
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
        #HistogramBuilder().show_symm_mat_hist(c, 10)
        
        return c, docs_ocurr_mat
        
    # berechnet den Fuzzy-Index W(D,t) aus dem booleschen Index index
    # ben�tigt:
    #   Term-Term-Korrelationsmatrix corr 
    #   Schwelle threshold (nur Postings mit W(D,t) >= threshold werden gespeichert)
    #   die Matrix docs_ocurr_mat(t,D) aus calc_correlation_mat()
    # der Fuzzy-Index wird durch ein dict repr�sentiert
    # das dict speichert zu jedem Term t eine RankedPosting-list
    # jedes RankedPosting speichert ein Dokument dok und den Fuzzy-Zugeh�rigkeitsgrad W(D,t)
    def build_fuzzy_index(self, terms, corr, docs_ocurr_mat, threshold):
        logging.debug('terms {}'.format(terms))     
        logging.debug('docs_ocurr_mat shape {}'.format(docs_ocurr_mat.shape))  
        logging.debug('corr shape {}'.format(corr.shape))         
        with np.errstate(divide='ignore'):  # log(0) = -inf -> ignoriere Warnung, da gew�nscht
            one_minus_log = np.log(1 - corr)
        one_minus_log = np.nan_to_num(one_minus_log)    # ersetze -inf durch kleinstm�glichen zul�ssigen Wert
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
        for term in affiliation_mationary:
            affiliation_mationary[term].sort(key=lambda x: x.docID)
                
        return affiliation_mationary, res_mat
