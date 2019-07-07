'''Generate pattern variants
'''
from pprint import pprint
import itertools
from spacy_pattern_builder.exceptions import FeaturesMissingFromPatternError
from spacy_pattern_builder import util


def yield_pattern_permutations(pattern, feature_sets):
    # First check all features in feature_sets are present in all pattern_elements
    all_features = set(util.flatten_list(feature_sets))
    all_features_are_in_pattern = util.features_are_in_pattern(all_features, pattern)
    if not all_features_are_in_pattern:
        raise FeaturesMissingFromPatternError('Tried to create pattern permutations using features that are not present in the pattern. Ensure the pattern has all the features specified in feature_sets.')
    pattern_element_combinations = []
    for pattern_element in pattern:
        token_features = pattern_element['PATTERN']
        new_pattern_elements = []
        for feature_set in feature_sets:
            new_token_features = {k: v for k, v in token_features.items() if k in feature_set}
            new_pattern_element = {'SPEC': pattern_element['SPEC'], 'PATTERN': new_token_features}
            new_pattern_elements.append(new_pattern_element)
        pattern_element_combinations.append(new_pattern_elements)
    return itertools.product(*pattern_element_combinations)
