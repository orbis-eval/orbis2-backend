from orbis2.evaluation.scorer.annotation_processor_util import tokenize
from orbis2.model.annotation import get_mock_annotation as a

def test_token_annotation_tokenizedAnnotation():
    annotation = [a(10, 38, 'Grosser Gott wir loben dich!'),
                  a(40, 70, 'Herr, wir rühmen deine Stärke!')]
    tokenized = tokenize(annotation)

    print(tokenized)
    assert tokenized == [a(10, 17, 'Grosser'),
                         a(18, 22, 'Gott'),
                         a(23, 26, 'wir'),
                         a(27, 32, 'loben'),
                         a(33, 38, 'dich!'),
                         a(40, 45, 'Herr,'),
                         a(46, 49, 'wir'),
                         a(50, 56, 'rühmen'),
                         a(57, 62, 'deine'),
                         a(63, 70, 'Stärke')]