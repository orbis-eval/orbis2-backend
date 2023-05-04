#!/usr/bin/env python3

import streamlit as st
from annotated_text import annotated_text
from pickle import load


def annnotate_document(document, document_annotations):
    text = document.content.replace("\n", " ")
    content_idx = 0

    annotated_content = []
    for annotation in sorted(document_annotations[document], key=lambda x: x.start_indices[0]):
        prefix = text[content_idx:annotation.start_indices[0]]

        annotated_content.append(prefix)
        annotated_content.append((text[annotation.start_indices[0]:annotation.end_indices[0]],
                                  annotation.annotation_type.name))
        content_idx = annotation.end_indices[0]

    return annotated_content


st.write("## Orbis Evaluation")

with open('../test.dump', 'rb') as f:
    obj = load(f)
    ref_documents = list(obj['reference'].keys())

filter_text = ''
documents = [r for r in ref_documents if not filter_text or filter_text in r.content]
selected = st.number_input('Pick a document', 0, len(documents) - 1)

reference, annotator = st.columns(2)
with reference:
    st.header("Reference")
    annotated = annnotate_document(documents[selected], obj['reference'])
    annotated_text(*annotated)

with annotator:
    st.header("Annotator")
    annotated = annnotate_document(documents[selected], obj['annotator'])
    annotated_text(*annotated)
