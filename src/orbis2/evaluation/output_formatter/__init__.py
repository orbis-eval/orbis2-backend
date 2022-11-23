from collections import namedtuple
from typing import List

OrbisEvaluationResult = namedtuple('OrbisEvaluationResult', 'metric result')


class OutputFormatter:
    """
    Visualizes Orbis evaluation output.
    """

    def format_output(self, result: List[OrbisEvaluationResult]):
        raise NotImplementedError
