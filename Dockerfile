FROM python:3.9-slim-buster

#Configuration
ENV SERVER_PORT=63012

RUN mkdir /src
RUN mkdir /config
RUN mkdir /src/config
RUN mkdir /resources

COPY ./src /src
COPY ./config/logger.ini /config/logger.ini
COPY requirements.txt setup.py ./
WORKDIR .

RUN pip3 install -r requirements.txt
RUN python3 setup.py install

EXPOSE $SERVER_PORT

ENTRYPOINT ["uvicorn", "src.orbis2.api.app:app", "--host", "0.0.0.0", "--port", "63012"]
