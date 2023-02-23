from collections import namedtuple
from functools import partialmethod
from operator import mul

from orbis2.evaluation.annotation_preprocessor.tokenizer import AnnotationTokenizer, TokenizeBy
from orbis2.evaluation.annotation_preprocessor.unique import UniqueSlotValue
from orbis2.evaluation.metric.f1 import F1Metric
from orbis2.evaluation.scorer import Scorer
from orbis2.evaluation.scorer.annotation_util import overlaps
from orbis2.evaluation.scorer.annotation_entity_scorer import same_entity, same_type, always_true
from orbis2.evaluation.scorer.annotation_surface_scorer import exact_match

MetricDescription = namedtuple('MetricDescription', 'metric requires_reference_corpus description')


def p(cls, *args, **kw):
    """
    A type save partial for classes which allows adding annotation_preprocessors to the F1Metric class.
    """

    class NewCls(cls):
        __init__ = partialmethod(cls.__init__, *args, **kw)
    return NewCls


SUPPORTED_METRICS = {
    'slot_filling_pF1': MetricDescription(p(F1Metric, Scorer(surface_scorer=exact_match,
                                                             entity_scorer=same_entity,
                                                             scoring_operator=mul),
                                            UniqueSlotValue()),
                                          requires_reference_corpus=True,
                                          description='Slot filling: Precision, Recall and F1; perfect matching.'),
    'slot_filling_oF1': MetricDescription(p(F1Metric, Scorer(surface_scorer=overlaps,
                                                             entity_scorer=same_entity,
                                                             scoring_operator=mul),
                                            UniqueSlotValue()),
                                          requires_reference_corpus=True,
                                          description='Slot filling: Precision, Recall and F1; overlapping matching.'),
    'el_pF1': MetricDescription(p(F1Metric, Scorer(surface_scorer=exact_match,
                                                   entity_scorer=same_entity,
                                                   scoring_operator=mul),
                                  ),
                                requires_reference_corpus=True,
                                description='Entity Linking: Precision, Recall and F1; perfect matching.'),
    'el_oF1': MetricDescription(p(F1Metric, Scorer(surface_scorer=overlaps,
                                                   entity_scorer=same_entity,
                                                   scoring_operator=mul),
                                  ),
                                requires_reference_corpus=True,
                                description='Entity Linking: Precision, Recall and F1; overlapping matching.'),
    'ec_pF1': MetricDescription(p(F1Metric, Scorer(surface_scorer=exact_match,
                                                   entity_scorer=same_type,
                                                   scoring_operator=mul),
                                  ),
                                requires_reference_corpus=True,
                                description='Entity Classification: Precision, Recall and F1; perfect matching.'),
    'ec_oF1': MetricDescription(p(F1Metric, Scorer(surface_scorer=overlaps,
                                                   entity_scorer=same_type,
                                                   scoring_operator=mul),
                                  ),
                                requires_reference_corpus=True,
                                description='Entity Recognition: Precision, Recall and F1; overlapping matching.'),
    'er_pF1': MetricDescription(p(F1Metric, Scorer(surface_scorer=exact_match,
                                                   entity_scorer=always_true,
                                                   scoring_operator=mul),
                                  ),
                                requires_reference_corpus=True,
                                description='Entity Recognition: Precision, Recall and F1; perfect matching.'),
    'er_oF1': MetricDescription(p(F1Metric, Scorer(surface_scorer=overlaps,
                                                   entity_scorer=always_true,
                                                   scoring_operator=mul),
                                  ),
                                requires_reference_corpus=True,
                                description='Entity Recognition: Precision, Recall and F1; overlapping matching.'),
    'content_extraction_f1': MetricDescription(p(F1Metric, Scorer(surface_scorer=exact_match,
                                                                  entity_scorer=always_true,
                                                                  scoring_operator=mul),
                                                 AnnotationTokenizer(
                                                     tokenize_by=TokenizeBy.WHITESPACE)),
                                               requires_reference_corpus=True,
                                               description='Content Extraction: Precision, Recall and F1.'),
    'content_classification_f1': MetricDescription(p(F1Metric, Scorer(surface_scorer=exact_match,
                                                                      entity_scorer=same_entity,
                                                                      scoring_operator=mul),
                                                     AnnotationTokenizer(
                                                         tokenize_by=TokenizeBy.WHITESPACE)),
                                                   requires_reference_corpus=True,
                                                   description='Content Classification: Precision, Recall and F1.'),
}
