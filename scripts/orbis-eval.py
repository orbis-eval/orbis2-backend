#!/usr/bin/env python3
from warnings import warn

from orbis2.business_logic.orbis_service import OrbisService
from orbis2.evaluation.metric import SUPPORTED_METRICS
from orbis2.evaluation.output_formatter import OrbisEvaluationResult
from orbis2.evaluation.output_formatter.markdown import MarkdownOutputFormatter

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('reference', help='The run containing the annotations considered to be true, i.e., '
                                          'the gold standard.')
    parser.add_argument('annotator', help='The annotator run, i.e. the predicted annotations.')
    parser.add_argument('--metrics', nargs='+', help='The metrics to compute')
    args = parser.parse_args()

    orbis = OrbisService()
    reference = orbis.get_run_by_name(args.reference).document_annotations
    annotator = orbis.get_run_by_name(args.annotator).document_annotations

    result = []
    for metric in args.metrics:
        if metric not in SUPPORTED_METRICS:
            warn(f'Ignoring unsupported metric: {metric}.')
            continue

        res = SUPPORTED_METRICS[metric].metric.compute(reference, annotator)
        result.append(OrbisEvaluationResult(SUPPORTED_METRICS[metric].description, res))

    print(MarkdownOutputFormatter().format_output(result))