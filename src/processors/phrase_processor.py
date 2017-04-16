import logging
from src.processors.query_operator_processor import QueryOperatorProcessor
from src.posting import Posting

class PhraseProcessor(QueryOperatorProcessor):
    
    def __init__(self, dispatcher):
        super().__init__(dispatcher)
    
    # "a b"
    def process(self, nodes, universe):
        nodes_postings = self._process_all_nodes(nodes) 
        logging.debug('processing phrase operator on postings {}, universe{}'.format(nodes_postings, universe))
        assert 1 <= len(nodes) <= 3
        # TODO 2er-Phrases
        
        ret = []
        postings1, postings2, postings3 = nodes_postings[0], nodes_postings[1], nodes_postings[2]
        doc1, doc2, doc3 = 0, 0, 0
        while doc1 < len(postings1) and doc2 < len(postings2) and doc3 < len(postings3):
            post1, post2, post3 = postings1[doc1], postings2[doc2], postings3[doc3]
            docID1, docID2, docID3 = post1.docID, post2.docID, post3.docID
            if docID1 == docID2 == docID3:
                logging.debug('all terms occuring in document {}'.format(docID1))
                pos1, pos2, pos3 = 0, 0, 0
                while pos1 < len(post1.positions) and pos2 < len(post2.positions) and pos3 < len(post3.positions):
                    text_pos1, text_pos2, text_pos3 = post1.positions[pos1], post2.positions[pos2], post3.positions[pos3]
                    if text_pos1 == text_pos2-1 == text_pos3-2:
                        logging.debug('phrase found in doc {} at position {}'.format(docID1, text_pos1))
                        ret.append(Posting(docID1, [text_pos1]))
                        pos1, pos2, pos3 = pos1+1, pos2+1, pos3+1
                    if text_pos1 < max(text_pos1, text_pos2-1, text_pos3-2):
                        pos1 += 1
                    if text_pos2 < max(text_pos1, text_pos2-1, text_pos3-2):
                        pos2 += 1
                    if text_pos3 < max(text_pos1, text_pos2-1, text_pos3-2):
                        pos3 += 1
                
                doc1, doc2, doc3 = doc1+1, doc2+1, doc3+1
            # erhöhe die Zeiger, deren docIDs nicht dem Maximum entsprechen
            if docID1 < max(docID1, docID2, docID3):
                doc1 += 1
            if docID2 < max(docID1, docID2, docID3):
                doc2 += 1
            if docID3 < max(docID1, docID2, docID3):
                doc3 += 1
        
        return ret
        
        """
        i2, i3 = 0, 0
        post1, post2, post3 = nodes_postings[0], nodes_postings[3], nodes_postings[2]
        for i1 in range(0, len(nodes)):
            id1 = post1[i1].docID
            while pos
        """