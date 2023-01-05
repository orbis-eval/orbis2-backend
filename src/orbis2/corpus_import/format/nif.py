import json
from typing import List, Dict
from rdflib import Namespace, Graph

from orbis2.corpus_import.format import CorpusFormat
from orbis2.model.annotation import Annotation
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.annotator import Annotator
from orbis2.model.document import Document
from orbis2.model.metadata import Metadata
from orbis2.model.role import Role

SEGMENT_TYPE_PREFIX = 'segment/'

ANNOTATOR = Annotator(name='CorpusImporter', roles=[Role(name='CorpusImporter')])

class CareerCoachFormat(CorpusFormat):
    """
    CorpusFormat used to support imports from the CareerCoach corpus.
    """

    @staticmethod
    def is_supported(document_list: List[str], partition: str):
        try:
            doc = json.loads(document_list[0])
        except json.decoder.JSONDecodeError:
            return False

        for key in 'text', partition:
            if key not in doc:
                return False

        return True

    @staticmethod
    def get_document_annotations(document_list: List[str], invalid_annotation_types: List[str]) \
            -> Dict[Document, List[Annotation]]:
        """
        Return:
            A dictionary of documents and corresponding annotations for import.
        """
        nif_namespace = Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
        its_rdf_namespace = Namespace("http://www.w3.org/2005/11/its/rdf#")

        document_annotations = {}
        for doc in document_list:
            g = Graph()
            g.parse(data=doc, format='turtle')

            

            for doc in map(json.loads, document_list):
                annotations = []
                document_annotations[Document(content=doc['text'], key=doc['url'])] = annotations
                for segment_name, annotation in segment_generator(doc[partition]):
                    if 'type' in annotation:
                        annotation_type = annotation['type']
                    elif 'entity_type' in annotation:
                        annotation_type = annotation['entity_type']
                    else:
                        annotation_type = SEGMENT_TYPE_PREFIX + '/' + segment_name

                    if annotation_type not in invalid_annotation_types:
                        annotations.append(
                            Annotation(key=annotation['key'] if 'key' in annotation and
                                                                annotation_type != 'proposal' else None,
                                       surface_forms=annotation['phrase'] if 'phrase' in annotation else annotation[
                                           'surface_form'],
                                       start_indices=annotation['start'],
                                       end_indices=annotation['end'],
                                       annotation_type=AnnotationType(get_type_or_proposed_type(annotation)),
                                       metadata=(Metadata(key="segment", value=segment_name),),
                                       annotator=ANNOTATOR)
                        )
        return document_annotations

    @staticmethod
    def get_document_content(document_list: List[str]) -> List[Document]:
        pass
