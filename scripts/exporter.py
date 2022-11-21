#!/usr/bin/env python3
from collections import namedtuple
from pathlib import Path

from orbis2.business_logic.orbis_service import OrbisService
from orbis2.config.corpus_export.careercoach import CareerCoachExportFormat
from orbis2.model.run import Run

ExportFormat = namedtuple('ExportFormat', 'exporter description')

SUPPORTED_EXPORT_FORMATS = {
    'careercoach2022': ExportFormat(CareerCoachExportFormat, 'The CareerCoach 2022 export format.')
}


def export_documents(export_run: Run, export_directory: Path, export_format: ExportFormat) -> None:
    """
    Export the run to the given corpus_directory.

    Args:
        export_run: The run to export.
        export_directory: The export directory.
        export_format: The
    """
    export_format.exporter.export(export_run, export_directory)


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

    if not (run := OrbisService().get_run_by_name(run_name=args.run_name)):
        print(f'Unknown run with name {args.run_name}')
        exit(-1)

    if not corpus_directory.exists():
        corpus_directory.mkdir(parents=True)

    export_documents(run, corpus_directory, export_format=export_format)
