from orbis2.corpus_import.format.nif import NifFormat, ANNOTATOR, ENTITY_ANNOTATION_TYPE
from orbis2.model.annotation import Annotation
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.document import Document
from orbis2.model.metadata import Metadata

DBPEDIA_EN = Metadata(key='http://www.w3.org/2005/11/its/rdf#taSource', value='DBpedia_en_3.9')
DBPEDIA_DE = Metadata(key='http://www.w3.org/2005/11/its/rdf#taSource', value='DBpedia_de_3.9')

COUNTRY_ANNOTATION_TYPE = AnnotationType(name='https://schema.org/Country')

EXAMPLE_NIF = """
@prefix itsrdf: <http://www.w3.org/2005/11/its/rdf#> .
@prefix nif: <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#> .
@prefix orbis: <https://www.fhgr.ch/orbis2/2023/export/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

nif:Context a owl:Class .
nif:String a owl:Class .
nif:ContextCollection a owl:Class .
nif:RFC5147String a owl:Class .
nif:anchorOf a owl:DatatypeProperty .
nif:beginIndex a owl:DatatypeProperty .
nif:endIndex a owl:DatatypeProperty .
nif:hasContext a owl:DatatypeProperty .
nif:isString a owl:DatatypeProperty .
nif:referenceContext a owl:DatatypeProperty .
nif:sourceUrl a owl:DatatypeProperty .
itsrdf:taIdentRef a owl:DatatypeProperty .
itsrdf:taSource a owl:DatatypeProperty .

orbis:reuters a nif:ContextCollection ;
    nif:hasContext 
        <https://www.fhgr.ch/orbis2/2023/export/reuters/1560772437#char=0,1329>,
        <https://www.fhgr.ch/orbis2/2023/export/reuters/2007996992#char=0,130> .
        
<https://www.fhgr.ch/orbis2/2023/export/reuters/2007996992#24,33> a nif:RFC5147String,
        <https://www.w3.org/2002/07/owl#Thing> ;
    nif:anchorOf "Eskey Inc" ;
    nif:beginIndex 24 ;
    nif:endIndex 33 ;
    nif:referenceContext <https://www.fhgr.ch/orbis2/2023/export/reuters/2007996992#char=0,130> ;
    itsrdf:taIdentRef <http://dbpedia.org/resource/Esky> ;
    itsrdf:taSource "DBpedia_en_3.9" .    

<https://www.fhgr.ch/orbis2/2023/export/reuters/1560772437#0,14> a nif:RFC5147String,
        <https://www.w3.org/2002/07/owl#Thing> ;
    nif:anchorOf "Montedison SPA" ;
    nif:beginIndex 0 ;
    nif:endIndex 14 ;
    nif:referenceContext <https://www.fhgr.ch/orbis2/2023/export/reuters/1560772437#char=0,1329> ;
    itsrdf:taIdentRef <http://de.dbpedia.org/resource/Montedison> ;
    itsrdf:taSource "DBpedia_de_3.9" .

<https://www.fhgr.ch/orbis2/2023/export/reuters/1560772437#724,727> a nif:RFC5147String,
        <https://schema.org/Country> ;
    nif:anchorOf "U.S" ;
    nif:beginIndex 724 ;
    nif:endIndex 727 ;
    nif:referenceContext <https://www.fhgr.ch/orbis2/2023/export/reuters/1560772437#char=0,1329> ;
    itsrdf:taIdentRef <http://dbpedia.org/resource/United_States> ;
    itsrdf:taSource "DBpedia_en_3.9" .

<https://www.fhgr.ch/orbis2/2023/export/reuters/1560772437#char=0,1329> nif:beginIndex 0 ;
    nif:endIndex 1329 ;
    nif:isString "Montedison SPA of Italy said net consolidated profit for its Agrimont Group, formed in June 1986, totalled 1.5 billion lire in 1986. Agrimont SPA, the holding company for Montedisons Agro-Industrial businesses, had sales of 810 billion lire and a net profit of about 1.1 billion lire, after amortization costs of 35 billion lire and a 13 billion lire reduction in the value of inventory due to falling market prices, Montedison said. Agrimont, still wholly owned by Montedison, is taking steps to be traded on the Milan exchange, the company said. The company said that 1986 was characterized by an unstable fertlizer market due to the weak dollar and the decline of international prices for products sold in Europe and the U.S where Agrimont operates through its Conserv division. In pesticides and in animal health care products Agrimont maintained its previous level of revenues and market share in 1986, Montedison said. Montedison said it named Ettore dellIsola to the newly created position of president of Agrimont. Montedison also said it named Renato Picco, managing director of Eridania SPA and Gianfranco Ceroni, managing director of Italiana Olii e Sifi, both of whom are members of the the Ferruzzi Groups management board, to Argimonts board of directors. Ferruzzi owns about 40 pct of Montedison, the company said." ;
    nif:sourceUrl <http://www.research.att.com/~lewis/Reuters-21578/15121> .

<https://www.fhgr.ch/orbis2/2023/export/reuters/2007996992#char=0,130> nif:beginIndex 0 ;
    nif:endIndex 130 ;
    nif:isString "Yankee Cos Inc said its Eskey Inc ESK subsidiary has decided not to sell its Yale E. Key unit. Further details were not disclosed." ;
    nif:sourceUrl <http://www.research.att.com/~lewis/Reuters-21578/15138> .
"""


