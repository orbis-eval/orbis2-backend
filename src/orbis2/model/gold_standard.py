from pydantic import Field

from orbis2.model.run import Run


class GoldStandard(Run):
    number_of_runs: int = Field(0, alias="numberOfRuns")
    number_of_documents: int = Field(0, alias="numberOfDocuments")

    def __init__(self, **kwargs):
        number_of_runs = kwargs.pop('number_of_runs', 0)
        number_of_documents = kwargs.pop('number_of_documents', 0)
        super().__init__(**kwargs)
        self.number_of_runs = number_of_runs
        self.number_of_documents = number_of_documents
