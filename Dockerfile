FROM python:3.11-slim-buster

# system packages for building C extensions
RUN apt-get update && \
		apt-get install gcc -y

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

ENTRYPOINT ["uvicorn", "src.orbis2.api.app:app", "--host", "0.0.0.0", "--port", "63012", "--reload"]
