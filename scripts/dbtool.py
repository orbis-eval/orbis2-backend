#!/usr/bin/env python3

from glob import glob
from pathlib import Path
from typing import List

from orbis2.business_logic.orbis_service import OrbisService
from orbis2.corpus_import.format.careercoach import CareerCoachFormat
from orbis2.database.orbis.orbis_db import OrbisDb
from orbis2.evaluation.scorer.annotation_util import contains
from orbis2.model.corpus import Corpus
from orbis2.model.run import Run


if __name__ == '__main__':
    from argparse import ArgumentParser, BooleanOptionalAction

    parser = ArgumentParser()
    parser.add_argument('--create-database', action=BooleanOptionalAction,
                        help='Create or recreated the Orbis database.')
    parser.add_argument('-f', '--force', action=BooleanOptionalAction,
                        help='Force potentially destructive actions without user confirmation.')

    args = parser.parse_args()

    if args.create_database and (args.force or input("WARNING: (Re)creating the database will delete all existing "
                                                     "data. Proceede (y/n)?") in ('y', 'Y')):
        db = OrbisDb()
        db.create_database(True)
