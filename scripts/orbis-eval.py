#!/usr/bin/env python3
from typing import List
from warnings import warn

from orbis2.business_logic.orbis_service import OrbisService
from orbis2.evaluation.annotation_preprocessor.abstract_annotation_preprocessor import AnnotationPreprocessor
from orbis2.evaluation.annotation_preprocessor.annotation_filter import AnnotationTypeFilter
from orbis2.evaluation.annotation_preprocessor.normalize_overlaps import NormalizeOverlaps
from orbis2.evaluation.metric import SUPPORTED_METRICS
from orbis2.evaluation.output_formatter import OrbisEvaluationResult
from orbis2.evaluation.output_formatter.markdown import MarkdownOutputFormatter

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('reference', help='The run containing the annotations considered to be true, i.e., '
                                          'the gold standard.')
    parser.add_argument('annotator', help='The annotator run, i.e. the run with the predicted annotations.')
    parser.add_argument('--metrics', nargs='+', default=[], help='The metrics to compute.')
    parser.add_argument('--type-whitelist', nargs='*', default=[],
                        help='Optional list of annotation types to evaluation.')
    parser.add_argument('--type-blacklist', nargs='*', default=[], help='Optional list of annotation types to ignore.')
    parser.add_argument('--type-priority', nargs='*', default=[], help='Optional list that indicates the annotation '
                        'types\'s priorities (the most important type is listed first; types not listed receive equal '
                        'priority). If specified, Orbis removes overlapping annotations from the evaluation based on '
                        'the annotation type\'s priority. Annotations of same priority are filtered based on the '
                        'annotation\'s length (i.e., longer annotations are preferred over shorter ones). ')
    args = parser.parse_args()

    orbis = OrbisService()
    reference = orbis.get_run_by_name(args.reference).document_annotations
    annotator = orbis.get_run_by_name(args.annotator).document_annotations

    annotation_preprocessors: List[AnnotationPreprocessor] = []
    if args.type_blacklist:
        annotation_preprocessors.append(AnnotationTypeFilter(blacklist=tuple(args.type_blacklist)))
    if args.type_whitelist:
        annotation_preprocessors.append(AnnotationTypeFilter(whitelist=tuple(args.type_whitelist)))
    if args.type_priority:
        annotation_preprocessors.append(NormalizeOverlaps(annotation_priority=tuple(args.type_priority)))

    result = []
    for metric in args.metrics:
        if metric not in SUPPORTED_METRICS:
            warn(f'Ignoring unsupported metric: {metric}.')
            continue

        res = SUPPORTED_METRICS[metric].metric(*annotation_preprocessors).compute(reference, annotator)
        result.append(OrbisEvaluationResult(SUPPORTED_METRICS[metric].description, res))

    print(MarkdownOutputFormatter().format_output(result))
