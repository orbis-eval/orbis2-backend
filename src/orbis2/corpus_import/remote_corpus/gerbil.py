"""
Provide access to the corpora published by GERBIL under
  https://github.com/dice-group/gerbil/tree/master/src/main/resources/dataId/corpora
"""

import gzip
from rdflib import Namespace, Graph
from rdflib.namespace import RDF, DCTERMS
from pathlib import Path
from glob import glob
from collections import namedtuple

RemoteCorpus = namedtuple('RemoteCorpus', 'url title date language rights description')
CORPUS_DIR = Path(__file__).parent / 'data' / 'gerbil'

DCAT = Namespace('http://www.w3.org/ns/dcat#')


get = lambda g, s, p: list(g.triples((s, p, None)))[0][2].replace('\n', ' ')


def parse_corpus_definition(fname):
    with gzip.open(fname, 'rt', encoding='latin1') as f:
        g = Graph()
        g.parse(f, format='turtle')

        for s, p, o in g.triples((None, RDF.type, DCAT.Dataset)):
            title = get(g, s, DCTERMS.title)
            date = get(g, s, DCTERMS.issued)
            language = get(g, s, DCTERMS.language)
            rights = get(g, s, DCTERMS.rights)
            description = get(g, s, DCTERMS.description)
            url = get(g, s, DCAT.distribution)
    return RemoteCorpus(url, title, date, language, rights, description)


CORPORA = {str(fname.name).split('.')[0]: parse_corpus_definition(fname) for fname in sorted(CORPUS_DIR.glob('*.ttl.gz'))}
