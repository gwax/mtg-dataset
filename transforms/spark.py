"""Common spark configuration."""

import multiprocessing
import os

from pyspark.sql import SparkSession
from pyspark.sql.types import DateType


def get_dataframes():
    workspace_dir = os.path.join(os.path.dirname(__file__), "..")
    build_dir = os.path.join(workspace_dir, "build")
    hive_dir = os.path.join(build_dir, "hive")
    jsonl_dir = os.path.join(build_dir, "jsonl")
    librarities_cards_jsonl = os.path.join(jsonl_dir, "librarities", "cards.jsonlines")
    scryall_cards_jsonl = os.path.join(jsonl_dir, "scryfall", "cards.jsonlines")
    scryall_sets_jsonl = os.path.join(jsonl_dir, "scryfall", "sets.jsonlines")

    cores = multiprocessing.cpu_count()

    spark = (
        SparkSession.builder.appName("mtg-dataset")
        .master(f"local[{cores}]")
        .config("spark.sql.warehouse.dir", os.path.abspath(hive_dir))
        .enableHiveSupport()
        .getOrCreate()
    )

    raritiesDF = spark.read.json(librarities_cards_jsonl)
    raritiesDF = raritiesDF.withColumn(
        "release_date", raritiesDF["release_date"].cast(DateType())
    )

    scryfallCardsDF = spark.read.json(scryall_cards_jsonl)
    scryfallCardsDF = scryfallCardsDF.withColumn(
        "released_at", scryfallCardsDF["released_at"].cast(DateType())
    )

    scryfallSetsDF = spark.read.json(scryall_sets_jsonl)
    scryfallSetsDF = scryfallSetsDF.withColumn(
        "released_at", scryfallSetsDF["released_at"].cast(DateType())
    )
    return raritiesDF, scryfallCardsDF, scryfallSetsDF
