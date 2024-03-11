#!/usr/bin/env python3

import sys
from pathlib import Path
from typing import List, Dict
from urllib.request import urlopen

try:
    orbis_src = Path(__file__).parent.parent / 'src'
    if orbis_src.is_dir():
        sys.path.append(str(orbis_src))
except IndexError:
    pass

from orbis2.business_logic.orbis_service import OrbisService
from orbis2.corpus_import.format.careercoach import CareerCoachFormat
from orbis2.corpus_import.format.nif import NifFormat
from orbis2.evaluation.scorer.annotation_util import contains
from orbis2.model.annotation import Annotation
from orbis2.model.corpus import Corpus
from orbis2.model.document import Document
from orbis2.model.run import Run

IMPORT_FORMATS = (CareerCoachFormat, NifFormat)


def append_annotations_with_segments(document_annotations: Dict[Document, List[Annotation]],
                                     document_segments: Dict[Document, List[Annotation]]):
    resulting_document_annotations = {}
    for document, annotations in document_annotations.items():
        resulting_document_annotations[document] = []
        for segment in document_segments[document]:
            for annotation in annotations:
                if contains(segment, annotation):
                    annotation.metadata = segment.metadata
                    resulting_document_annotations[document].append(annotation)
    return resulting_document_annotations


def import_documents(document_list: List[str], run_name: str, run_description: str, invalid_annotation_types: List[str],
                     corpus_partition: str = None, careercoach_filter: str = None):
    """
    Import the given list of documents into the Orbis database.
    """
    for import_format in IMPORT_FORMATS:
        if import_format.is_supported(document_list, corpus_partition):
            break
    else:
        raise ValueError("Unsupported corpus format.")

    # create run for serialization in the database
    document_annotations = import_format.get_document_annotations(document_list,
                                                                  invalid_annotation_types=invalid_annotation_types,
                                                                  partition=corpus_partition)

    # filter the annotations based on Annotations specified in a second corpus.
    if careercoach_filter:
        filter_documents = [p.open().read() for p in Path(careercoach_filter).rglob('*.json') if p.is_file()]
        document_segments = import_format.get_document_annotations(
            filter_documents, invalid_annotation_types=invalid_annotation_types,
            partition='gold_standard_annotation_segmentation')
        document_annotations = append_annotations_with_segments(document_annotations, document_segments)

    supported_annotation_types = import_format.get_supported_annotation_types(document_annotations)
    OrbisService().add_run(Run(name=run_name, description=run_description,
                               corpus=Corpus(name=run_name, supported_annotation_types=supported_annotation_types),
                               document_annotations=document_annotations))

    # Add Gold Standard
    OrbisService().add_run(Run(name="Gold Standard", description=run_description,
                               corpus=Corpus(name=run_name, supported_annotation_types=supported_annotation_types),
                               document_annotations=document_annotations, is_gold_standard=True))


def import_local_corpus(subargs):
    """
    Import the corpus from the local file system.
    """
    corpus_path = Path(subargs.corpus_path)
    if corpus_path.is_dir():
        documents = [p.open().read() for p in corpus_path.rglob("*.json") if p.is_file()]
    else:
        documents = [corpus_path.open().read()]
    print(f'Importing {len(documents)} documents.')
    import_documents(documents, subargs.run_name, subargs.run_description,
                     invalid_annotation_types=subargs.invalid_annotation_type,
                     corpus_partition=subargs.corpus_partition,
                     careercoach_filter=subargs.careercoach_filter)


def import_remote_corpus(subargs):
    """
    Import the corpus from a remote repository.
    """
    from orbis2.corpus_import.remote_corpus.gerbil import CORPORA
    if subargs.corpus_name not in CORPORA:
        print(f"Unknown corpus name: '{subargs.corpus_name}'. Use the 'list-remote' command to obtain a list of "
              "available corpora")
        sys.exit(-1)

    if not subargs.run_description:
        subargs.run_description = subargs.run_name

    # fetch the corpus from the remove server
    corpus = CORPORA[subargs.corpus_name]
    if not corpus.url.lower().startswith('http'):
        raise ValueError(f'Invalid URL: {corpus.url}.')

    print(f"Fetching remote corpus from '{corpus.url}'")
    with urlopen(corpus.url) as f:  # noqa: S310 -- http schema enforced above
        documents = [f.read().decode(f.headers.get_content_charset())]
        print("Importing corpus.")
        import_documents(documents, subargs.run_name, subargs.run_description,
                         invalid_annotation_types=subargs.invalid_annotation_type)


def list_remote_corpora(_):
    """
    Provide a list with all remote corpora.
    """
    from orbis2.corpus_import.remote_corpus.gerbil import CORPORA
    for identifier, corpus in CORPORA.items():
        print(f'{identifier}: {corpus.title} ({corpus.date}, {corpus.language})')
        print(f'  {corpus.description}\n')


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    subparsers = parser.add_subparsers(required=True)

    parser_remote = subparsers.add_parser('remote', help='Import a named corpus (e.g., Reuters-128) from a remote '
                                                         'repository.')
    parser_remote.add_argument('corpus_name', help='The name of the corpus to import.')
    parser_remote.add_argument('run_name', help='The AnnotatedCorpus (i.e., run) name to use.')
    parser_remote.add_argument('--run-description', help='Description of the given run.')
    parser_remote.add_argument('--invalid-annotation-type', nargs="+", default=[],
                               help='Annotation types to ignore during import.')
    parser_remote.set_defaults(func=import_remote_corpus)

    parser_local = subparsers.add_parser('local', help='Import a corpus from the local filesystem.')
    parser_local.add_argument('corpus_path', help='The path to the corpus to import')
    parser_local.add_argument('run_name', help='The AnnotatedCorpus (i.e., run) name to use.')
    parser_local.add_argument('--run-description', help='Description of the given run.')
    parser_local.add_argument('--invalid-annotation-type', nargs="+", default=[],
                              help='Annotation types to ignore during import.')

    parser_local.add_argument('--corpus-partition', help='Corpus partition to import.')
    parser_local.add_argument('--careercoach-filter', help='Optional CareerCoach segment corpus for filtering the '
                                                           'results')
    parser_local.set_defaults(func=import_local_corpus)

    parser_list = subparsers.add_parser('list-remote', help='List all available remote corpora.')
    parser_list.set_defaults(func=list_remote_corpora)

    args = parser.parse_args()
    args.func(args)
