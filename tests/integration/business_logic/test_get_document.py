"""
Test navigation using the get_document calls.
"""
from itertools import chain

from orbis2.business_logic.orbis_service import OrbisService


def test_get_next_document(insert_test_data_multiple_documents):
    """
    Return the next document for a given run.
    """
    run_id = OrbisService().get_run_by_name('run2').identifier
    document_ids = sorted([document.identifier for document in OrbisService().get_documents_of_run(run_id=run_id)])
    assert len(document_ids) > 1

    # test obtaining the document with the next id. the method cycles to the next document, if called with the
    # corpus' last document id.
    for current_id, next_id in zip(document_ids, chain(document_ids[1:], document_ids)):
        next_document = OrbisService().get_next_document(run_id=run_id, document_id=current_id)
        assert next_document and next_document.identifier == next_id


def test_get_previous_document(insert_test_data_multiple_documents):
    """
    Return the previous document for a given run.
    """
    run_id = OrbisService().get_run_by_name('run2').identifier
    document_ids = sorted([document.identifier for document in OrbisService().get_documents_of_run(run_id=run_id)])
    assert len(document_ids) > 1

    # test obtaining the document with the next id. the method cycles to the next document, if called with the
    # corpus' last document id.
    for current_id, previous_id in zip(chain(document_ids[1:], document_ids), document_ids):
        print(current_id, previous_id, document_ids)
        previous_document = OrbisService().get_previous_document(run_id=run_id, document_id=current_id)
        assert previous_document and previous_document.identifier == previous_id
        break
