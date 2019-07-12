from spacy.matcher import DependencyMatcher


def build_matcher(vocab, pattern):
    matcher = DependencyMatcher(vocab)
    matcher.add('pattern', None, pattern)
    return matcher


def find_matches(doc, pattern):
    matcher = build_matcher(doc.vocab, pattern)
    matches = matcher(doc)
    match_list = []
    for match_id, token_idxs in matches:
        try:
            if isinstance(token_idxs[0], list):  # Matcher now returning nested list as of last spacy release
                token_idxs = token_idxs[0]
        except:
            pass
        tokens = [doc[idx] for idx in token_idxs]
        tokens = sorted(tokens, key=lambda t: t.i)
        match_list.append(tokens)
    return match_list
