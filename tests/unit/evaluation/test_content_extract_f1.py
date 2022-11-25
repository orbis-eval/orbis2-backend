from orbis2.evaluation.metric import SUPPORTED_METRICS
from orbis2.model.annotation import Annotation
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.annotator import Annotator

ANNOTATOR = Annotator("muster", roles=[])


def test_content_extraction_f1_single_document():
    reference = {
        '0': [Annotation("", "Ehre sei Gott in der Höhe!", 30, 56,
                         annotation_type=AnnotationType("praise"), annotator=ANNOTATOR),
              ]
    }

    annotator = {
        '0': [Annotation("", "Ehre sei Gott", 30, 43,
                         annotation_type=AnnotationType("praise"), annotator=ANNOTATOR),
              ]
    }

    print(SUPPORTED_METRICS['content_extraction_f1'].metric)
    res = SUPPORTED_METRICS['content_extraction_f1'].metric().compute(reference, annotator)
    assert res.mP == 1
    assert res.MP == 1
    assert res.mR == 3 / 6
    assert res.MR == 3 / 6
    assert res.mF1 == res.mP * res.mR * 2 / (res.mP + res.mR)
    assert res.MF1 == res.MP * res.MR * 2 / (res.MP + res.MR)


def test_content_extraction_f1_multiple_documents():
    reference = {
        '0': [Annotation("", "Ehre sei Gott in der Höhe!", 30, 56,
                         annotation_type=AnnotationType("praise"), annotator=ANNOTATOR)],
        '1':  [Annotation("", "Und Friede den Menschen, die guten Willens sind.", 90, 138,
                          annotation_type=AnnotationType("praise"), annotator=ANNOTATOR)]
    }

    annotator = {
        '0': [Annotation("", "Ehre sei Gott", 30, 43,
                         annotation_type=AnnotationType("praise"), annotator=ANNOTATOR)],
        '1': [Annotation("", "Friede den Menschen, die guten Willens sind. Im Himmel", 94, 148,
                         annotation_type=AnnotationType("praise"), annotator=ANNOTATOR)]
    }

    res = SUPPORTED_METRICS['content_extraction_f1'].metric().compute(reference, annotator)
    assert res.mP == 10 / 12, "Incorrect mP."
    assert res.MP == (1 + 7 / 9) / 2, "Incorrect MP."
    assert res.mR == 10 / 14, "Incorrect mR"
    assert res.MR == (3 / 6 + 7 / 8) / 2, "Incorrect MR"
    assert res.mF1 == res.mP * res.mR * 2 / (res.mP + res.mR), "Incorrect mF1"
    assert res.MF1 == res.MP * res.MR * 2 / (res.MP + res.MR), "Incorrect MF1"
