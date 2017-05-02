import logging
import numpy as np
from scipy.sparse import coo_matrix
from sklearn.metrics.pairwise import pairwise_distances
from src.ranked_posting import RankedPosting
from collections import OrderedDict


class MembershipCalculator(object):
    
    # berechnet die Korrelationsmatrix c(t,u) f�r Terme aus index
    # mithilfe des Jaccard-Ma�es
    # die Matrix wird durch ein dict repr�sentiert, welches zu jedem Term t
    # ein dict speichert, welches zu jedem Term u den Wert c(t,u) speichert
    # t ist stets kleiner als u (zur Dublettenvermeidung) ???????????
    # Ja schein sinnvoll!!!!!!!!!einseinself
    # Eintr�ge c(t,u) werden nur explizit gespeichert, falls das 
    # Jaccard-Ma� einen Wert >= threshold ergibt
    def calc_correlation_mat(self, index, numdocs, threshold):
        
        # TODO #docs, sortierte indexterme �bergeben
        keys = [ele for ele in sorted(index)]
        mat = []
        for key in keys:
            posting_list_docs = [post.docID for post in index[key].postings]
            docs_of_key = np.zeros(numdocs, dtype=np.dtype(bool))
            docs_of_key[posting_list_docs] = 1
            mat.append(docs_of_key)
        logging.debug('keys {}'.format(keys)) 
        mat = np.reshape(mat, (len(index), numdocs))
        logging.debug('mat shape {}'.format(mat.shape))
    
        out = 1 - pairwise_distances(mat, metric = "jaccard")
        logging.debug('calculated jaccard values')
        #out = np.triu(out, k=0)  # setze Elemente in oberer Dreicksmatrix (au�erhalb Diagonale) 0
        out[out < threshold] = 0    # kicke kleine Werte
        return out, mat
    
    # berechnet den Fuzzy-Index aus dem booleschen Index index
    # ben�tigt die Korrelationsmatrix corr und eine Schwelle threshold
    # der Fuzzy-Index wird durch ein dict repr�sentiert
    # das dict speichert zu jedem Term t eine RankedPosting-list
    # jedes RankedPosting speichert ein Dokument dok und den Fuzzy-Zugeh�rigkeitsgrad W(D,t)    # also genau anderes als in der vorlesung ;) (W(t,D)) [macht aber auch sinn]
    # nur Postings mit W(D,t) >= threshold werden gespeichert
    # ggf. sp�ter TermPostings statt list ????????????????????
    def build_fuzzy_index(self, index, corr, docs_ocurr_mat, threshold):
        
        # TODO sortiertes �bergeben 
        terms = sorted([term.literal for term in index.keys()])        
        logging.debug('docs_ocurr_mat shape {}'.format(docs_ocurr_mat.shape))  
        logging.debug('corr shape {}'.format(corr.shape))         
                
        with np.errstate(divide='ignore'):  # log(0) = -inf -> ignoriere Warnung
            one_minus_log = np.log(1 - corr)
        one_minus_log = np.nan_to_num(one_minus_log)    # ersetze -inf durch kleinstm�glichen zul�ssigen Wert
        logging.debug('one_minus_log {}'.format(one_minus_log))
        # Matrizenmultiplikation
        # one_minus_log speichert log(1-c(u,t)) als Matrix zwischen allen u, t
        # docs_ocurr_mat speichert als Matrix zu jedem Term t zu jedem Dokument d, ob
        # t in d vorkommt oder nicht
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
        