from spacy.matcher import DependencyTreeMatcher


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
