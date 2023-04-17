# orbis2-backend

## Setup Development Environment

### Prerequisites

- Python 3.9 - PostgreSQL 15.0

## Run the API


### Database setup and environment variables

Setup the following databases:

1. orbis (used for production)
2. orbis_test (used in unit tests)

The environment variables are all stored in the file [src/orbis2/config/app_config.py](src/orbis2/config/app_config.py) during run time.

| Name                        | Description           | Default            |
| :----                       |:----------------------|:-------------------|
| DB_URL                      |                       | localhost          |
| DB_PORT                     |                       | 5432               |
| DB_USER                     |                       | postgres           |
| DB_PASSWORD                 |                       |                    |
| ORBIS_DB_NAME               |                       | orbis              |


## (Re)initialize the Orbis database

```bash
./scripts/dbtool.py --create-database --force --add-dummy-data
```

## Corpus import

### Local corpus

Import the NIF corpus `KORE50.ttl` to the run (i.e., AnnotatedCorpus) `KORE50-version1.0`.
```bash
./scripts/importer.py local KORE50.ttl KORE50-version1.0
```

Import CareerCoach 2022 entity annotations
```bash
./scripts/importer.py local --corpus-partition gold_standard_annotation \
     ../education-extraction/corpus/goldDocuments/ \
     careercoach2022  
```

Import CareerCoach 2022 partition annotations
```bash
./scripts/importer.py local --corpus-partition gold_standard_annotation_segmentation \
     ../education-extraction/corpus/goldDocuments/ \
     careercoach2022
```

Import CareerCoach 2022 entity annotations filtered by the page segments
```bash
./scripts/importer.py local ../education-extraction/corpus/goldDocuments/ careercoach2022 \
    --corpus-partition gold_standard_annotation \
    --careercoach-filter ../education-extraction/corpus/goldDocumentsPre/ \
    --invalid-annotation-type languageSkill languageskill position scope school softskill industry sco
```

### Remote corpus

The Orbis import tool also supports importing remote corpora that have been published by the 
[GERBIL](https://github.com/dice-group/gerbil) project.

The `list-remote` command provides a list of all available corpora.
```bash
./scripts/importer.py list-remote
```

The `remote` command imports a given corpus into the specified run (`N3-Reuters-128-version1` in the example below).
```bash
./scripts/importer.py remote N3-Reuters-128 N3-Reuters-128-version1
```

## Corpus export

Export a run with all documents and annotations.
```bash
/scripts/exporter.py careercoach2022 /tmp/cc2022 --export-format careercoach2022
```

## Evaluation

Compare two runs using with two different metrics:

```bash
./scripts/orbis-eval.py --reference careercoach2022-entities.v1 careercoach2022-entities.v0 --metrics el_oF1
Results for metric 'er_oF1': Entity Classification: Precision, Recall and F1; overlapping matching.
    F1Result(mP=1.0, mR=0.5850606179116151, mF1=0.7382186035035776, MP=0.9636363636363636, MR=0.566183898888596, MF1=0.6802433858599718)
```

Notes:
- if the metric benchmarks against a gold standard, you need to use the `--reference` parameter to specify the gold standard run.
- symmetric metrics such as the inter-rater-agreement may specify more than two runs (e.g., to compute the inter-rater-agreement for more than two raters).


## Inter-rater-agreement

Compute the Inter-Rater-Agreement between the provided evaluation runs (i.e., annotated corpora) using the following metrics:
- average macro F1 and micro F1 between the raters 
- a modified kappa score which does not correct for random matches, since they are extremely unlikely in an annotation setting. 


```bash
./scripts/orbis-eval.py --metrics er_pIRR -- careercoach2022.v1 careercoach2022.v2
```

| Metric | kappa_micro | kappa_macro | average_macro_f1 | average_micro_f1 |
|-----|-----|-----|-----|-----|
| Entity Recognition: Inter Rater Agreement; perfect matching.|0.54 | 0.53 | 0.68 | 0.65|



## New API Calls


### Next and previous document support:

1. `get_next_document(run_id: int, document_id: int) -> Union[Document, None]`: retrieve the next document
2. `get_previous_document(run_id: int, document_id: int) -> Union[Document, None]`: retrieve the previous document


### Color support:

1. `get_color_palettes() -> List[ColorPalette]`: available color palettes which contain a name + a list of colors
2. `get_corpus_annotation_types(corpus_id: int) > Dict[AnnotationType, int]`: a dictionary of AnnotationTypes and the corresponding `color_id`. The color to use is computed by 
     ```python
     color_index = color_id % len(color_palette)
     color = color_palette[color_index]
     ```
3. `set_corpus_annotation_type_color(corpus_id: int, annotation_type_id: int, color_id: int)`: sets a color for a given corpus and `annotation_type`.
