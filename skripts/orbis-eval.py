#!/usr/bin/env python3

from orbis2.business_logic.orbis_service import OrbisService

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('reference', help='The run containing the annotations considered to be true, i.e., '
                                          'the gold standard.')
    parser.add_argument('annotator', help='The annotator run, i.e. the predicted annotations.')
    parser.add_argument('--metrics', help='The metrics to compute')
    args = parser.parse_args()

    orbis = OrbisService()
    reference = orbis.get_runs_by_corpus_id(corpus_id=orbis.get_corpus_id(args.reference))
    annotator = orbis.get_runs_by_corpus_id(corpus_id=orbis.get_corpus_id(args.annotator))

