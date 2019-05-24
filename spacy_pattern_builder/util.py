import itertools
import networkx as nx
from spacy.tokens import Token
from spacy.matcher import DependencyTreeMatcher


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


def smallest_connected_subgraph(with_tokens, nx_graph, doc):
    # Find root nodes
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


def build_matcher(vocab, pattern):
    matcher = DependencyTreeMatcher(vocab)
    matcher.add('pattern', None, pattern)
    return matcher


def find_matches(doc, pattern):
    matcher = build_matcher(doc.vocab, pattern)
    matches = matcher(doc)
    match_list = []
    for match_id, token_idxs in matches:
        tokens = [doc[idx] for idx in token_idxs]
        tokens = sorted(tokens, key=lambda t: t.i)
        match_list.append(tokens)
    return match_list
