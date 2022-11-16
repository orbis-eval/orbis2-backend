`# orbis2-backend

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


## Corpus import

Import CareerCoach 2022 entity annotations
```bash
./scripts/importer.py --corpus-partition gold_standard_annotation \
     ../education-extraction/corpus/goldDocuments/ \
     careercoach2022-entities.v1  
```

Import CareerCoach 2022 partition annotations
```bash
./scripts/importer.py --corpus-partition gold_standard_annotation_segmentation \
     ../education-extraction/corpus/goldDocuments/ \
     careercoach2022-segments.v1  
```

Import CareerCoach 2022 entity annotations filtered with the page segements
```bash
./scripts/importer.py --corpus-partition gold_standard_annotation \
    --careercoach-filter ../education-extraction/corpus/goldDocumentsPre/ \ 
    ../education-extraction/corpus/goldDocuments/ \  
    careercoach2022-entities.v0 
```

## Evaluation

Compare two runs using with two different metrics:

```bash
./scripts/orbis-eval.py careercoach2022-entities.v1 careercoach2022-entities.v0 --metrics el_oF1
Results for metric 'el_pF1': Entity Linking: Precision, Recall and F1; perfect matching.
    F1Result(mP=1.0, mR=0.5850606179116151, mF1=0.7382186035035776, MP=0.9636363636363636, MR=0.566183898888596, MF1=0.6802433858599718)
Results for metric 'er_oF1': Entity Classification: Precision, Recall and F1; overlapping matching.
    F1Result(mP=1.0, mR=0.5850606179116151, mF1=0.7382186035035776, MP=0.9636363636363636, MR=0.566183898888596, MF1=0.6802433858599718)
```
