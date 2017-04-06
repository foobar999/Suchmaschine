import re
import logging
from src.tree_node import TreeNode

class BooleanQueryParser(object):

    def parse(self, query):      
        logging.debug('parsing query ' + query)  
        tok_query_whitespace = re.split("(\(|\)| )", query)
        tok_query = list(filter(str.strip, tok_query_whitespace))
        logging.debug('tokenized query without whitespace ' + str(tok_query))
        
        i = 0
        curr_node = TreeNode()
        while i < len(tok_query):
            tok = tok_query[i]
            if tok == '(':
                new_node = TreeNode(curr_node)
                curr_node.childs.append(new_node)
                curr_node = new_node
            elif tok == ')':
                curr_node = curr_node.parent
            elif tok in ('AND', 'OR'):
                # innerhalb eines Terms darf nur gleiche Junktoren vorkommen
                if curr_node.key != None and tok != curr_node.key:
                    raise SyntaxError()
                else:
                    curr_node.key = tok
            elif tok == 'NOT':
                # nimm nachfolgendes Token und füge NOT-Operation mit akt. Token
                new_node = TreeNode(curr_node, tok)
                new_node.childs.append(TreeNode(new_node, tok_query[i + 1]))
                curr_node.childs.append(new_node)
                # überspringe nachfolgendes Token
                i += 1
            else:
                curr_node.childs.append(TreeNode(curr_node, tok))    
            i += 1
        logging.debug('tokenized query without whitespace ' + str(tok_query))
                            
        return curr_node