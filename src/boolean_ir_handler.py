from src.boolean_query_parser import BooleanQueryParser
from src.boolean_ir import BooleanIR

class BooleanIRHandler(object):

    def handle_query(self, query, indexterms_dict, docs_dict):

        parse_result = BooleanQueryParser().parse_query(query)
        print(parse_result)
        for inner_list in parse_result:
            for literal in inner_list:
                key = literal.postings
                term_postings = indexterms_dict[key]
                literal.postings = term_postings.get_postings_list()
        print(parse_result)
        universe = list(docs_dict.keys())
        and_result = [BooleanIR().intersect_literals(inner_clause, universe) for inner_clause in parse_result]
        print('ergebbbnis', and_result)
        return BooleanIR().union_literals(and_result, universe).postings