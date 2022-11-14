#!/usr/bin/env python3

from typing import List
from glob import glob
from pathlib import Path

from orbis2.corpus_import.format.careercoach import CareerCoachFormat
from orbis2.database.orbis.entities.corpus_dao import CorpusDao
from orbis2.database.orbis.entities.run_dao import RunDao
from orbis2.database.orbis.orbis_db import OrbisDb


IMPORT_FORMATS = (CareerCoachFormat,)


def import_documents(document_list: List[str], run_name: str,
                     run_description: str):
    """
    Import the given list of documents into the Orbis database.
    """
    for import_format in IMPORT_FORMATS:
        if import_format.is_supported(document_list):
            break
    else:
        raise ValueError("Unsupported corpus format.")

    run_documents = CareerCoachFormat.get_run_documents(document_list)

    # create run for serialization in the database
    run = RunDao(name=run_name, description=run_description,
            run_has_documents=run_documents, corpus=CorpusDao(name=run_name))
    db = OrbisDb()
    db.create_database(True)
    db.add_run(run)



if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('corpus_directory')
    parser.add_argument('run_name')
    parser.add_argument('--run-description',
                        help='Description of the given run.')
    args = parser.parse_args()
    if not args.run_description:
        args.run_description = args.run_name

    document_list = [p.open().read()
                     for p in map(Path, glob(args.corpus_directory + "/*"))
                     if p.is_file()]
    print(f'Importing {len(document_list)} documents.')
    import_documents(document_list, args.run_name, args.run_description)
