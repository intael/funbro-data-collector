FROM python:3.10

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y postgresql-client

RUN useradd -m funbro-data-collector && \
    mkdir /app && \
    chown funbro-data-collector app
USER funbro-data-collector
WORKDIR /app
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
ENV PATH="/home/funbro-data-collector/.local/bin:${PATH}"
RUN pip install --user -r requirements.txt

COPY . .