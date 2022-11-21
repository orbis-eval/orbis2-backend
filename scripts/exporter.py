#!/usr/bin/env python3
from collections import namedtuple
from glob import glob
from pathlib import Path
from typing import List

from orbis2.business_logic.orbis_service import OrbisService
from orbis2.corpus_import.format.careercoach import CareerCoachFormat
from orbis2.database.orbis.orbis_db import OrbisDb
from orbis2.evaluation.scorer.annotation_util import contains
from orbis2.model.corpus import Corpus
from orbis2.model.run import Run

ExportFormat = namedtuple('ExportFormat', 'class description')

SUPPORTED_EXPORT_FORMATS = {
    'careercoach': ExportFormat(None, 'The CareerCoach 2022 export format.')
}


def export_documents(run_id: int, corpus_directory: Path, format: ExportFormat) -> None:
    """
    Export the run to the given corpus_directory.

    Args:
        run_name: The run to export.
        corpus_directory: The export directory.
        format: The
    """
    run = OrbisService().get_runs_by_corpus_id(run_id)[ß]


    # create run for serialization in the database
    # db = OrbisDb()
    # db.create_database(True)
    document_annotations = CareerCoachFormat.get_document_annotations(document_list, corpus_partition)

    # filter the annotations based on Annotations specified in a second corpus.
    if careercoach_filter:
        filter_documents = [p.open().read() for p in map(Path, glob(careercoach_filter + "/*")) if p.is_file()]

        document_segments = CareerCoachFormat.get_document_annotations(
            filter_documents, partition='gold_standard_annotation_segmentation')
        document_annotations = {document: [annotation
                                           for annotation in annotations if any(
               [contains(segment_annotation, annotation)
                for segment_annotation in document_segments[document]]
            )]
                                for document, annotations in document_annotations.items()}

    supported_annotation_types = CareerCoachFormat.get_supported_annotation_types(document_annotations)
    OrbisService().add_run(Run(name=run_name, description=run_description,
                               corpus=Corpus(name=run_name, supported_annotation_types=supported_annotation_types),
                               document_annotations=document_annotations))


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('run_name')
    parser.add_argument('corpus_directory', help='Directory to export to')
    parser.add_argument('--export-format', help='Export run to the given export format.')
    args = parser.parse_args()

    corpus_directory = Path(args.corpus_directory)
    if args.export_format not in SUPPORTED_EXPORT_FORMATS:
        print(f'Unsupported export format: {args.export_format}.')
        exit(-1)
    export_format = SUPPORTED_EXPORT_FORMATS[args.export_format]

    if not (run_id := OrbisService.get_corpus(args.run_name)):
        print(f'Unknown run with name {args.run_name}')
        exit(-1)

    if not corpus_directory.exists():
        corpus_directory.mkdir(parents=True)

    export_documents(run_id, corpus_directory, export_format=export_format)
