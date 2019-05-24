import itertools
from pprint import pprint
import spacy_pattern_builder.util as util
from spacy_pattern_builder.exceptions import TokensNotFullyConnectedError


DEFAULT_BUILD_PATTERN_TOKEN_FEATURE_DICT = {
    'DEP': 'dep_',
    'TAG': 'tag_'
}


def build_dependency_pattern(doc, match_tokens, token_feature_dict=DEFAULT_BUILD_PATTERN_TOKEN_FEATURE_DICT, nx_graph=None):
    '''Build a depedency pattern for use with DependencyTreeMatcher that will match the set of tokens provided in "match_tokens". This set of tokens MUST form a fully connected graph.

    Arguments:
        doc {SpaCy Doc object}
        match_tokens {list} -- Set of tokens to match with the resulting dependency pattern
        token_features {list} -- Attributes of spaCy tokens to match in the pattern
        nx_graph {NetworkX object} -- graph representing the doc dependency tree

    Returns:
        [list] -- Dependency pattern in the format consumed by SpaCy's DependencyTreeMatcher
    '''
    if not nx_graph:
        nx_graph = util.doc_to_nx_graph(doc)
    try:
        doc[0]._.depth
    except:
        util.annotate_token_depth(doc)
    smallest_connect_subgraph_tokens = util.smallest_connected_subgraph(match_tokens, nx_graph, doc)
    tokens_not_fully_connected = match_tokens != smallest_connect_subgraph_tokens
    if tokens_not_fully_connected:
        raise TokensNotFullyConnectedError('Try expanding the training example to include all tokens in between those you are trying to match. Or, try the "role-pattern" module which handles this for you.')
    token_depths = [t._.depth for t in match_tokens]
    lowest_depth = min(token_depths)
    match_tokens = sorted(match_tokens, key=lambda t: t._.depth)
    spacy_dep_pattern = []
    for i, t in enumerate(match_tokens):
        depth = t._.depth
        token_pattern = {
            name: getattr(t, feature) for name, feature in token_feature_dict.items()
        }
        depths_above = list(range(lowest_depth, depth))
        if not depths_above:  # This is the root of a pattern
            dep_pattern_element = {'SPEC': {'NODE_NAME': str(t.i)}, 'PATTERN': token_pattern}
            spacy_dep_pattern.append(dep_pattern_element)
        if depths_above:  # This is not a root token
            # Find the nearest parent node and set that as the head
            head_depth = depths_above[-1]
            head_candidates = util.filter_by_depth(head_depth, match_tokens)
            shortest_path = None
            for head_candidate in head_candidates:
                path = util.shortest_dependency_path(nx_graph, doc, t, head_candidate)
                if not shortest_path or len(path) < len(shortest_path):
                    shortest_path = path
                    head = head_candidate
            for head, child in itertools.tee(shortest_path):
                dep_pattern_element = {
                    'SPEC': {
                        'NODE_NAME': str(child.i),
                        'NBOR_NAME': str(head.i),
                        'NBOR_RELOP': '>'
                    },
                    'PATTERN': token_pattern
                }
                if dep_pattern_element not in spacy_dep_pattern:
                    spacy_dep_pattern.append(dep_pattern_element)
    return spacy_dep_pattern
