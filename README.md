# Funbro Data Collector

This project downloads data from whatever sources and makes it available in some persistance storage.

### Credentials

The project relies on a number of credentials to be available at runtime. Some of them are just environment variables
and some are files expected at a given path.

In order to make these credentials available at runtime, just fill the `.env*` files present at then root of the
project.

Actual file credentials are git/docker-ignored, but `.env*` files are not for convenience. The `.env` file, which
contains production env variables, has some of its keys empty so they are easily filled if needed. In case of being
filled, do remember not to version control the changes!

### Running it

```shell
docker-compose run funbro-data-collector python -m src IMDB_DAILY --dataset ALL
```

Or just modify the arguments in the makefile and run:

```shell
make run
```

You can ask for help to see what's available:

```shell
docker-compose run funbro-data-collector python --help
```

Each data source can potentially accept different arguments. You can check that invoking its sub-argument parser:

```shell
docker-compose run funbro-data-collector python IMDB_DAILY --help
```

### Development

You can make available a local database and force it rebuild running:

```shell
make rebuild_db
```

Run the tests like so:

```shell
make test
```

Run the static code analyzer:

```shell
make mypy
```
