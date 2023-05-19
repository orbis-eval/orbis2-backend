FROM python:3.11-slim-buster

# system packages for building C extensions
RUN apt-get update && \
		apt-get install gcc -y

RUN mkdir /src
RUN mkdir /config
RUN mkdir /src/config
RUN mkdir /resources

COPY ./src /src
COPY ./config/logger.ini /config/logger.ini
COPY requirements.txt setup.py .

RUN pip3 install -r requirements.txt
RUN python3 setup.py install

WORKDIR /app

ENTRYPOINT ["uvicorn", "src.orbis2.api.app:app", "--host", "0.0.0.0", "--port", "63012"]
