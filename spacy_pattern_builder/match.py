from spacy.matcher import DependencyMatcher


def build_matcher(vocab, pattern):
    matcher = DependencyMatcher(vocab)
    matcher.add('pattern', None, pattern)
    return matcher


def find_matches(doc, pattern):
    matcher = build_matcher(doc.vocab, pattern)
    # print(doc, pattern)
    matches = matcher(doc)
    match_list = []
    for match_id, match_trees in matches:
        for token_idxs in match_trees:
            tokens = [doc[idx] for idx in token_idxs]
            tokens = sorted(tokens, key=lambda t: t.i)
            match_list.append(tokens)
    return match_list
