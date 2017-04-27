import logging
from src.boolean_query_parser import BooleanQueryParser
from src.fuzzy.fuzzy_operator_dispatcher import FuzzyOperatorDispatcher
from src.fuzzy.fuzzy_posting import FuzzyPosting

class FuzzyIRHandler(object):

    def handle_query(self, query, fuzzy_index, docs_dict):
        logging.info('processing fuzzy query')
        root_node = BooleanQueryParser().parse(query)
        logging.info('result of parsing fuzzy query: {}'.format(root_node))
        self._replace_leaf_terms_by_postings(root_node, fuzzy_index)
        logging.info('replaced index terms in boolean query: {}'.format(root_node))
        universe = [FuzzyPosting(key, None) for key in docs_dict.keys()]     
        return FuzzyOperatorDispatcher().dispatch(root_node, universe)

    def _replace_leaf_terms_by_postings(self, node, fuzzy_index):
        if len(node.children) == 0:
            logging.debug('searching for term {} in index'.format(node.key))
            term_postings = fuzzy_index[node.key]
            node.key = [tp for tp in term_postings.postings]
        for ch in node.children:
            self._replace_leaf_terms_by_postings(ch, fuzzy_index)
            