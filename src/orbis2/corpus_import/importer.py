#!/usr/bin/env python3

from typing import List
from glob import glob
from pathlib import Path

from orbis2.corpus_import.format.careercoach import CareerCoachFormat

IMPORT_FORMATS = (CareerCoachFormat,)

def  import_documents(document_list: List[str]):
    for import_format in IMPORT_FORMATS:
        if import_format.is_supported(document_list):
            break
    else:
        raise ValueError("Unsupported corpus format.")

    document_content  = import_format.get_document_content(document_list)
    annotations = import_format.get_document_annotations(document_list)


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('corpus_directory')
    args = parser.parse_args()

    document_list = [p.open().read() for p in map(Path,
                                                  glob(args.corpus_directory + "/*"))
                     if p.is_file()]
    print(f'Importing {len(document_list)} documents.')
    import_documents(document_list)