import sys
from pathlib import Path

try:
    orbis_src = Path(__file__).parent.parent / 'src'
    if orbis_src.is_dir():
        sys.path.append(str(orbis_src))
except IndexError:
    pass

from orbis2.model.annotation import Annotation
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.annotator import Annotator
from orbis2.model.corpus import Corpus
from orbis2.model.document import Document
from orbis2.model.metadata import Metadata
from orbis2.model.role import Role
from orbis2.model.run import Run

GOLD_STANDARD = Run(
    'gold-standard', 'Gold Standard', Corpus('corpus1', [AnnotationType('annotation-type1'),
                                                      AnnotationType('annotation-type2')]),
    {
        Document('Text, das ist ein Beispiel', metadata=[Metadata('key1', 'value1')]):
            [Annotation('url', 'Text', 0, 4, AnnotationType('annotation-type1'),
                        Annotator('Andreas', [Role('admin')]), metadata=[Metadata('key2', 'value2')])],
        Document('Text, das ist ein anderes Beispiel, mit etwas mehr Text.', metadata=[Metadata('key3', 'value3')]):
            [Annotation('url', 'Text', 0, 4, AnnotationType('annotation-type1'),
                        Annotator('Andreas', [Role('admin')]), metadata=[Metadata('key2', 'value2')]),
             Annotation('url', 'Text', 51, 55, AnnotationType('annotation-type1'),
                        Annotator('Andreas', [Role('admin')]), metadata=[Metadata('key2', 'value2')])]
    },
    is_gold_standard=True
)

FIRST_RUN = Run(
    'first-run', 'run number one', Corpus('corpus1', [AnnotationType('annotation-type1'),
                                                      AnnotationType('annotation-type2')]),
    {
        Document('Text, das ist ein Beispiel', metadata=[Metadata('key1', 'value1')]):
            [Annotation('url', 'Text', 0, 4, AnnotationType('annotation-type1'),
                        Annotator('Andreas', [Role('admin')]), metadata=[Metadata('key2', 'value2')])],
        Document('Text, das ist ein anderes Beispiel, mit etwas mehr Text.', metadata=[Metadata('key3', 'value3')]):
            [Annotation('url', 'Text', 0, 4, AnnotationType('annotation-type1'),
                        Annotator('Andreas', [Role('admin')]), metadata=[Metadata('key2', 'value2')]),
             Annotation('url', 'Text', 51, 55, AnnotationType('annotation-type1'),
                        Annotator('Andreas', [Role('admin')]), metadata=[Metadata('key2', 'value2')])]
    }
)

SECOND_RUN = Run(
    'second-run', 'run number two', Corpus('corpus1', [AnnotationType('annotation-type1'),
                                                       AnnotationType('annotation-type2')]),
    {
        Document('Text, das ist ein Beispiel', metadata=[Metadata('key1', 'value1')]):
            [Annotation('url', 'Text', 0, 4, AnnotationType('annotation-type1'),
                        Annotator('Norman', [Role('annotator')]), metadata=[Metadata('key2', 'value2')]),
             Annotation('url', 'Beispiel', 18, 26, AnnotationType('annotation-type2'),
                        Annotator('Norman', [Role('annotator')]), metadata=[Metadata('key2', 'value2')])],
        Document('Text, das ist ein anderes Beispiel, mit etwas mehr Text.', metadata=[Metadata('key3', 'value3')]):
            [Annotation('url', 'Text', 0, 4, AnnotationType('annotation-type1'),
                        Annotator('Norman', [Role('annotator')]), metadata=[Metadata('key2', 'value2')]),
             Annotation('url', 'Beispiel', 26, 34, AnnotationType('annotation-type2'),
                        Annotator('Norman', [Role('annotator')]), metadata=[Metadata('key2', 'value2')]),
             Annotation('url', 'Text', 51, 55, AnnotationType('annotation-type1'),
                        Annotator('Norman', [Role('annotator')]), metadata=[Metadata('key2', 'value2')])]
    }
)

ANOTHER_GOLD_STANDARD = Run(
    'another gold standard', 'a different gold standdard', Corpus('corpus2', [AnnotationType('annotation-type1'),
                                                         AnnotationType('annotation-type2'),
                                                         AnnotationType('annotation-type3')]),
    {
        Document('Ein komplett anderer Text. Er enthält sogar zwei Sätze.', metadata=[Metadata('key1', 'value1')]):
            [Annotation('url', 'Text', 21, 25, AnnotationType('annotation-type1'),
                        Annotator('Andreas', [Role('admin')]), metadata=[Metadata('key2', 'value2')]),
             Annotation('url', 'Sätze', 49, 54, AnnotationType('annotation-type3'),
                        Annotator('Andreas', [Role('admin')]), metadata=[Metadata('key2', 'value2')])],
        Document('Ein zweites neues Dokumnet. Auch das enthält zwei Sätze.', metadata=[Metadata('key3', 'value3')]):
            [Annotation('url', 'Dokument', 18, 26, AnnotationType('annotation-type1'),
                        Annotator('Norman', [Role('annotator')]), metadata=[Metadata('key2', 'value2')]),
             Annotation('url', 'Sätze', 50, 55, AnnotationType('annotation-type3'),
                        Annotator('Norman', [Role('annotator')]), metadata=[Metadata('key2', 'value2')]), ]
    },
    is_gold_standard=True
)

ANOTHER_RUN = Run(
    'another run', 'a different run', Corpus('corpus2', [AnnotationType('annotation-type1'),
                                                         AnnotationType('annotation-type2'),
                                                         AnnotationType('annotation-type3')]),
    {
        Document('Ein komplett anderer Text. Er enthält sogar zwei Sätze.', metadata=[Metadata('key1', 'value1')]):
            [Annotation('url', 'Text', 21, 25, AnnotationType('annotation-type1'),
                        Annotator('Andreas', [Role('admin')]), metadata=[Metadata('key2', 'value2')]),
             Annotation('url', 'Sätze', 49, 54, AnnotationType('annotation-type3'),
                        Annotator('Andreas', [Role('admin')]), metadata=[Metadata('key2', 'value2')])],
        Document('Ein zweites neues Dokumnet. Auch das enthält zwei Sätze.', metadata=[Metadata('key3', 'value3')]):
            [Annotation('url', 'Dokument', 18, 26, AnnotationType('annotation-type1'),
                        Annotator('Norman', [Role('annotator')]), metadata=[Metadata('key2', 'value2')]),
             Annotation('url', 'Sätze', 50, 55, AnnotationType('annotation-type3'),
                        Annotator('Norman', [Role('annotator')]), metadata=[Metadata('key2', 'value2')]), ]
    }
)
