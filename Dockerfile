FROM python:3.11-slim-buster

# system packages for building C extensions
RUN apt-get update && \
		apt-get install gcc -y

COPY ./src /src
COPY ./scripts /scripts
COPY ./config /config
COPY ./requirements.txt /requirements.txt
COPY ./setup.py /setup.py

WORKDIR .

RUN pip3 install -r requirements.txt
RUN python3 setup.py install

ENTRYPOINT ["uvicorn", "src.orbis2.api.app:app", "--host", "0.0.0.0", "--port", "63012", "--reload"]
