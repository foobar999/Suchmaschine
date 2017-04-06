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
                curr_node.key = tok
            elif tok == 'NOT':
                # nimm nachfolgendes Token und f�ge NOT-Operation mit akt. Token
                new_node = TreeNode(curr_node, tok)
                new_node.childs.append(TreeNode(new_node, tok_query[i + 1]))
                curr_node.childs.append(new_node)
                # �berspringe nachfolgendes Token
                i += 1
            else:
                curr_node.childs.append(TreeNode(curr_node, tok))    
            i += 1
        logging.debug('tokenized query without whitespace ' + str(tok_query))
                            
        return curr_node
    
    def parse2(self, query):  
        logging.debug('parsing query ' + query)  
        
        query_toks = re.split("(\(|\)| )", query)
        query_toks = list(filter(str.strip, query_toks))
        logging.debug('parsed query tokens ' + str(query_toks))  
        
        tuple_toks = self._replace_words_by_tuples(query_toks)       
        logging.debug('replaced words by tuples ' + str(tuple_toks))
        
        nested_toks = self._replace_quotes_by_nested_lists(tuple_toks)
        logging.debug('replaced quotes by nested lists ' + str(nested_toks))      
          
        return nested_toks
    
    def _is_word(self, token):
        return token not in ('AND', 'OR', 'NOT', '(', ')')
    
    def _replace_words_by_tuples(self, query_toks):
        tuple_toks = []
        for i in range(0, len(query_toks)):
            tok = query_toks[i]
            if self._is_word(tok):
                is_pos_literal = i == 0 or query_toks[i-1] != 'NOT'
                tuple_toks.append((tok, is_pos_literal))
            elif tok not in ('AND', 'OR', 'NOT'):
                tuple_toks.append(tok)   
        return tuple_toks
    
    def _replace_quotes_by_nested_lists(self, tuple_toks):
        nested_toks = []
        i = 0
        while i < len(tuple_toks):
            tok = tuple_toks[i]
            if tok == '(':
                inner_array = []
                j = i + 1
                while j < len(tuple_toks) and tuple_toks[j] != ')':
                    inner_array.append(tuple_toks[j])
                    j += 1
                nested_toks.append(inner_array)
                i = j
            i += 1
        return nested_toks
                
                