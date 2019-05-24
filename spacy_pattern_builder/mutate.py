'''Generate pattern variations

Provide the ability to generate pattern variations using:
    - different combinations of features
        - throughout the whole pattern
        - within each element of the pattern
    - using different combinations of features across the whole pattern
    - using dirre
'''

from spacy_pattern_builder.build import build_pattern_element, DEFAULT_BUILD_PATTERN_FEATURE_DICT


def node_name_to_token_idx(node_name):
    token_idx = int(node_name.split('node')[1])
    return token_idx

# def generate_variations(dependency_pattern, doc, feature_combinations, level='global'):
#     if level not in GENERATE_VARIATIONS_LEVEL_CHOICES:
#         raise
#     if level == 'global':


def pattern_element_node_token(pattern_element, doc):
    node_name = pattern_element['SPEC']['NODE_NAME']
    token_idx = node_name_to_token_idx(node_name)
    token = doc[token_idx]
    return token


def pattern_element_nbor_token(pattern_element, doc):
    try:
        nbor_name = pattern_element['SPEC']['NBOR_NAME']
        token_idx = node_name_to_token_idx(nbor_name)
        token = doc[token_idx]
        return token
    except KeyError:
        return None


def pattern_element_for_each_feature_combination(token, feature_combinations,
    feature_dict, nbor=None):
    for features in feature_combinations:
        variation_feature_dict = {k: v for k, v in feature_dict.items() if k in features}
        if nbor:
            new_pattern_element = build_pattern_element(token, variation_feature_dict, nbor=nbor)
        else:
            new_pattern_element = build_pattern_element(token, variation_feature_dict)
        yield new_pattern_element


def pattern_for_each_feature_combination(doc, feature_combinations, feature_dict):
    for features in feature_combinations:
        variation_feature_dict = {k: v for k, v in feature_dict.items() if k in features}
        dependency_pattern = build_dependency_pattern()
        new_dependency_pattern = []
        variation_feature_dict = {k: v for k, v in feature_dict.items() if k in features}
        for pattern_element in dependency_pattern:
            node_name = pattern_element['SPEC']['NODE_NAME']
            token_idx = node_name_to_token_idx(node_name)
            token = doc[token_idx]
            features = node_features(token, variation_feature_dict)
            new_spec = {'SPEC': pattern_element['SPEC'], 'PATTERN': features}
            new_dependency_pattern.append(new_spec)
        variations.append(new_dependency_pattern)
    return variations


def pattern_for_each_feature_combination_within_elements():


def global_feature_substitution(dependency_pattern, doc, feature_combinations, feature_dict):
    # Yield a pattern for each combination of features in feature_combinations.  Generates N = len(feature_combinations) variations.
    variations = []
    for features in feature_combinations:
        new_dependency_pattern = []
        variation_feature_dict = {k: v for k, v in feature_dict.items() if k in features}
        for pattern_element in dependency_pattern:
            node_name = pattern_element['SPEC']['NODE_NAME']
            token_idx = node_name_to_token_idx(node_name)
            token = doc[token_idx]
            features = node_features(token, variation_feature_dict)
            new_spec = {'SPEC': pattern_element['SPEC'], 'PATTERN': features}
            new_dependency_pattern.append(new_spec)
        variations.append(new_dependency_pattern)
    return variations



def element_level_feature_substitution(dependency_pattern, doc, feature_combinations, feature_dict):
    # Yield a pattern for each combination of features in feature_combinations.  Generates N = len(feature_combinations) variations.
    