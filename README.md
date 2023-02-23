# orbis2-backend

## Setup Development Environment

### Prerequisites

- Python 3.9
- PostgreSQL 15.0

### Run the API


### Environment variables

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

Import CareerCoach 2022 entity annotations
```bash
./scripts/importer.py --corpus-partition gold_standard_annotation \
     ../education-extraction/corpus/goldDocuments/ \
     careercoach2022  
```

Import CareerCoach 2022 partition annotations
```bash
./scripts/importer.py --corpus-partition gold_standard_annotation_segmentation \
     ../education-extraction/corpus/goldDocuments/ \
     careercoach2022
```

Import CareerCoach 2022 entity annotations filtered by the page segments
```bash
./scripts/importer.py ../education-extraction/corpus/goldDocuments/ careercoach2022 \
    --corpus-partition gold_standard_annotation \
    --careercoach-filter ../education-extraction/corpus/goldDocumentsPre/ \
    --invalid-annotation-type languageSkill languageskill position scope school softskill industry sco
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
