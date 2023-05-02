from orbis2.model.annotation import Annotation
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.annotator import Annotator
from orbis2.model.corpus import Corpus
from orbis2.model.document import Document
from orbis2.model.metadata import Metadata
from orbis2.model.role import Role
from orbis2.model.run import Run


def test_pydantic_run():
    """
    Test that we can create the dict object for the given pydantic run type.
    """
    run = Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1')]),
              {Document('Text, das ist ein Beispiel', metadata=[Metadata('key1', 'value1')]):
               [Annotation('', 'Text', 0, 4, AnnotationType('annotation-type1'), Annotator('Andreas', [Role('admin')]),
                           metadata=[Metadata('key1', 'value1')])]})

    from json import dumps
    assert dumps(run.dict())
