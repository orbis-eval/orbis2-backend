#!/usr/bin/env python3

from glob import glob
from pathlib import Path
from typing import List, Dict

from orbis2.business_logic.orbis_service import OrbisService
from orbis2.corpus_import.format.careercoach import CareerCoachFormat
from orbis2.database.orbis.orbis_db import OrbisDb
from orbis2.evaluation.scorer.annotation_util import contains
from orbis2.model.annotation import Annotation
from orbis2.model.corpus import Corpus
from orbis2.model.document import Document
from orbis2.model.run import Run

IMPORT_FORMATS = (CareerCoachFormat,)


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
    document_annotations = CareerCoachFormat.get_document_annotations(document_list,
                            invalid_annotation_types=invalid_annotation_types, partition=corpus_partition)

    # filter the annotations based on Annotations specified in a second corpus.
    if careercoach_filter:
        filter_documents = [p.open().read() for p in map(Path, glob(careercoach_filter + "/**", recursive=True))
                            if p.is_file()]

        document_segments = CareerCoachFormat.get_document_annotations(
            filter_documents, invalid_annotation_types=invalid_annotation_types,
            partition='gold_standard_annotation_segmentation')

        document_annotations = append_annotations_with_segments(document_annotations, document_segments)

    supported_annotation_types = CareerCoachFormat.get_supported_annotation_types(document_annotations)
    OrbisService().add_run(Run(name=run_name, description=run_description,
                               corpus=Corpus(name=run_name, supported_annotation_types=supported_annotation_types),
                               document_annotations=document_annotations))


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('corpus_directory')
    parser.add_argument('run_name')
    parser.add_argument('--run-description', help='Description of the given run.')
    parser.add_argument('--corpus-partition', help='Corpus partition to import.')
    parser.add_argument('--invalid-annotation-type', nargs="+", default=[],
                        help='Annotation types to ignore during import.')
    parser.add_argument('--careercoach-filter', help='Optional CareerCoach segment corpus for filtering the results')
    args = parser.parse_args()
    if not args.run_description:
        args.run_description = args.run_name

    documents = [p.open().read()
                 for p in map(Path, glob(args.corpus_directory + "/**", recursive=True))
                 if p.is_file()]
    print(f'Importing {len(documents)} documents.')
    import_documents(documents, args.run_name, args.run_description,
                     invalid_annotation_types=args.invalid_annotation_type,
                     corpus_partition=args.corpus_partition,
                     careercoach_filter=args.careercoach_filter)
