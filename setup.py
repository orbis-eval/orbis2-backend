#!/usr/bin/env python

"""orbis2 backend setup script."""

import sys
from pathlib import Path
from setuptools import setup, find_packages
from os import path

here = Path(path.dirname(__file__)).resolve()
sys.path.insert(0, path.join(here, 'src'))

from src.orbis2.metadata import __version__

setup(
    # Metadata
    name='orbis2-backend',
    version=__version__,
    description='orbis2-backend - backend for the orbis2 framework, used for annotating and evaluating nlp documents',
    python_requires='>=3.9',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.9',
    ],
    package_dir={'': 'src'},

    # Package List
    packages=find_packages(where='src'),

    # Include gerbil files
    package_data={
        'orbis2.corpus_import.remote_corpus': ['data/gerbil/*'],
    },

    # Requirements
    install_requires=[
        'SQLAlchemy',
        'SQLAlchemy-Utils',
        'psycopg2-binary',
        'fastapi',
        'pytest',
        'pydantic',
        'xxhash',
        'scikit-learn',
        'uvicorn'
    ],
)
