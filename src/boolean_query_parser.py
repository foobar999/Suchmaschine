import re
import logging
from src.tree_node import TreeNode
from src.query_operator import QueryOp

class BooleanQueryParser(object):
   
    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT' 
    LBRACKET = '('
    RBRACKET = ')'
    QUOTES = '"'
    PROXIMITY = '^/[1-9]$'

    def _is_proximity(self, tok):
        return re.match(self.PROXIMITY, tok) != None

    def _is_word(self, tok):
        return tok not in (self.AND, self.OR, self.NOT, self.LBRACKET, self.RBRACKET, self.QUOTES) and not self._is_proximity(tok)
        
    #def _verifiy(self, node):
    #    return all([ch.parent is node and self._verifiy(ch) for ch in node.children])
    
    def parse(self, query):
        query_toks = re.split('(\(|\)| |")', query)
        query_toks = list(filter(str.strip, query_toks))
        logging.debug('parsed query tokens: ' + str(query_toks))  
        
        for i in range(0, len(query_toks)):
            tok = query_toks[i]
            query_toks[i] = TreeNode(tok.lower(), []) if self._is_word(tok) else tok
        logging.debug('replaced terminals by nodes: {}'.format(query_toks)) 
             
        quotes_pos = [i for i,x in enumerate(query_toks) if x == self.QUOTES]        
        logging.debug('{} as quote positions found'.format(quotes_pos))
        for i in range(len(quotes_pos)-1, -1, -2):
            pos_quote_1, pos_quote_2 = quotes_pos[i-1], quotes_pos[i]
            eles_between_quotes = query_toks[pos_quote_1+1:pos_quote_2]
            new_node = TreeNode(QueryOp.PHRASE, eles_between_quotes)
            new_node.set_self_as_parent()
            query_toks[pos_quote_1:pos_quote_2+1] = [new_node]
        logging.debug('{}: result of finding phrase queries'.format(query_toks))
                
        regex = re.compile(self.PROXIMITY)
        for i in range(len(query_toks)-1, -1, -1):
            tok = query_toks[i]
            if 1 <= i <= len(query_toks)-2 and isinstance(tok, str) and regex.match(tok) != None:
                operand1, operand2 = query_toks[i-1], query_toks[i+1]
                new_node = TreeNode(QueryOp.PROXIMITY(int(tok[1])), [operand1, operand2])
                new_node.set_self_as_parent()
                query_toks[i-1:i+2] = [new_node]
        logging.debug('{}: result of finding proximity queries'.format(query_toks))
        
        root = TreeNode()
        curr_node = root
        for i in range(0, len(query_toks)):
            tok = query_toks[i]
            logging.debug('processing token {}'.format(tok))
            if tok == self.LBRACKET:
                new_node = TreeNode(None, [], curr_node)
                curr_node.children.append(new_node)
                curr_node = new_node
            elif tok == self.RBRACKET:
                curr_node = curr_node.parent
            elif tok in (self.AND, self.OR):
                op = QueryOp.AND if tok == self.AND else QueryOp.OR
                assert curr_node.key == None or curr_node.key == op
                curr_node.key = op
            elif tok != self.NOT:
                assert isinstance(tok, TreeNode)
                new_node = tok
                if i > 0 and query_toks[i-1] == self.NOT:
                    new_node = TreeNode(QueryOp.NOT, [new_node])
                    new_node.set_self_as_parent()
                new_node.parent = curr_node
                curr_node.children.append(new_node)
            
        if root.key == None:
            root = root.children[0]
            root.parent = None
            
        root.set_self_as_parent_recursively()
        return root
    