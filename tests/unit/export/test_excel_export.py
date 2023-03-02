from orbis2.corpus_export.excel import ExcelFormat
from orbis2.corpus_import.format.careercoach import ANNOTATOR
from orbis2.corpus_import.format.nif import ENTITY_ANNOTATION_TYPE
from orbis2.model.annotation import Annotation
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.document import Document

COUNTRY_ANNOTATION_TYPE = AnnotationType(name='https://schema.org/Country')


def get_document_annotations():
    doc1 = Document(content='Montedison SPA of Italy said net consolidated profit for its Agrimont Group, '
                            'formed in June 1986, totalled 1.5 billion lire in 1986. Agrimont SPA, the holding company for Montedisons Agro-Industrial businesses, had sales of 810 billion lire and a net profit of about 1.1 billion lire, after amortization costs of 35 billion lire and a 13 billion lire reduction in the value of inventory due to falling market prices, Montedison said. Agrimont, still wholly owned by Montedison, is taking steps to be traded on the Milan exchange, the company said. The company said that 1986 was characterized by an unstable fertlizer market due to the weak dollar and the decline of international prices for products sold in Europe and the U.S where Agrimont operates through its Conserv division. In pesticides and in animal health care products Agrimont maintained its previous level of revenues and market share in 1986, Montedison said. Montedison said it named Ettore dellIsola to the newly created position of president of Agrimont. Montedison also said it named Renato Picco, managing director of Eridania SPA and Gianfranco Ceroni, managing director of Italiana Olii e Sifi, both of whom are members of the the Ferruzzi Groups management board, to Argimonts board of directors. Ferruzzi owns about 40 pct of Montedison, the company said.',
                    key='http://www.research.att.com/~lewis/Reuters-21578/15121')
    doc2 = Document(
        content='Yankee Cos Inc said its Eskey Inc ESK subsidiary has decided not to sell its Yale E. Key unit. Further details were not disclosed.',
        key='http://www.research.att.com/~lewis/Reuters-21578/15138')

    return ((doc1, [Annotation(key='http://de.dbpedia.org/resource/Montedison',
                               surface_forms='Montedison SPA',
                               start_indices=0,
                               end_indices=14,
                               annotation_type=ENTITY_ANNOTATION_TYPE,
                               annotator=ANNOTATOR),
                    Annotation(key='http://dbpedia.org/resource/United_States',
                               surface_forms=('U.S', 'U.S.'),
                               start_indices=(724, 730),
                               end_indices=(727, 733),
                               annotation_type=COUNTRY_ANNOTATION_TYPE,
                               annotator=ANNOTATOR)]),
            (doc2, [Annotation(key='http://dbpedia.org/resource/Esky',
                               surface_forms='Eskey Inc',
                               start_indices=24,
                               end_indices=33,
                               annotation_type=ENTITY_ANNOTATION_TYPE,
                               annotator=ANNOTATOR), ]))


def test_get_annotation_property():
    """
    Test whether annotation property returns the correct entries.
    """
    document_annotation1, document_annotation2 = get_document_annotations()
    assert ExcelFormat.get_annotation_property(document_annotation1[1], 'start_indices') == '0; 724, 730'
    assert ExcelFormat.get_annotation_property(document_annotation2[1], 'start_indices') == '24'

    # surface forms
    assert ExcelFormat.get_annotation_property(document_annotation1[1], 'surface_forms') == 'Montedison SPA; U.S, U.S.'

    # annotation type
    assert ExcelFormat.get_annotation_property(document_annotation1[1], 'annotation_type') == (
        'https://www.w3.org/2002/07/owl#Thing; https://schema.org/Country')
