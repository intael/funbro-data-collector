# Funbro Data Collector

This project downloads data from whatever sources and makes them available in raw in some persistance storages.

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