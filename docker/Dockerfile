FROM python:3.9

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y postgresql-client

RUN pip install --upgrade pip

RUN useradd -m funbro-data-collector
USER funbro-data-collector
COPY requirements.txt requirements.txt
ENV PATH="/home/funbro-data-collector/.local/bin:${PATH}"
RUN pip install --user -r requirements.txt

WORKDIR /app

COPY . .