import rdflib
from rdflib import Literal
from rdflib.plugins.sparql.evalutils import _eval


def custom_concat(query_results, ctx, part, eval_part):
    """
    Concat 2 string and return the length as additional Length variable
    \f
    :param query_results:   An array with the query results objects
    :param ctx:             <class 'rdflib.plugins.sparql.sparql.QueryContext'>
    :param part:            Part of the query processed (e.g. Extend or BGP) <class 'rdflib.plugins.sparql.parserutils.CompValue'>
    :param eval_part:       Part currently evaluated
    :return:                the same query_results provided in input param, with additional results
    """
    argument1 = str(_eval(part.expr.expr[0], eval_part.forget(ctx, _except=part.expr._vars)))
    argument2 = str(_eval(part.expr.expr[1], eval_part.forget(ctx, _except=part.expr._vars)))
    evaluation = []
    scores = []
    concat_string = argument1 + argument2
    reverse_string = argument2 + argument1
    # Append the concatenated string to the results
    evaluation.append(concat_string)
    evaluation.append(reverse_string)
    # Append the scores for each row of results
    scores.append(len(concat_string))
    scores.append(len(reverse_string))
    # Append our results to the query_results
    for i, result in enumerate(evaluation):
        query_results.append(
            eval_part.merge({part.var: Literal(result), rdflib.term.Variable(part.var + "Length"): Literal(scores[i])})
        )
    return query_results, ctx, part, eval_part
