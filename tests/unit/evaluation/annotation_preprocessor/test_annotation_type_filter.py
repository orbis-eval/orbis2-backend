from orbis2.evaluation.annotation_preprocessor.annotation_filter import AnnotationTypeFilter
from orbis2.model.annotation import get_mock_annotation as Annotation


def test_annotation_type_filter_blacklist():
    type_filter = AnnotationTypeFilter(blacklist=('languageskill', 'languageSkill', 'position', 'scope', 'school',
                                                  'softskill', 'industry', 'sco'))
    annotations = [Annotation(1, 2, annotation_type=annotation_type)
                   for annotation_type in ('topic', 'topic', 'position', 'sco', 'occupation')]

    assert type_filter.preprocess(annotations) == [Annotation(1, 2, annotation_type=annotation_type)
                                                   for annotation_type in ('topic', 'topic', 'occupation')]


def test_annotation_type_filter_whitelist():
    type_filter = AnnotationTypeFilter(whitelist=('languageskill', 'languageSkill', 'position', 'scope', 'school',
                                                  'softskill', 'industry', 'sco'))
    annotations = [Annotation(1, 2, annotation_type=annotation_type)
                   for annotation_type in ('topic', 'topic', 'position', 'sco', 'occupation')]

    assert type_filter.preprocess(annotations) == [Annotation(1, 2, annotation_type=annotation_type)
                                                   for annotation_type in ('position', 'sco')]
