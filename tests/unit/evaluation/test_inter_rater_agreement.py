from operator import mul

from orbis2.evaluation.metric.inter_rater_agreement import InterRaterAgreement
from orbis2.evaluation.scorer.annotation_surface_scorer import exact_match
from orbis2.model.annotation import get_mock_annotation as Annotation
from orbis2.evaluation.scorer.symmetric_scorer import SymmetricScorer

from pytest import approx

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


def test_inter_rater_agreement_computation():
    """
    Ensures that the inter rater agreement fulfills the outlined conditions
    """
    scorer = SymmetricScorer(surface_scorer=exact_match,
                             entity_scorer=lambda x, y: True,
                             scoring_operator=mul)
    irr = InterRaterAgreement(scorer=scorer)
    agreement = irr.compute([{1: ANNOTATOR1}, {1:ANNOTATOR2}, {1: ANNOTATOR3}])
    assert agreement == irr.compute([{1: ANNOTATOR2}, {1:ANNOTATOR3}, {1: ANNOTATOR1}])

    # use an annotator twice => higher agreement
    assert agreement < irr.compute([{1: ANNOTATOR2}, {1: ANNOTATOR3}, {1: ANNOTATOR2}])

    # approximation of the agreement score
    assert agreement.kappa_macro == approx(0.555555, abs=1E-06)
    assert agreement.kappa_micro == approx(0.555555, abs=1E-06)

    # approximation of the f1 score
    assert agreement.average_macro_f1 == approx(0.638888, abs=1E-06)
    assert agreement.average_micro_f1 == approx(0.638888, abs=1E-06)
