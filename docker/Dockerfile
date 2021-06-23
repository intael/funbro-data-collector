FROM python:3.9

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y postgresql-client

RUN pip install --upgrade pip

RUN useradd -m funbro-data-collector
USER funbro-data-collector
COPY --chown=funbro-data-collector:funbro-data-collector requirements.txt requirements.txt
RUN pip install --user -r requirements.txt
ENV PATH="/home/funbro-data-collector/.local/bin:${PATH}"
COPY --chown=funbro-data-collector:funbro-data-collector . .

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt --user
