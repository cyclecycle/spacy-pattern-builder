from setuptools import setup, find_packages

readme = open('README.md').read()
requirements = open('requirements.txt').read().splitlines()

setup(
    name='spacy-pattern-builder',
    version='0.0.6',
    description='Reverse engineer patterns for use with the SpaCy DependencyTreeMatcher',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Nick Morley',
    author_email='nick.morley111@gmail.com',
    url='https://github.com/cyclecycle/spacy-pattern-builder',
    packages=find_packages(),
    package_dir={'spacy-pattern-builder': 'spacy-pattern-builder'},
    include_package_data=True,
    install_requires=requirements,
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
