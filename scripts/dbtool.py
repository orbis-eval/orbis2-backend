#!/usr/bin/env python3
from orbis2.business_logic.orbis_service import OrbisService
from orbis2.database.orbis.orbis_db import OrbisDb

if __name__ == '__main__':
    from argparse import ArgumentParser, BooleanOptionalAction

    parser = ArgumentParser()
    parser.add_argument('--create-database', action=BooleanOptionalAction,
                        help='Create or recreated the Orbis database.')
    parser.add_argument('-f', '--force', action=BooleanOptionalAction,
                        help='Force potentially destructive actions without user confirmation.')
    parser.add_argument('--add-dummy-data', action=BooleanOptionalAction,
                        help='Add dummy data to database, but only if it is created.')

    args = parser.parse_args()

    if args.create_database and (args.force or input("WARNING: (Re)creating the database will delete all existing "
                                                     "data. Proceed (y/n)?") in ('y', 'Y')):
        db = OrbisDb()
        if not db.create_database(True):
            exit(-1)

        if args.add_dummy_data:
            from scripts.dummy_data import FIRST_RUN, SECOND_RUN, ANOTHER_RUN
            OrbisService().add_runs([FIRST_RUN, SECOND_RUN, ANOTHER_RUN])
