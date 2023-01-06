from typing import List, Dict, Union, Tuple

from rdflib import Namespace, Graph
from rdflib.plugins.parsers.notation3 import BadSyntax
from rdflib.term import Literal, Node

from orbis2.corpus_import.format import CorpusFormat
from orbis2.model.annotation import Annotation
from orbis2.model.annotation_type import AnnotationType
from orbis2.model.annotator import Annotator
from orbis2.model.document import Document
from orbis2.model.metadata import Metadata
from orbis2.model.role import Role

ANNOTATOR = Annotator(name='CorpusImporter', roles=[Role(name='CorpusImporter')])
ENTITY_ANNOTATION_TYPE = AnnotationType(name='Entity')

NIF_NAMESPACE = Namespace("http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#")
ITS_RDF_NAMESPACE = Namespace("http://www.w3.org/2005/11/its/rdf#")


class NifFormat(CorpusFormat):
    """
    CorpusFormat used to support imports from the CareerCoach corpus.
    """

    @staticmethod
    def is_supported(document_list: List[str], partition: str):
        try:
            g = Graph()
            g.parse(data=document_list[0], format='turtle')
        except BadSyntax:
            return False

        return True

    @staticmethod
    def get_document_annotations(document_list: List[str], invalid_annotation_types: List[str], partition=None) \
            -> Dict[Document, List[Annotation]]:
        """
        Return:
            A dictionary of documents and corresponding annotations for import.
        """
        document_annotations = {}
        for nif_document in document_list:
            g = Graph()
            g.parse(data=nif_document, format='turtle')

            for resource, _, value in g.triples((None, NIF_NAMESPACE.isString, None)):
                annotation = []
                document_annotations[Document(content=str(value), key=str(resource))] = annotation
                for annotation_url, _, _ in g.triples((None, NIF_NAMESPACE.referenceContext, None)):
                    metadata = NifFormat.get_annotation_prop(g, annotation_url, ITS_RDF_NAMESPACE.taSource)
                    annotation.append(
                        Annotation(key=NifFormat.get_annotation_prop(g, annotation_url,
                                                                     ITS_RDF_NAMESPACE.taIdentRef),
                                   surface_forms=NifFormat.get_annotation_prop(g, annotation_url,
                                                                               NIF_NAMESPACE.anchorOf,
                                                                               scalar=False),
                                   start_indices=NifFormat.get_annotation_int(g, annotation_url,
                                                                              NIF_NAMESPACE.beginIndex),
                                   end_indices=NifFormat.get_annotation_int(g, annotation_url, NIF_NAMESPACE.endIndex),
                                   metadata=[Metadata(key='Knowledge Base', value=v)
                                             for v in metadata] if metadata else None,
                                   annotation_type=ENTITY_ANNOTATION_TYPE,
                                   annotator=ANNOTATOR
                                   )
                    )
        return document_annotations

    @staticmethod
    def get_annotation_prop(graph: Graph, annotation_url: Node, rdf_property: Literal, scalar: bool = True) -> \
            Union[None | str | List[str]]:
        res = [str(value) for _, _, value in graph.triples((annotation_url, rdf_property, None))]
        if len(res):
            return res[0] if scalar else res
        return None

    @staticmethod
    def get_annotation_int(graph: Graph, annotation_url: Node, rdf_property: Literal) -> Tuple[int, ...]:
        return tuple([int(value) for _, _, value in graph.triples((annotation_url, rdf_property, None))])

    @staticmethod
    def get_document_content(document_list: List[str]) -> List[Document]:
        pass
