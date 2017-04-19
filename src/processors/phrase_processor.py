import logging
from src.processors.query_operator_processor import QueryOperatorProcessor
from src.posting import Posting

class PhraseProcessor(QueryOperatorProcessor):
    
    def __init__(self, dispatcher):
        super().__init__(dispatcher)
    
    def process(self, nodes, universe):
        nodes_postings = self._process_all_nodes(nodes) 
        logging.debug('processing phrase operator on postings {}, universe{}'.format(nodes_postings, universe))
        assert len(nodes) >= 1
        
        ret = []
        # index of current posting per term
        docs = [0] * len(nodes_postings)
        
        while self.doc_valid(docs, nodes_postings):
            posts = [nodes_postings[i][docs[i]] for i in range(0,len(docs))]
            logging.debug('posts: {}'.format(posts))
            docIDs = [nodes_postings[i][docs[i]].docID for i in range(0,len(posts))]

            # all elements equal?
            if docIDs[1:] == docIDs[:-1]:
                
                found_positions = []
                
                docID = docIDs[0]
                logging.debug('all terms occuring in document {}'.format(docID))
                poses = [0] * len(nodes_postings)
                while self.pos_valid(poses, posts):
                    text_poses = [posts[i].positions[poses[i]] for i in range(0,len(poses))]
                    text_poses_reduced = [text_poses[i]-i for i in range(0, len(text_poses))]
                    if text_poses_reduced[1:] == text_poses_reduced[:-1]:
                        text_pos = text_poses[0]
                        logging.debug('phrase found in doc {} at position {}'.format(docID, text_pos))
                        found_positions.append(text_pos)
                        poses = [pos+1 for pos in poses]
                        
                    for i in range(0, len(text_poses)):
                        if text_poses[i] < max(text_poses_reduced):
                            poses[i] += 1
                
                if len(found_positions) > 0:
                    ret.append(Posting(docID, found_positions))
                
                docs = [doc+1 for doc in docs]
                
            # erhöhe die Zeiger, deren docIDs nicht dem Maximum entsprechen
            else:
                for i in range(0, len(docIDs)):
                    if docIDs[i] < max(docIDs):
                        docs[i] += 1
                    
        return ret
        
    def doc_valid(self, docs, nodes_postings):
        for i in range(0,len(nodes_postings)):
            if(docs[i] >= len(nodes_postings[i])):
                return False
        return True
        
        
    def pos_valid(self, poses, posts):
        for i in range(0,len(posts)):
            if(poses[i] >= len(posts[i].positions)):
                return False
        return True
    
        