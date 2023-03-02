#!/usr/bin/env python3
from typing import List

from orbis2.business_logic.orbis_service import OrbisService
from orbis2.evaluation.annotation_preprocessor.abstract_annotation_preprocessor import AnnotationPreprocessor
from orbis2.evaluation.annotation_preprocessor.annotation_filter import AnnotationTypeFilter
from orbis2.evaluation.annotation_preprocessor.normalize_overlaps import NormalizeOverlaps
from orbis2.evaluation.metric import SUPPORTED_METRICS
from orbis2.evaluation.output_formatter import OrbisEvaluationResult
from orbis2.evaluation.output_formatter.markdown import MarkdownOutputFormatter


def verify_metrics_configuration(parser, args):
    """
    Verify that the provided metrics configuration is valid.

    1. the metric exist
    2. the number of annotator runs corresponds to the metric.
    3. a reference corpus is (only) specified, if the metric requires it.

    Raises:
        An ArgumentParserError, if any of these conditions is violated.
    """
    for metric in args.metrics:
        if metric not in SUPPORTED_METRICS:
            parser.error(f'Unsupported metric: {metric}.')
        if SUPPORTED_METRICS[metric].requires_reference_corpus:
            if not args.reference:
                parser.error(f'Metric \'{metric}\' requires a reference run.')
            if len(args.annotator) != 1:
                parser.error(f'Metric \'{metric}\' requires exactly one annotator run but '
                             f'{len(args.annotator)} runs have been specified.')
        else:
            if args.reference:
                parser.error(f'Metric \'{metric}\' does not support specification of a reference run.')
            if len(args.annotator) < 2:
                parser.error(f'Metric \'{metric}\' requires at least two annotators, but only '
                             f'{len(args.annotator)} have been specified.')


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('annotator', nargs='+', help='The annotator run(s), i.e. the run with the predicted or '
                                                     'user-supplied annotations.')
    parser.add_argument('--reference', help='The run containing the annotations considered to be true, i.e., '
                                            'the gold standard.')
    parser.add_argument('--metrics', nargs='+', default=[], help='The metrics to compute.')
    parser.add_argument('--type-whitelist', nargs='*', default=[],
                        help='Optional list of annotation types to evaluation.')
    parser.add_argument('--type-blacklist', nargs='*', default=[], help='Optional list of annotation types to ignore.')
    parser.add_argument('--type-priority', nargs='*', default=[],
                        help='Optional list that indicates the annotation '
                             'types\'s priorities (the most important type is listed first; types not listed receive '
                             'equal priority). If specified, Orbis removes overlapping annotations from the evaluation '
                             'based on the annotation type\'s priority. Annotations of same priority are filtered '
                             'based on the annotation\'s length (i.e., longer annotations are preferred over shorter '
                             'ones). ')
    parser.add_argument('--serialize', help='Optional filename for serializing the evaluation results.')
    args = parser.parse_args()

    # ensure that the provided metrics configuration is valid.
    verify_metrics_configuration(parser, args)

    # compile the list of runs to annotate; the reference run (if available) is always on the first position
    orbis = OrbisService()
    eval_runs = [orbis.get_run_by_name(args.reference).document_annotations] if args.reference else []
    for annotator_run in args.annotator:
        eval_runs.append(orbis.get_run_by_name(annotator_run).document_annotations)

    annotation_preprocessors: List[AnnotationPreprocessor] = []
    if args.type_blacklist:
        annotation_preprocessors.append(AnnotationTypeFilter(blacklist=tuple(args.type_blacklist)))
    if args.type_whitelist:
        annotation_preprocessors.append(AnnotationTypeFilter(whitelist=tuple(args.type_whitelist)))
    if args.type_priority:
        annotation_preprocessors.append(NormalizeOverlaps(annotation_priority=tuple(args.type_priority)))

    result = []
    for metric in args.metrics:
        res = SUPPORTED_METRICS[metric].metric(*annotation_preprocessors).compute(eval_runs)
        result.append(OrbisEvaluationResult(SUPPORTED_METRICS[metric].description, res))

    if args.serialize:
        with open(args.serialize, 'bw') as f:
            from pickle import dump

            dump({'eval_runs': eval_runs,
                  'metrics': result},
                 f)

    print(MarkdownOutputFormatter().format_output(result))
