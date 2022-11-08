from orbis2.model.annotation import Annotation
from orbis2.evaluation.scorer import ScorerResult

PREDICTED = [Annotation(1, 5),
             Annotation(7, 14),
             Annotation(8, 14),
             Annotation(12, 14),
             Annotation(22, 24)
             ]

TRUE = [Annotation(12, 14),
        Annotation(16, 18),
        Annotation(22, 24)]

def scorer_test():
