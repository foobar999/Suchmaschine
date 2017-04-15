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
        return dispatcher.dispatch(root_node)

    def _replace_leaf_terms_by_postings(self, node, index):
        if len(node.children) == 0:
            logging.debug('searching for term {} in index'.format(node.key))
            term_postings = index[Term(node.key)]
            node.key = [tp for tp in term_postings.postings]
        for ch in node.children:
            self._replace_leaf_terms_by_postings(ch, index)