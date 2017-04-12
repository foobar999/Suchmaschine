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
        
        quotesPos = [i for i,x in enumerate(query_toks) if x==self.QUOTES]
        print(query_toks)
        print(quotesPos)
        
        # ersetze in query_toks von hinten alles, was zwischen 2 '"' liegt, durch
        # eine list mit diesen Elementen
        # von vorne Ersetzen is problematisch, da dies die nachfolgenden Indizes ändert
        for i in range(len(quotesPos)-1, -1, -2):
            pos_quote_1, pos_quote_2 = quotesPos[i-1], quotesPos[i]
            eles_between_quotes = query_toks[pos_quote_1+1:pos_quote_2]
            query_toks[pos_quote_1:pos_quote_2+1] = [eles_between_quotes]
        print(query_toks)
        
        # (a /5 b AND "c d" /6 e) OR f
        regex = re.compile("^/[2-9]$")
        for i in range(len(query_toks)-1, -1, -1):
            tok = query_toks[i]
            if 1 <= i <= len(query_toks)-2 and isinstance(tok, str) and regex.match(tok) != None:
                operand1, operand2 = query_toks[i-1], query_toks[i+1]
                query_toks[i-1:i+2] = [(operand1, operand2)]
        print('regex result', query_toks)
        
        
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
    
            
            
            