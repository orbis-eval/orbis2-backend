#!/usr/bin/env python3

from glob import glob
from shutil import copy
import os.path


def _get_document_id(p):
    print(p.split('_i')[1].split('.json')[0])
    return int(p.split('_i')[1].split('.json')[0])

if __name__ == '__main__':
    from argparse import ArgumentParser, BooleanOptionalAction

    parser = ArgumentParser()
    parser.add_argument('source_directory')
    parser.add_argument('destination_directory')
    parser.add_argument('--start', type=int, help='Lowest index to move.')
    parser.add_argument('--end', type=int, help='Highest document index to move.')

    args = parser.parse_args()

    files = [path for path in sorted(glob(args.source_directory + "/*"), key=lambda p: _get_document_id(p))]
    for fname in files[args.start:args.end+1]:
        print(fname)
        copy(fname, os.path.join(args.destination_directory, os.path.basename(fname)))

