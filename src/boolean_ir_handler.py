import logging
from src.boolean_query_parser import BooleanQueryParser
from src.boolean_ir import BooleanIR

class BooleanIRHandler(object):

    def handle_query(self, query, indexterms_dict, docs_dict):
        parse_result = BooleanQueryParser().parse_query(query)
        logging.info('result of parsing boolean query: {}'.format(parse_result))
        for clause in parse_result:
            for literal in clause:
                key = literal.postings
                term_postings = indexterms_dict[key]
                literal.postings = term_postings.get_postings_list()
        logging.info('replaced index terms in boolean query: {}'.format(parse_result))
        universe = list(docs_dict.keys())
        intersect_result = [BooleanIR().intersect_literals(inner_clause, universe) for inner_clause in parse_result]
        logging.info('calculated and-clauses: {}'.format(intersect_result))
        union_result = BooleanIR().union_literals(intersect_result, universe)
        logging.info('calculated or-clause: {}'.format(union_result))
        return union_result.postings