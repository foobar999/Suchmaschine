import logging
from src.boolean_query_parser import BooleanQueryParser
from src.fuzzy.fuzzy_operator_dispatcher import FuzzyOperatorDispatcher
from src.fuzzy.fuzzy_posting import FuzzyPosting

class FuzzyIRHandler(object):

    def handle_query(self, query, fuzzy_index, doc_ids):
        logging.info('processing fuzzy query')
        root_node = BooleanQueryParser().parse(query)
        logging.info('result of parsing fuzzy query: {}'.format(root_node))
        self._replace_leaf_terms_by_postings(root_node, fuzzy_index)
        logging.info('replaced index terms in boolean query: {}'.format(root_node))
        universe = [FuzzyPosting(doc_id, 1) for doc_id in doc_ids]     
        return FuzzyOperatorDispatcher(universe).dispatch(root_node)

    def _replace_leaf_terms_by_postings(self, node, fuzzy_index):
        if len(node.children) == 0:
            logging.debug('searching for term {} in index'.format(node.key))
            node.key = fuzzy_index[node.key]
        for ch in node.children:
            self._replace_leaf_terms_by_postings(ch, fuzzy_index)
            