def test_import_nifDump():
    """
    Tests the import of a NIF file into the system.
    """
    document_annotations = NifFormat.get_document_annotations([EXAMPLE_NIF], invalid_annotation_types=[])

    doc1 = Document(content='Montedison SPA of Italy said net consolidated profit for its Agrimont Group, '
                            'formed in June 1986, totalled 1.5 billion lire in 1986. Agrimont SPA, the holding company for Montedisons Agro-Industrial businesses, had sales of 810 billion lire and a net profit of about 1.1 billion lire, after amortization costs of 35 billion lire and a 13 billion lire reduction in the value of inventory due to falling market prices, Montedison said. Agrimont, still wholly owned by Montedison, is taking steps to be traded on the Milan exchange, the company said. The company said that 1986 was characterized by an unstable fertlizer market due to the weak dollar and the decline of international prices for products sold in Europe and the U.S where Agrimont operates through its Conserv division. In pesticides and in animal health care products Agrimont maintained its previous level of revenues and market share in 1986, Montedison said. Montedison said it named Ettore dellIsola to the newly created position of president of Agrimont. Montedison also said it named Renato Picco, managing director of Eridania SPA and Gianfranco Ceroni, managing director of Italiana Olii e Sifi, both of whom are members of the the Ferruzzi Groups management board, to Argimonts board of directors. Ferruzzi owns about 40 pct of Montedison, the company said.',
                    key='http://www.research.att.com/~lewis/Reuters-21578/15121')
    doc2 = Document(
        content='Yankee Cos Inc said its Eskey Inc ESK subsidiary has decided not to sell its Yale E. Key unit. Further details were not disclosed.',
        key='http://www.research.att.com/~lewis/Reuters-21578/15138')

    assert set(document_annotations.keys()) == {doc1, doc2}
    assert set(document_annotations[doc1]) == {Annotation(key='http://de.dbpedia.org/resource/Montedison',
                                                          surface_forms='Montedison SPA',
                                                          start_indices=0,
                                                          end_indices=14,
                                                          annotation_type=ENTITY_ANNOTATION_TYPE,
                                                          annotator=ANNOTATOR,
                                                          metadata=[DBPEDIA_DE]),
                                               Annotation(key='http://dbpedia.org/resource/United_States',
                                                          surface_forms='U.S',
                                                          start_indices=724,
                                                          end_indices=727,
                                                          annotation_type=COUNTRY_ANNOTATION_TYPE,
                                                          annotator=ANNOTATOR,
                                                          metadata=[DBPEDIA_EN])}
    assert document_annotations[doc2] == [Annotation(key='http://dbpedia.org/resource/Esky',
                                                     surface_forms='Eskey Inc',
                                                     start_indices=24,
                                                     end_indices=33,
                                                     annotation_type=ENTITY_ANNOTATION_TYPE,
                                                     annotator=ANNOTATOR,
                                                     metadata=[DBPEDIA_EN]), ]


