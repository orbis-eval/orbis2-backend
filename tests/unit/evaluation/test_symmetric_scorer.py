from itertools import chain
from operator import mul

from orbis2.evaluation.scorer.annotation_surface_scorer import exact_match
from orbis2.model.annotation import get_mock_annotation as Annotation
from orbis2.evaluation.scorer.symmetric_scorer import SymmetricScorer

ANNOTATOR1 = [Annotation(1, 5),
              Annotation(7, 14),
              Annotation(8, 14),
              Annotation(12, 14),
              Annotation(22, 24)]

ANNOTATOR2 = [Annotation(12, 14),
              Annotation(16, 18),
              Annotation(22, 24)]

ANNOTATOR3 = [Annotation(12, 14),
              Annotation(1, 5),
              Annotation(22, 24)]


def test_get_unique_annotation_list_exact_match():
    """
    Verifies the result of unique annotation list.
    """
    scorer = SymmetricScorer(surface_scorer=exact_match,
                             entity_scorer=lambda x, y: True,
                             scoring_operator=mul)

    # order does not change result
    reference = {a for a in chain(ANNOTATOR1, ANNOTATOR2, ANNOTATOR3)}
    assert list(sorted(reference)) == list(sorted(scorer.get_unique_annotation_list([ANNOTATOR1, ANNOTATOR2,
                                                                                     ANNOTATOR3])))
    assert list(sorted(reference)) == list(sorted(scorer.get_unique_annotation_list([ANNOTATOR2, ANNOTATOR3,
                                                                                     ANNOTATOR1])))
    assert list(sorted(reference)) == list(sorted(scorer.get_unique_annotation_list([ANNOTATOR3, ANNOTATOR1,
                                                                                     ANNOTATOR2])))
    assert len(list(sorted(scorer.get_unique_annotation_list([ANNOTATOR3, ANNOTATOR1,
                                                              ANNOTATOR2])))) == 6


def test_get_rater_agreement_matrix():
    """
    Compares the computed rater_agreement_matrix with a reference one.
    """
    eval_runs = [ANNOTATOR1, ANNOTATOR2, ANNOTATOR3]
    scorer = SymmetricScorer(surface_scorer=exact_match,
                             entity_scorer=lambda x, y: True,
                             scoring_operator=mul)
    unique_annotation_list = scorer.get_unique_annotation_list(eval_runs)
    rater_agreement_matrix = scorer.get_rater_agreement_matrix(unique_annotation_list, eval_runs)
    assert rater_agreement_matrix == [[1, 0, 1],
                                      [1, 0, 0],
                                      [1, 0, 0],
                                      [1, 1, 1],
                                      [1, 1, 1],
                                      [0, 1, 0]]
