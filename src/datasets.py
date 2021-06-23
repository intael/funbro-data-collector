from enum import auto

from cli.cli_parsable import CLIParsableEnum


class Dataset(CLIParsableEnum):
    ...


class ImdbDailyUpdatedDataset(Dataset):
    ALL = auto()
    NAME_BASICS = "https://datasets.imdbws.com/name.basics.tsv.gz"
    TITLE_AKAS = "https://datasets.imdbws.com/title.akas.tsv.gz"
    TITLE_BASICS = "https://datasets.imdbws.com/title.basics.tsv.gz"
    TITLE_CREW = "https://datasets.imdbws.com/title.crew.tsv.gz"
    TITLE_EPISODE = "https://datasets.imdbws.com/title.episode.tsv.gz"
    TITLE_PRINCIPALS = "https://datasets.imdbws.com/title.principals.tsv.gz"
    TITLE_RATINGS = "https://datasets.imdbws.com/title.ratings.tsv.gz"
