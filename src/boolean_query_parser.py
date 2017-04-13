# -*- coding: utf-8 -*-
import re
import logging
from src.literal import Literal

class BooleanQueryParser(object):
    
    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT' 
    LBRACKET = '('
    RBRACKET = ')'
    QUOTES = '"'
    PROXIMITY = '^/[2-9]$'
    
    def parse_query(self, query):  
        logging.info('parsing query: ' + query)  
        
        if self.AND in query and self.OR not in query:
            query = self.LBRACKET + query + self.RBRACKET
            logging.debug('query has 1+ ANDs, 0 ORs -> added brackets: ' + str(query))  
        
        query_toks = re.split('(\(|\)| |")', query)
        query_toks = list(filter(str.strip, query_toks))
        logging.debug('parsed query tokens: ' + str(query_toks))  
        
        return self._generate_nested_tuple_list(query_toks)

    def _generate_nested_tuple_list(self, query_toks):
        logging.debug('parsing {} to query representation'.format(query_toks))
        
        query_toks = [tok.lower() if self._is_word(tok) else tok for tok in query_toks]
        logging.debug('{}: set words to lowercase'.format(query_toks))
        
        # ersetze in query_toks von hinten alles, was zwischen 2 '"' liegt, durch
        # eine list mit diesen Elementen
        # von vorne Ersetzen is problematisch, da dies die nachfolgenden Indizes ändert
        quotes_pos = [i for i,x in enumerate(query_toks) if x==self.QUOTES]
        logging.debug('{} as quote positions found'.format(quotes_pos))
        for i in range(len(quotes_pos)-1, -1, -2):
            pos_quote_1, pos_quote_2 = quotes_pos[i-1], quotes_pos[i]
            eles_between_quotes = query_toks[pos_quote_1+1:pos_quote_2]
            query_toks[pos_quote_1:pos_quote_2+1] = [('phrase', eles_between_quotes)]
        logging.debug('{}: result of finding phrase queries'.format(query_toks))
        
        # (a /5 B AND "hallo welt") OR F
        regex = re.compile("^/[2-9]$")
        for i in range(len(query_toks)-1, -1, -1):
            tok = query_toks[i]
            if 1 <= i <= len(query_toks)-2 and isinstance(tok, str) and regex.match(tok) != None:
                operand1, operand2 = query_toks[i-1], query_toks[i+1]
                query_toks[i-1:i+2] = [('proximity', [operand1, operand2])]
        logging.debug('{}: result of finding proximity queries'.format(query_toks))
        
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
            elif tok not in (self.OR, self.AND, self.NOT):
                is_pos_literal = i == 0 or query_toks[i - 1] != self.NOT
                literal = Literal(tok, is_pos_literal)
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
        return token not in (self.AND, self.OR, self.NOT, self.LBRACKET, self.RBRACKET, self.QUOTES) \
            and not re.match(self.PROXIMITY, token)
    
            
            
            