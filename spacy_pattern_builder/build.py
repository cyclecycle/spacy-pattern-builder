import itertools
from pprint import pprint
import spacy_pattern_builder.util as util
from spacy_pattern_builder.exceptions import TokensNotFullyConnectedError, DuplicateTokensError, TokenNotInMatchTokensError


DEFAULT_BUILD_PATTERN_FEATURE_DICT = {
    'DEP': 'dep_',
    'TAG': 'tag_'
}


def node_name(token):
    return 'node{0}'.format(token.i)


def node_features(token, feature_dict):
    native_feature_dict = {name: feature for name, feature in feature_dict.items() if name != '_'}
    extension_feature_dict = feature_dict.get('_', None)
    node_features = {
        name: getattr(token, feature) for name, feature in native_feature_dict.items()
    }
    if extension_feature_dict:
        extension_node_features = {
            name: getattr(token._, feature) for name, feature in extension_feature_dict.items()
        }
        node_features['_'] = extension_node_features
    return node_features


def build_pattern_element(token, feature_dict, nbor=None, operator='>'):
    features = node_features(token, feature_dict)
    if not nbor:
        pattern_element = {
            'SPEC': {'NODE_NAME': node_name(token)},
            'PATTERN': features
        }
    else:
        pattern_element = {
            'SPEC': {
                'NODE_NAME': node_name(token),
                'NBOR_NAME': node_name(nbor),
                'NBOR_RELOP': operator
            },
            'PATTERN': features
        }
    return pattern_element


def build_dependency_pattern(doc, match_tokens, feature_dict=DEFAULT_BUILD_PATTERN_FEATURE_DICT, nx_graph=None):
    '''Build a depedency pattern for use with DependencyTreeMatcher that will match the set of tokens provided in "match_tokens". This set of tokens must form a fully connected graph.

    Arguments:
        doc {SpaCy Doc object}
        match_tokens {list} -- Set of tokens to match with the resulting dependency pattern
        token_features {list} -- Attributes of spaCy tokens to match in the pattern
        nx_graph {NetworkX object} -- graph representing the doc dependency tree

    Returns:
        [list] -- Dependency pattern in the format consumed by SpaCy's DependencyTreeMatcher
    '''
    # Pre-flight checks
    if not nx_graph:
        nx_graph = util.doc_to_nx_graph(doc)
    util.annotate_token_depth(doc)
    connected_tokens = util.smallest_connected_subgraph(
        match_tokens, doc, nx_graph=nx_graph)
    match_token_ids = util.token_idxs(match_tokens)
    connected_token_ids = util.token_idxs(connected_tokens)
    tokens_not_fully_connected = set(match_token_ids) != set(connected_token_ids)
    if tokens_not_fully_connected:
        raise TokensNotFullyConnectedError('Try expanding the training example to include all tokens in between those you are trying to match. Or, try the "role-pattern-nlp" module which handles this for you.')
    tokens_contain_duplicates = util.list_contains_duplicates(match_tokens)
    if tokens_contain_duplicates:
        raise DuplicateTokensError('Ensure the match_tokens is a unique list of tokens.')
    match_tokens = util.sort_by_depth(match_tokens)  # Iterate through tokens in descending depth order
    dependency_pattern = []
    root_token = match_tokens[0]
    pattern_element = build_pattern_element(root_token, feature_dict, operator='>')
    dependency_pattern.append(pattern_element)
    tokens_in_pattern = [root_token]
    non_root_tokens = match_tokens[1:]
    for i, token in enumerate(non_root_tokens):
        # If the token is a right sibling of a token already in the pattern, also add a sibling relationship.
        left_siblings = util.siblings(token, side='left')
        left_siblings_in_pattern = [t for t in left_siblings if t in tokens_in_pattern]
        if left_siblings_in_pattern:
            last_left_sibling_in_pattern = left_siblings_in_pattern[-1]
            pattern_element = build_pattern_element(
                token, feature_dict, nbor=last_left_sibling_in_pattern, operator='$--')
            dependency_pattern.append(pattern_element)
        else:  # Parent-child relation
            head = token.head
            if head not in match_tokens:
                raise TokenNotInMatchTokensError('Head token not in match_tokens. Is match_tokens fully connected?')
            pattern_element = build_pattern_element(token, feature_dict, nbor=head, operator='>')
            dependency_pattern.append(pattern_element)
        tokens_in_pattern.append(token)
    return dependency_pattern
