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
./scripts/dbtool.py --create-database --force
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
./scripts/importer.py --corpus-partition gold_standard_annotation \
    --careercoach-filter ../education-extraction/corpus/goldDocumentsPre/ \
    --invalid-annotation-type languageSkill languageskill position scope school softskill industry sco  \
    ../education-extraction/corpus/goldDocuments/ \  
    careercoach2022
```

## Corpus export

Export a run with all documents and annotations.
```bash
/scripts/exporter.py careercoach2022 /tmp/cc2022 --export-format careercoach2022
``` 

## Evaluation

Compare two runs using with two different metrics:

```bash
./scripts/orbis-eval.py careercoach2022-entities.v1 careercoach2022-entities.v0 --metrics el_oF1
Results for metric 'er_oF1': Entity Classification: Precision, Recall and F1; overlapping matching.
    F1Result(mP=1.0, mR=0.5850606179116151, mF1=0.7382186035035776, MP=0.9636363636363636, MR=0.566183898888596, MF1=0.6802433858599718)
```

## Annotation workaround for careercoach project
We use the old orbis2 frontend with this backend.
Do the following step to start the services correctly:
0. setup a local PostgreSQL db

  example:
  ```
  sudo docker run --name postgres-server -e POSTGRES_PASSWORD=1234 -v /home/andreas/Projects/ProjectResources/SQL/postgres/:/var/lib/postgres --network host -p 5432:5432 -d postgres
  ```
1. import the CareerCoach 2022 gold documents [see above](Corpus import)
  if you already imported or changed the database and want to start from the beginning: uncomment line 29 & 30 in the importer.py before running it: ```db = OrbisDb()``` ```db.create_database(True)```, but ATTENTION all changes to the db will be lost after this.
2. start the backend by running src/orbis2/api/app.py (when the app.py is started over the pycharm IDE set the Working directory to ```/orbis2-backend/src/orbis2```)
3. checkout [FoW Orbis2](https://git.fhgr.ch/nlp/project/future-of-work/orbis2/-/tree/workaround/NewOrbis2Backend), make sure you change the branch to **```workaround/NewOrbis2Backend```**
4. to correctly run the frontend you need nodejs and npm installed, if not already done you can do it with the following cmds:

  ```sh
  # install node.js using ubuntu
  curl -fsSL https://deb.nodesource.com/setup_19.x | sudo -E bash - &&\
  sudo apt-get install -y nodejs
  node --version
  # output: v19.0.0

  # install the latest npm:
  sudo npm install -g npm
  npm --version
  # output: 8.19.3

  # Yarn is a package manager for your code. It allows you to use and share code with other developers from around the world. Yarn does this quickly, securely, and reliably so you don't ever have to worry.
  # Corepack is included by default with all Node.js installs, but is currently opt-in. To enable it, run the following command:
  sudo corepack enable
  #activate yarn
  sudo corepack prepare yarn@stable --activate
  yarn --version
  # output: 1.22.19
  ```

5. build the frontend:

  ```sh
  cd src/frontend
  npm install
  npm run build
  # copy the generated files to scripts/assets
  cd ../..
  rm -rf scripts/assets
  cp -r src/frontend/dist/* scripts/
  ```

6. run the frontend standalone

  ```sh
  cd src/frontend
  npm run dev
  ```

7. since we're using different ports for the front- and backend we have to start the frontend in a browser with disabled web security (cross side scripting is not allowed per default), for starting chrome you can execute the following cmd:

  ```sh
  nohup google-chrome --disable-web-security --user-data-dir='/tmp' &
  ```

8. go to https://localhost:63011 (link must be copied to the newly opened chrome browser with disabled web security)

9. annotate the documents, some **IMPORTANT** notes:
  1. the documents are shown with the current annotations, each annotation must be approved and the file must be saved only at the end otherwise the annotations which have not been approved get lost
  2. changing documents (next / previous) without saving does not affect anything at the db even when you already approved or added annotations
  3. at the moment the importer imports all documents and all documents are looped through, maybe a user could delete the documents from database he should / must not annotate?
  4. the loop is endless... so when you annotated all documents, ```"nächstes Dokument"``` or ```"speichern & weiter"``` will return the first document again!
  5. THEREFORE: in the logs of the running app.py from orbis2-backend, you get information about the current document index (ex. 5/54)
