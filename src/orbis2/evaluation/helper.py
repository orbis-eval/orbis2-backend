from orbis2.evaluation.metric.inter_rater_agreement import InterRaterAgreement, InterRaterAgreementResult
from orbis2.evaluation.scorer.symmetric_scorer import SymmetricScorer
from orbis2.evaluation.scorer.asymmetric_scorer import AsymmetricScorer

from operator import mul
from orbis2.evaluation.scorer.annotation_entity_scorer import same_entity
from orbis2.evaluation.scorer.annotation_surface_scorer import exact_match, overlapping_match


def get_inter_rater_agreement_result(gold_standard_document_annotations,
                                     run_document_annotations) -> InterRaterAgreementResult:
    scorer = SymmetricScorer(surface_scorer=exact_match, entity_scorer=same_entity, scoring_operator=mul)
    ira = InterRaterAgreement(scorer)
    eval_runs_list = [gold_standard_document_annotations, run_document_annotations]
    if eval_runs_list[0] and eval_runs_list[1]:
        return ira.compute(eval_runs_list)
    return None


def get_scoring_annotation_level(true_annotations, pred_annotations) -> dict:
    scorer = AsymmetricScorer(surface_scorer=overlapping_match,
                              entity_scorer=lambda x, y: True,
                              scoring_operator=mul)
    scoring = scorer.score_annotation_list(true_annotations=true_annotations,
                                           pred_annotations=pred_annotations)
    return scoring
