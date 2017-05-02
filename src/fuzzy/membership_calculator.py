from src.ranked_posting import RankedPosting
from src.term import Term
from src.processors.or_processor import OrProcessor
from collections import OrderedDict, defaultdict
import numpy as np
from scipy.sparse import csr_matrix, find, coo_matrix
from sklearn.metrics.pairwise import pairwise_distances
import logging

def union(posting1, posting2):
    res = []
    i1, i2 = 0, 0
    while i1 < len(posting1) and i2 < len(posting2):
        doc1, doc2 = posting1[i1], posting2[i2]
        if doc1 == doc2:
            res.append(doc1)
            i1 += 1
            i2 += 1
        elif doc1 < doc2:
            res.append(doc1)
            i1 += 1
        else:
            res.append(doc2)
            i2 += 1
    return res + posting1[i1:] + posting2[i2:]

def intersect_cnt(posting1, posting2):
    #res = []
    res = 0
    i1, i2 = 0, 0
    while i1 < len(posting1) and i2 < len(posting2):
        doc1, doc2 = posting1[i1], posting2[i2]
        if doc1 == doc2:
            #res.append(doc1)
            res += 1
            i1 += 1
            i2 += 1
        elif doc1 < doc2:
            i1 += 1
        else:
            i2 += 1
    return res


class MembershipCalculator(object):
    
    # berechnet die Korrelationsmatrix c(t,u) für Terme aus index
    # mithilfe des Jaccard-Maßes
    # die Matrix wird durch ein dict repräsentiert, welches zu jedem Term t
    # ein dict speichert, welches zu jedem Term u den Wert c(t,u) speichert
    # t ist stets kleiner als u (zur Dublettenvermeidung) ???????????
    # Ja schein sinnvoll!!!!!!!!!einseinself
    # Einträge c(t,u) werden nur explizit gespeichert, falls das 
    # Jaccard-Maß einen Wert >= threshold ergibt
    def calc_correlation_mat(self, index, numdocs, threshold):
        
        # TODO #docs, sortierte indexterme übergeben
        keys = [ele for ele in sorted(index)]
        mat = []
        for key in keys:
            posting_list_docs = [post.docID for post in index[key].postings]
            docs_of_key = np.zeros(numdocs, dtype=np.dtype(bool))
            docs_of_key[posting_list_docs] = 1
            #print(docs_of_key)
            mat.append(docs_of_key)
        logging.debug('keys {}'.format(keys)) 
        mat = np.reshape(mat, (len(index), numdocs))
        logging.debug('mat shape {}'.format(mat.shape))
        
    #===========================================================================
    #     csr = csr_matrix(mat).astype(bool).astype(int)
    # 
    #     csr_rownnz = csr.getnnz(axis=1)
    #     print('csr_rownnz', csr_rownnz, len(csr_rownnz))
    #     intrsct = csr.dot(csr.T)
    # 
    #     nnz_i = np.repeat(csr_rownnz, intrsct.getnnz(axis=1))
    #     print('nnz', nnz_i, len(nnz_i))
    #     unions = nnz_i + csr_rownnz[intrsct.indices] - intrsct.data
    #     dists = 1.0 - intrsct.data / unions
    # 
    #     mask = (dists > 0) & (dists >= threshold)
    #     data = dists[mask]
    #     
    #     indices = intrsct.indices[mask]
    # 
    #     rownnz = np.add.reduceat(mask, intrsct.indptr[:-1])
    #     indptr = np.r_[0, np.cumsum(rownnz)]
    # 
    #     out = csr_matrix((data, indices, indptr), intrsct.shape)
    #     
    #     print(out.shape)
    #===========================================================================
    
        out = 1 - pairwise_distances(mat, metric = "jaccard")
        logging.debug('calculated jaccard values')
        #out = np.triu(out, k=0)  # setze Elemente in oberer Dreicksmatrix (außerhalb Diagonale) 0
        out[out < threshold] = 0    # kicke kleine Werte
        #return OrderedDict([(keys[i],{keys[j]:val for j,val in enumerate(row) if val}) for i,row in enumerate(out)])
        #return csr_matrix(out), mat
        return out, mat
    
        ret = OrderedDict()
        for term in keys:
            ret[term] = {}
        rows, cols, vals = find(out)
        
        print('nonzero', len(rows), len(cols), len(vals))
        for i,j,v in zip(rows,cols,vals):
            #if i < j:
                term1, term2 = keys[i], keys[j]
                ret[term1][term2] = v
        for i in range(0, 100):
            for j in range(0, 100):
                if out[i,j] != out[j,i]:
                    print(i, j, out[i,j], out[j,i])
        
        #print(ret)
        
        return ret
        
