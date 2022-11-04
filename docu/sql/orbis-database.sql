CREATE TABLE corpus(
    corpus_id INT PRIMARY KEY,
    name VARCHAR(40) NOT NULL
);

CREATE TABLE run(
    run_id BIGINT PRIMARY KEY,
    name VARCHAR(40) NOT NULL,
    description text,
    corpus_id INT REFERENCES corpus(corpus_id)
);

CREATE TABLE document(
    document_id BIGINT PRIMARY KEY,
    content text NOT NULL,
    key TEXT -- optional external identifier (e.g., a URL, etc.)
);
CREATE INDEX document_text_idx ON document USING GIN(to_tsvector('english', content));

CREATE TABLE annotator(
    annotator_id INT PRIMARY KEY,
    name VARCHAR(40) NOT NULL
);

CREATE TABLE annotation_type(
  type_id INT PRIMARY KEY,
  name TEXT
);

CREATE TABLE annotation(
    annotation_id BIGINT PRIMARY KEY,
    key TEXT,  -- URL/URI to entity, may be NULL
    annotation_type_id INT REFERENCES annotation_type(type_id) NOT NULL,
    annotator_id INT REFERENCES annotator(annotator_id) NOT NULL,
    surface_forms TEXT[] NOT NULL,
    start_indices INT[] NOT NULL,
    end_indices INT[] NOT NULL,
   CHECK (array_length(surface_forms, 1) = array_length(start_indices, 1) AND array_length(start_indices, 1) = array_length(end_indices, 1))
);

CREATE TABLE metadata(
  metadata_id INT PRIMARY KEY,
  key TEXT NOT NULL,
  value TEXT NOT NULL
);

CREATE TABLE role(
    role_id INT PRIMARY KEY
);

-- Relations
CREATE TABLE run_has_document (
    run_id INT REFERENCES run(run_id),
    document_id BIGINT REFERENCES document(document_id),
    done BOOLEAN DEFAULT FALSE,
    PRIMARY KEY(run_id, document_id)
);

CREATE TABLE document_has_annotation(
    document_id BIGINT REFERENCES document(document_id),
    annotation_id BIGINT REFERENCES annotation(annotation_id),
    run_id BIGINT REFERENCES run(run_id),
    timestamp TIMESTAMP DEFAULT now(),
    PRIMARY KEY(document_id, run_id, annotation_id)
);

CREATE TABLE annotator_has_role(
    annotator_id INT REFERENCES annotator(annotator_id),
    role_id INT REFERENCES role(role_id),
    PRIMARY KEY(annotator_id, role_id)
);

CREATE TABLE has_annotation_metadata(
    annotation_id BIGINT REFERENCES annotation(annotation_id),
    metadata_id BIGINT REFERENCES metadata(metadata_id),
    PRIMARY KEY(annotation_id, metadata_id)
);

-- allows to add metadata such as "contains table" to a document
CREATE TABLE has_document_metadata(
    document_id BIGINT REFERENCES document(document_id),
    metadata_id BIGINT REFERENCES metadata(metadata_id),
    PRIMARY KEY(document_id, metadata_id)
);

CREATE TABLE run_derived_from(
    child_id BIGINT REFERENCES run(run_id),
    parent_id BIGINT REFERENCES run(run_id),
    timestamp TIMESTAMP DEFAULT now(),
    PRIMARY KEY(child_id, parent_id)
);

CREATE TABLE corpus_supports_annotation_type(
    corpus_id INT REFERENCES corpus(corpus_id),
    annotation_type INT REFERENCES annotation_type(type_id),
    PRIMARY KEY (corpus_id, annotation_type)
);