def test_import_nifDump_with_invalid_annotation_types():
    """
    Test whether specifying invalid annotation types works.
    """
    document_annotations = NifFormat.get_document_annotations([EXAMPLE_NIF],
                                                              invalid_annotation_types=[COUNTRY_ANNOTATION_TYPE.name])
    doc1 = Document(content='Montedison SPA of Italy said net consolidated profit for its Agrimont Group, '
                            'formed in June 1986, totalled 1.5 billion lire in 1986. Agrimont SPA, the holding company for Montedisons Agro-Industrial businesses, had sales of 810 billion lire and a net profit of about 1.1 billion lire, after amortization costs of 35 billion lire and a 13 billion lire reduction in the value of inventory due to falling market prices, Montedison said. Agrimont, still wholly owned by Montedison, is taking steps to be traded on the Milan exchange, the company said. The company said that 1986 was characterized by an unstable fertlizer market due to the weak dollar and the decline of international prices for products sold in Europe and the U.S where Agrimont operates through its Conserv division. In pesticides and in animal health care products Agrimont maintained its previous level of revenues and market share in 1986, Montedison said. Montedison said it named Ettore dellIsola to the newly created position of president of Agrimont. Montedison also said it named Renato Picco, managing director of Eridania SPA and Gianfranco Ceroni, managing director of Italiana Olii e Sifi, both of whom are members of the the Ferruzzi Groups management board, to Argimonts board of directors. Ferruzzi owns about 40 pct of Montedison, the company said.',
                    key='http://www.research.att.com/~lewis/Reuters-21578/15121')

    assert document_annotations[doc1] == [Annotation(key='http://de.dbpedia.org/resource/Montedison',
                                                     surface_forms='Montedison SPA',
                                                     start_indices=0,
                                                     end_indices=14,
                                                     annotation_type=ENTITY_ANNOTATION_TYPE,
                                                     annotator=ANNOTATOR,
                                                     metadata=[DBPEDIA_DE])]


EXAMPLE_NIF_WITHOUT_TYPES = """
@prefix itsrdf: <http://www.w3.org/2005/11/its/rdf#> .
@prefix nif: <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#> .
@prefix orbis: <https://www.fhgr.ch/orbis2/2023/export/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

nif:Context a owl:Class .
nif:String a owl:Class .
nif:anchorOf a owl:DatatypeProperty .
nif:beginIndex a owl:DatatypeProperty .
nif:endIndex a owl:DatatypeProperty .
nif:hasContext a owl:DatatypeProperty .
nif:isString a owl:DatatypeProperty .
nif:referenceContext a owl:DatatypeProperty .
nif:sourceUrl a owl:DatatypeProperty .
itsrdf:taIdentRef a owl:DatatypeProperty .
itsrdf:taSource a owl:DatatypeProperty .

orbis:reuters a nif:ContextCollection ;
    nif:hasContext 
        <https://www.fhgr.ch/orbis2/2023/export/reuters/1560772437#char=0,1329>,
        <https://www.fhgr.ch/orbis2/2023/export/reuters/2007996992#char=0,130> .

<https://www.fhgr.ch/orbis2/2023/export/reuters/2007996992#24,33> a nif:RFC5147String;
    nif:anchorOf "Eskey Inc" ;
    nif:beginIndex 24 ;
    nif:endIndex 33 ;
    nif:referenceContext <https://www.fhgr.ch/orbis2/2023/export/reuters/2007996992#char=0,130> ;
    itsrdf:taIdentRef <http://dbpedia.org/resource/Esky> ;
    itsrdf:taSource "DBpedia_en_3.9" .    

<https://www.fhgr.ch/orbis2/2023/export/reuters/2007996992#char=0,130> nif:beginIndex 0 ;
    nif:endIndex 130 ;
    nif:isString "Yankee Cos Inc said its Eskey Inc ESK subsidiary has decided not to sell its Yale E. Key unit. Further details were not disclosed." ;
    nif:sourceUrl <http://www.research.att.com/~lewis/Reuters-21578/15138> .
"""


def test_import_nifDump_without_annotation_types():
    document_annotations = NifFormat.get_document_annotations([EXAMPLE_NIF_WITHOUT_TYPES], invalid_annotation_types=[])
    doc = Document(
        content='Yankee Cos Inc said its Eskey Inc ESK subsidiary has decided not to sell its Yale E. Key unit. Further details were not disclosed.',
        key='http://www.research.att.com/~lewis/Reuters-21578/15138')

    assert list(document_annotations.keys()) == [doc]
    assert document_annotations[doc] == [Annotation(key='http://dbpedia.org/resource/Esky',
                                                    surface_forms='Eskey Inc',
                                                    start_indices=24,
                                                    end_indices=33,
                                                    annotation_type=ENTITY_ANNOTATION_TYPE,
                                                    annotator=ANNOTATOR,
                                                    metadata=[DBPEDIA_EN]), ]
