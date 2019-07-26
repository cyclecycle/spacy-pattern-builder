import itertools
import networkx as nx
from spacy.tokens import Token


def annotate_token_depth(doc):
    '''Annotate token depth in the syntactic tree'''
    Token.set_extension('depth', default=None, force=True)
    for word in doc:
        depth = 0
        current_word = word
        while not current_word == current_word.head:
            depth += 1
            current_word = current_word.head
        word._.depth = depth
    return doc


def filter_by_depth(depths, tokens):
    if isinstance(depths, int):
        depths = set([depths])
    return [t for t in tokens if t._.depth in depths]


def shallowest_token(tokens):
    tokens = sort_by_depth(tokens)
    return tokens[0]


def sort_by_depth(tokens):
    return sorted(tokens, key=lambda w: (w._.depth, w.i))


def sort_by_idx(tokens):
    return sorted(tokens, key=lambda w: w.i)


def siblings(token, side=None):
    try:
        siblings = token.head.children
    except:
        return []
    if side == 'left':
        siblings = [s for s in siblings if s.i < token.i]
    elif side == 'left':
        siblings = [s for s in siblings if s.i > token.i]
    return siblings


def doc_to_nx_graph(doc):
    edges = []
    for token in doc:
        for child in token.children:
            edges.append(('{0}-{1}'.format(token.text, token.i),
                          '{0}-{1}'.format(child.text, child.i)))
    graph = nx.Graph(edges)
    return graph


def shortest_dependency_path(nx_graph, doc, source, target):
    source = '{0}-{1}'.format(source.text, source.i)
    target = '{0}-{1}'.format(target.text, target.i)
    try:
        path = nx.shortest_path(nx_graph, source=source, target=target)
    except nx.exception.NetworkXNoPath:
        path = []
    dep_path = []
    for node in path:
        idx = int(node.split('-')[-1])
        token = doc[idx]
        dep_path.append(token)
    dep_path = sorted(dep_path, key=lambda t: t._.depth)
    return dep_path


def smallest_connected_subgraph(with_tokens, doc, nx_graph=None):
    # Find root nodes
    if not nx_graph:
        nx_graph = doc_to_nx_graph(doc)
    try:
        doc[0]._.depth
    except AttributeError:
        annotate_token_depth(doc)
    min_depth = min([t._.depth for t in with_tokens])
    roots = [t for t in with_tokens if t._.depth == min_depth]
    non_roots = [t for t in with_tokens if t not in roots]
    tokens_touched = roots + non_roots
    # For each non-root token, trace paths to each root. This will touch every non-root token we're looking for
    for token in non_roots:
        for root in roots:
            path = shortest_dependency_path(nx_graph, doc, token, root)
            for t in path:
                if t not in tokens_touched:
                    tokens_touched.append(t)
    tokens_touched = sorted(tokens_touched, key=lambda t: t.i)
    # Trace paths between roots
    for root_x, root_y in itertools.combinations(roots, 2):
        path = shortest_dependency_path(nx_graph, doc, root_x, root_y)
        for t in path:
            if t not in tokens_touched:
                tokens_touched.append(t)
    return tokens_touched


def idxs_to_tokens(doc, idxs):
    return [doc[idx] for idx in idxs]


def token_idxs(tokens):
    return [t.i for t in tokens]


def de_duplicate_list(list_):
    unique_list = []
    for item in list_:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list


def list_contains_duplicates(list_):
    unique_list = de_duplicate_list(list_)
    if len(list_) > len(unique_list):
        return True
    return False


def features_are_in_pattern(features, pattern):
    for pattern_element in pattern:
        for feature in features:
            if feature not in pattern_element['PATTERN']:
                return False
    return True


def flatten_list(list_):
    return list(itertools.chain(*list_))
