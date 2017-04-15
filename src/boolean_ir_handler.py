import logging
from src.posting import Posting
from src.boolean_query_parser import BooleanQueryParser
from src.term import Term
from src.query_operator_dispatcher import QueryOperatorDispatcher

class BooleanIRHandler(object):

    def handle_query(self, query, indexterms_dict, docs_dict):
        root_node = BooleanQueryParser().parse(query)
        logging.info('result of parsing boolean query: {}'.format(root_node))
        self._replace_leaf_terms_by_postings(root_node, indexterms_dict)
        logging.info('replaced index terms in boolean query: {}'.format(root_node))
        universe = [Posting(key) for key in docs_dict.keys()]        
        dispatcher = QueryOperatorDispatcher(universe)
        #=======================================================================
        # intersect_result = [BooleanIR().intersect_literals(inner_clause, universe) for inner_clause in root_node]
        # logging.info('calculated and-clauses: {}'.format(intersect_result))
        # union_result = BooleanIR().union_literals(intersect_result, universe)
        # logging.info('calculated or-clause: {}'.format(union_result))
        #=======================================================================
        result = dispatcher.dispatch(root_node)
        return result

    def _replace_leaf_terms_by_postings(self, node, index):
        if len(node.children) == 0:
            logging.debug('searching for term {} in index'.format(node.key))
            term_postings = index[Term(node.key)]
            node.key = [tp for tp in term_postings.postings]
        for ch in node.children:
            self._replace_leaf_terms_by_postings(ch, index)