#===============================================================================
#         correlation_mationary = OrderedDict()
# 
#         index_list = [(tup[0], [ele for ele in tup[1].postings]) for tup in index.items()]
#         #index_list = [(tup[0], np.array([ele.docID for ele in tup[1].postings])) for tup in index.items()]
#         index_list.sort(key=lambda x: x[0])
#         #print(index_list)         
#         
#         print('iterating ', [t[0] for t in index_list])
#         
#         for it in range(0, len(index_list)):
#             t = index_list[it][0]               # t can be every term
#             t_postings = index_list[it][1]
#             t_res = {}
#             for iu in range(it + 1, len(index_list)):
#                 u = index_list[iu][0]               # u can be every term
#                 u_postings = index_list[iu][1]
#                 
#                 #if len(t.literal) < len(u.literal):     # only if t < u is c(t,u) calculated
#                                                         # Ha! This saves us half a matrix!(?) - and the diagonal (special case t == u)
# 
#                 #for entry in index[t].postings:
#                 #    t_postings.append(entry.docID)
#                 #for entry in index[u].postings:
#                 #    u_postings.append(entry.docID)
#                 #jaccard = len(intersect(t_postings, u_postings)) / len(union(t_postings, u_postings))
#                 int_len = intersect_cnt(t_postings, u_postings)
#                 jaccard = int_len / (len(t_postings) + len(u_postings) - int_len)
#                 
#                 if jaccard > threshold:     # '>' || '>=' ???
#                     #if t not in correlation_mationary:
#                     #    correlation_mationary[t] = {}
#                     #(correlation_mationary[t])[u] = jaccard
#                     t_res[u] = jaccard
#             correlation_mationary[t] = t_res
#         #print(len(correlation_mationary), len(index_list))
#             
#         return correlation_mationary
#===============================================================================
    
    # berechnet den Fuzzy-Index aus dem booleschen Index index
    # benötigt die Korrelationsmatrix corr und eine Schwelle threshold
    # der Fuzzy-Index wird durch ein dict repräsentiert
    # das dict speichert zu jedem Term t eine RankedPosting-list
    # jedes RankedPosting speichert ein Dokument dok und den Fuzzy-Zugehörigkeitsgrad W(D,t)    # also genau anderes als in der vorlesung ;) (W(t,D)) [macht aber auch sinn]
    # nur Postings mit W(D,t) >= threshold werden gespeichert
    # ggf. später TermPostings statt list ????????????????????
    def build_fuzzy_index(self, index, corr, docs_ocurr_mat, threshold):
    #def build_fuzzy_index(self, docmat, corr, index, threshold):
        
        # TODO sortiertes übergeben 
        terms = sorted([term.literal for term in index.keys()])
        
        #=======================================================================
        # docs_ocurr_mat = docs_ocurr_mat.T
        # logging.debug('docs_ocurr_mat shape {}'.format(docs_ocurr_mat.shape))  
        # logging.debug('corr shape {}'.format(corr.shape))         
        # 
        # for tindex, tcorrelations in enumerate(corr):
        #     t = terms[tindex].literal
        #     affiliation_mationary[t] = []
        #     for docid, doc_occuring_terms in enumerate(docs_ocurr_mat):
        #         
        #         doc_occuring_terms_corrs = np.multiply(tcorrelations, doc_occuring_terms)
        #         res = 1 - np.prod(1 - doc_occuring_terms_corrs)
        #         if res >= threshold:
        #             affiliation_mationary[t].append(RankedPosting(docid, res))
        #=======================================================================
        
        logging.debug('docs_ocurr_mat shape {}'.format(docs_ocurr_mat.shape))  
        logging.debug('corr shape {}'.format(corr.shape))         
                
        with np.errstate(divide='ignore'):  # log(0) = -inf -> ignoriere Warnung
            one_minus_log = np.log(1 - corr)
        one_minus_log = np.nan_to_num(one_minus_log)    # ersetze -inf durch kleinstmöglichen zulässigen Wert
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
        
        #=======================================================================
        # 
        # for t in index.keys():          # every term
        #     for doc in range(0, numdocs):        # every document
        #         
        #         prod = 0
        #         for u in doc:
        #             prod *= 1 - (corr[t])[u]    # every term in that document
        #         affiliation = 1 - prod
        #         
        #         if affiliation > threshold:
        #             if t not in affiliation_mationary:
        #                 affiliation_mationary[t] = []
        #             affiliation_mationary[t] = RankedPosting(doc, affiliation)
        # 
        # return affiliation_mationary
        # 
        # 
        # return {'a': [RankedPosting(1, 1), RankedPosting(3, 0.6), RankedPosting(4, 0.01)],
        #         'b': [RankedPosting(2, 0.8), RankedPosting(4, 1)],
        #         'c': [RankedPosting(1, 0.01), RankedPosting(3, 0.75)]}
        #=======================================================================
        
        