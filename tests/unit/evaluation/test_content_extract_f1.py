from orbis2.evaluation.metric import SUPPORTED_METRICS
from orbis2.model.annotation import get_mock_annotation as Annotation


def test_content_extraction_f1_single_document():
    reference = {
        '0': [Annotation(surface_forms="Ehre sei Gott in der Höhe!", start_indices=30, end_indices=56,
                         annotation_type="praise"),
              ]
    }

    annotator = {
        '0': [Annotation(surface_forms="Ehre sei Gott", start_indices=30, end_indices=43, annotation_type="praise"),
              ]
    }

    print(reference)
    print(annotator)
    print(SUPPORTED_METRICS['content_extraction_f1'].metric)
    res = SUPPORTED_METRICS['content_extraction_f1'].metric().compute([reference, annotator])
    assert res.mP == 1
    assert res.MP == 1
    assert res.mR == 3 / 6
    assert res.MR == 3 / 6
    assert res.mF1 == res.mP * res.mR * 2 / (res.mP + res.mR)
    assert res.MF1 == res.MP * res.MR * 2 / (res.MP + res.MR)


def test_content_extraction_f1_multiple_documents():
    reference = {
        '0': [Annotation(surface_forms="Ehre sei Gott in der Höhe!", start_indices=30, end_indices=56,
                         annotation_type="praise")],
        '1':  [Annotation(surface_forms="Und Friede den Menschen, die guten Willens sind.",
                          start_indices=90, end_indices=138, annotation_type="praise")]
    }

    annotator = {
        '0': [Annotation(surface_forms="Ehre sei Gott", start_indices=30, end_indices=43,
                         annotation_type="praise", annotator="mocky")],
        '1': [Annotation(surface_forms="Friede den Menschen, die guten Willens sind. Im Himmel",
                         start_indices=94, end_indices=148,
                         annotation_type="praise", annotator="mocky")]
    }

    res = SUPPORTED_METRICS['content_extraction_f1'].metric().compute([reference, annotator])
    assert res.mP == 10 / 12, "Incorrect mP."
    assert res.MP == (1 + 7 / 9) / 2, "Incorrect MP."
    assert res.mR == 10 / 14, "Incorrect mR"
    assert res.MR == (3 / 6 + 7 / 8) / 2, "Incorrect MR"
    assert res.mF1 == res.mP * res.mR * 2 / (res.mP + res.mR), "Incorrect mF1"
    assert res.MF1 == res.MP * res.MR * 2 / (res.MP + res.MR), "Incorrect MF1"
