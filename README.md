# SpaCy Pattern Builder

Use training examples to build and refine patterns for use with SpaCy's DependencyMatcher.

## Motivation

Generating patterns programmatically from training data is more efficient than creating them manually.

## Installation

With pip:

```bash
pip install spacy-pattern-builder
```

## Usage

```python
# Import a SpaCy model, parse a string to create a Doc object
import en_core_web_sm

text = 'We introduce efficient methods for fitting Boolean models to molecular data.'
nlp = en_core_web_sm.load()
doc = nlp(text)

from spacy_pattern_builder import build_dependency_pattern

# Provide a list of tokens we want to match.
match_tokens = [doc[i] for i in [0, 1, 3]]  # [We, introduce, methods]

''' Note that these tokens must be fully connected. That is,
all tokens must have a path to all other tokens in the list,
without needing to traverse tokens outside of the list.
Otherwise, spacy-pattern-builder will raise a TokensNotFullyConnectedError.
You can get a connected set that includes your tokens with the following: '''
from spacy_pattern_builder import util
connected_tokens = util.smallest_connected_subgraph(match_tokens, doc)
assert match_tokens == connected_tokens  # In this case, the tokens we provided are already fully connected

# Specify the token attributes / features to use
feature_dict = {  # This is equal to the default feature_dict
    'DEP': 'dep_',
    'TAG': 'tag_'
}

# Build the pattern
pattern = build_dependency_pattern(doc, match_tokens, feature_dict=feature_dict)

from pprint import pprint
pprint(pattern)  # In the format consumed by SpaCy's DependencyMatcher:
'''
[{'PATTERN': {'DEP': 'ROOT', 'TAG': 'VBP'}, 'SPEC': {'NODE_NAME': 'node1'}},
 {'PATTERN': {'DEP': 'nsubj', 'TAG': 'PRP'},
  'SPEC': {'NBOR_NAME': 'node1', 'NBOR_RELOP': '>', 'NODE_NAME': 'node0'}},
 {'PATTERN': {'DEP': 'dobj', 'TAG': 'NNS'},
  'SPEC': {'NBOR_NAME': 'node1', 'NBOR_RELOP': '>', 'NODE_NAME': 'node3'}}]
'''

# Create a matcher and add the newly generated pattern
from spacy.matcher import DependencyMatcher

matcher = DependencyTreeMatcher(doc.vocab)
matcher.add('pattern', None, pattern)

# And get matches
matches = matcher(doc)
for match_id, token_idxs in matches:
    tokens = [doc[i] for i in token_idxs]
    tokens = sorted(tokens, key=lambda w: w.i)  # Make sure tokens are in their original order
    print(tokens)  # [We, introduce, methods]

```

## Acknowledgements

Uses:

- [SpaCy](https://spacy.io)
- [networkx](https://github.com/networkx/networkx)