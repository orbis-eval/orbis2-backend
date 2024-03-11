from orbis2.database.orbis.entities.run_dao import RunDao
from orbis2.model.annotation import Annotation
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.annotator import Annotator
from orbis2.model.corpus import Corpus
from orbis2.model.document import Document
from orbis2.model.role import Role
from orbis2.model.run import Run


# noinspection PyPep8Naming
def test_run_getAnnotationsByNewDocument_returnCorrectAnnotations():
    run = Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1'),
                                                 AnnotationType('annotation-type2')]),
              {Document('Text, das ist ein Beispiel'):
                   [Annotation('', 'Text', 0, 4, AnnotationType('annotation-type1'),
                               Annotator('Andreas', [Role('admin')])),
                    Annotation('', 'Beispiel', 18, 26, AnnotationType('annotation-type2'),
                               Annotator('Andreas', [Role('admin')]))],
               Document('Text2, das ist ein neues Beispiel2'):
                   [Annotation('', 'Text2', 0, 5, AnnotationType('annotation-type1'),
                               Annotator('Andreas', [Role('admin')])),
                    Annotation('', 'Beispiel2', 25, 34, AnnotationType('annotation-type2'),
                               Annotator('Andreas', [Role('admin')]))]
               }
              )
    assert run.document_annotations[Document('Text, das ist ein Beispiel')][0].surface_forms[0] == 'Text'
    assert run.document_annotations[Document('Text2, das ist ein neues Beispiel2')][0].surface_forms[0] == 'Text2'


# noinspection PyPep8Naming
def test_run_getAnnotationsByExistingDocument_returnCorrectAnnotations():
    document1 = Document('Text, das ist ein Beispiel')
    document2 = Document('Text2, das ist ein neues Beispiel2')
    run = Run('Run1', 'Run1', Corpus('Corpus1', [AnnotationType('annotation-type1'),
                                                 AnnotationType('annotation-type2')]),
              {document1:
                   [Annotation('', 'Text', 0, 4, AnnotationType('annotation-type1'),
                               Annotator('Andreas', [Role('admin')])),
                    Annotation('', 'Beispiel', 18, 26, AnnotationType('annotation-type2'),
                               Annotator('Andreas', [Role('admin')]))],
               document2:
                   [Annotation('', 'Text2', 0, 5, AnnotationType('annotation-type1'),
                               Annotator('Andreas', [Role('admin')])),
                    Annotation('', 'Beispiel2', 25, 34, AnnotationType('annotation-type2'),
                               Annotator('Andreas', [Role('admin')]))]
               }
              )
    assert run.document_annotations[document1][0].surface_forms[0] == 'Text'
    assert run.document_annotations[document2][0].surface_forms[0] == 'Text2'


# noinspection PyPep8Naming
def test_from_run_dao_nameOnly_validRun():
    test = 'test'
    run_dao = RunDao(name=test, is_gold_standard=False)
    run = Run.from_run_dao(run_dao)
    assert run.name == test
    assert run.identifier is not None
