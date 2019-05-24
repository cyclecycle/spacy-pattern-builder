# SpaCy Pattern Builder

Reverse engineer patterns for use with SpaCy's DependencyTreeMatcher by providing training examples.

## Motivation

Generating patterns programmatically from training data is more efficient than creating them manually.

## Installation

With pip:

```bash
pip install spacy-pattern-builder
```

## Usage

build_spacy_dependency_pattern() - if match_tokens is not a fully connected graph, will return an error. To get a fully connected graph, use: smallest_connected_subgraph(doc, tokens). alternatively, you can use slot-pattern, which handles this for you.

```python

```

## Acknowledgements

Build with:

- networkx