import re
import logging
from src.literal import Literal

class BooleanQueryParser(object):
    
    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT' 
    LBRACKET = '('
    RBRACKET = ')'
    
    def parse_query(self, query):  
        logging.info('parsing query: ' + query)  
        
        if self.AND in query and self.OR not in query:
            query = self.LBRACKET + query + self.RBRACKET
            logging.debug('query has 1+ ANDs, 0 ORs -> added brackets: ' + str(query))  
        
        query_toks = re.split('(\(|\)| )', query)
        query_toks = list(filter(str.strip, query_toks))
        logging.debug('parsed query tokens: ' + str(query_toks))  
        
        return self._generate_nested_tuple_list(query_toks)

    def _generate_nested_tuple_list(self, query_toks):
        outer_list = []
        inner_list = None
        is_outside = True
        for i in range(0, len(query_toks)):
            tok = query_toks[i]
            if tok == self.LBRACKET:
                inner_list = []
                is_outside = False
            elif tok == self.RBRACKET:
                outer_list.append(inner_list)
                is_outside = True
            elif self._is_word(tok):
                is_pos_literal = i == 0 or query_toks[i - 1] != self.NOT
                literal = Literal(tok.lower(), is_pos_literal)
                if is_outside:
                    outer_list.append([literal])
                else:
                    inner_list.append(literal)
        
        # ersetze alle 1-Element-Klauseln durch Listen mit genau diesem Literal
        #=======================================================================
        # for i in range(0, len(outer_list)):
        #     clause = outer_list[i]
        #     if isinstance(clause, Literal):
        #         outer_list[i] = [clause]    
        #=======================================================================
            
        return outer_list
    
    def _is_word(self, token):
        return token not in (self.AND, self.OR, self.NOT, self.LBRACKET, self.RBRACKET)
    
            
            
            