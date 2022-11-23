from collections import namedtuple
from typing import List

from orbis2.evaluation.output_formatter import OutputFormatter, OrbisEvaluationResult


class MarkdownOutputFormatter(OutputFormatter):

    def __init__(self, precision=2):
        self.format_string = f'{{0:.{precision}f}}'

    def format_metric_heading(self, metric: namedtuple):
        return ' | '.join(metric._fields) + '|'

    def format_metric_result(self, metric: namedtuple):
        return ' | '.join([self.format_string.format(getattr(metric, field)) for field in metric._fields ]) + '|'

    def format_output(self, result: List[OrbisEvaluationResult]):
        if not result:
            return

        out = [
            '| Metric |' + self.format_metric_heading(result[0].result),
            ('| --- ' * len(result[0].result._fields) + '|')
        ]
        for res in result:
            out.append(f'|{res.metric}|' + self.format_metric_result(res.result))

        return '\n'.join(out)
