#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.md').read()
doclink = """
Documentation
-------------

The full documentation is at http://spacy-pattern-builder.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='spacy-pattern-builder',
    version='0.0.1',
    description='Reverse engineer patterns for use with SpaCy\'s DependencyTreeMatcher',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Nick Morley',
    author_email='nick.morley111@gmail.com',
    url='https://github.com/cyclecycle/spacy-pattern-builder',
    packages=find_packages(),
    package_dir={'spacy-pattern-builder': 'spacy-pattern-builder'},
    include_package_data=True,
    install_requires=[
        'networkx==2.3',
    ],
    license='MIT',
    zip_safe=False,
    keywords='spacy-pattern-builder',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
