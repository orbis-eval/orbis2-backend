from typing import Dict, List, Optional
import datetime

from pydantic import Field
from xxhash import xxh32_intdigest

from orbis2.database.orbis.entities.run_dao import RunDao
from orbis2.model.run import Run
from orbis2.model.annotation import Annotation
from orbis2.model.base_model import OrbisPydanticBaseModel
from orbis2.model.corpus import Corpus
from orbis2.model.document import Document
from orbis2.evaluation.output_formatter.inter_rater_agreement_result import InterRaterAgreementResult

class GoldStandard(Run):
    number_of_runs: int = Field(0, alias="numberOfRuns")
    number_of_documents: int = Field(0, alias="numberOfDocuments")

    def __init__(self, **kwargs):
        number_of_runs = kwargs.pop('number_of_runs', 0)
        number_of_documents = kwargs.pop('number_of_documents', 0)
        super().__init__(**kwargs)
        self.number_of_runs = number_of_runs
        self.number_of_documents = number_of_documents

