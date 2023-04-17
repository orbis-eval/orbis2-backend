from pathlib import Path

from rdflib import Namespace, Graph, Literal, URIRef
from rdflib.namespace import RDF, XSD, OWL

from orbis2.model.run import Run

ORBIS = Namespace('https://www.fhgr.ch/orbis2/2023/export/')
NIF = Namespace('http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#')
ITSRDF = Namespace('http://www.w3.org/2005/11/its/rdf#')


class NifExportFormat:
    """
    CorpusFormat used to support imports from the CareerCoach corpus.
    """

    def __init__(self):
        self.g = Graph()
        self.g.bind('rdf', RDF)
        self.g.bind('nif', NIF)
        self.g.bind('itsrdf', ITSRDF)
        self.g.bind('owl', OWL)
        self.g.bind('xsd', XSD)
        self.g.bind('orbis', ORBIS)

        # define DataTypeProperties
        for res in (NIF.anchorOf, ITSRDF.taIdentRef, NIF.referenceContext, ITSRDF.taSource, NIF.beginIndex,
                    NIF.sourceUrl, NIF.isString, NIF.endIndex, NIF.hasContext):
            self.g.add((res, RDF.type, OWL.DatatypeProperty))

        # define classes
        for res in (NIF.Context, NIF.String, NIF.RFC5147String, NIF.ContextCollection):
            self.g.add((res, RDF.type, OWL.Class))

    def add_document(self, uri: URIRef, source_url: str, content: str) -> None:
        """
        Add a document to the graph.
        """
        # set document classes
        map(self.g.add, ((uri, RDF.type, rdf_type) for rdf_type in (NIF.String, NIF.Context, NIF.RFC5147String,)))

        # properties
        self.g.add((uri, NIF.beginIndex, Literal(0)))
        self.g.add((uri, NIF.endIndex, Literal(len(content))))
        self.g.add((uri, NIF.isString, Literal(content)))
        if source_url:
            self.g.add((uri, NIF.sourceUrl, URIRef(source_url)))

    def add_annotation(self, document_uri, annotation):
        """
        Add an annotation to the given document uri.
        """
        annotation_uri = document_uri.defrag() + f'#{annotation.start_indices[0]},{annotation.end_indices[0]}'
        self.g.add((annotation_uri, RDF.type, NIF.RFC5147String))
        self.g.add((annotation_uri, NIF.anchorOf, Literal(annotation.surface_forms[0])))
        self.g.add((annotation_uri, NIF.beginIndex, Literal(annotation.start_indices[0])))
        self.g.add((annotation_uri, NIF.endIndex, Literal(annotation.end_indices[0])))
        self.g.add((annotation_uri, NIF.referenceContext, document_uri))
        self.g.add((annotation_uri, ITSRDF.taIdentRef, URIRef(annotation.key)))
        if annotation.annotation_type:
            annotation_type = URIRef(annotation.annotation_type.name) \
                if annotation.annotation_type.name.startswith('http://') or annotation.annotation_type.name.startswith(
                'https://') else ORBIS.term('type/' + annotation.annotation_type.name)
            self.g.add((annotation_uri, RDF.type, annotation_type))
            self.g.add((annotation_uri, ITSRDF.taClassRef, annotation_type))
        for metadata in annotation.metadata:
            self.g.add((annotation_uri, URIRef(metadata.key), Literal(metadata.value)))

    def export(self, run: Run, path: Path):
        """
        Export the documents and annotations of the run to a turtle file.

        Args:
            - run: the Run to export.
            - path: Path of the exported file.
        """
        collection_uri = URIRef(ORBIS.term(f'{run.name}'))
        self.g.add((collection_uri, RDF.type, NIF.ContextCollection))
        for document, annotations in run.document_annotations.items():
            # create the document
            uri = ORBIS.term(f'{run.name}/{hash(document)}#char=0,{len(document.content)}')
            self.add_document(uri=uri, source_url=document.key, content=document.content)

            # add the document to the collection
            self.g.add((collection_uri, NIF.hasContext, uri))

            # add annotations
            print(uri)
            for annotation in annotations:
                self.add_annotation(document_uri=uri, annotation=annotation)

        self.g.serialize(path, format='turtle')
