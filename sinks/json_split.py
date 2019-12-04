"""Sink data to individual json files."""

import argparse
import json
import pathlib
import string

from pyspark.sql import SparkSession
from slugify import slugify


def pad_collector_number(collector_number):
    """Pad a collector number with zeros and move non-digits to the end."""
    prefix = ""
    core = ""
    suffix = ""
    in_prefix = True
    for i, character in enumerate(collector_number):
        if character in string.digits:
            in_prefix = False
            core += character
        elif in_prefix:
            prefix += character
        else:
            suffix = collector_number[i:]
            break
    padded = f"{prefix}{core:0>5}{suffix}"
    return padded.replace("*", "★")


def get_args():
    """Get cli arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("outdir", help="output directory for json files.")
    return parser.parse_args()


def sink_sets(spark: SparkSession, sets_dir: pathlib.Path):
    """Sink set data to individual json files."""
    sets_dir.mkdir(parents=True, exist_ok=True)
    query = r"""
        SELECT
            *
        FROM
            stg_mtg.sets
    """
    df = spark.sql(query)
    for row in df.toLocalIterator():
        filename = f"{row.code.upper()}_{slugify(row.name)}.json"
        row_dict = row.asDict()

        filepath = sets_dir / filename
        if filepath.exists():
            raise Exception(f"Cannot write duplicate {filepath}")
        with filepath.open("wt") as row_file:
            json.dump(row_dict, row_file, indent=4, sort_keys=True)


def sink_cards(spark: SparkSession, cards_dir: pathlib.Path):
    """Sink card data to individual json files."""
    query = r"""
        SELECT
            pad_collector_number(collector_number) AS padded_collector_number,
            *
        FROM
            stg_mtg.cards
    """
    df = spark.sql(query)
    for row in df.toLocalIterator():
        filename = f"{row.padded_collector_number}_{slugify(row.name)}.json"
        row_dict = row.asDict()
        del row_dict["padded_collector_number"]

        card_set_dir = cards_dir / row.set_code
        card_set_dir.mkdir(parents=True, exist_ok=True)

        filepath = card_set_dir / filename
        if filepath.exists():
            raise Exception(f"Cannot write duplicate {filepath}")
        with filepath.open("wt") as row_file:
            json.dump(row_dict, row_file, indent=4, sort_keys=True)


def main():
    """Main sink function."""
    args = get_args()

    outdir = pathlib.Path(args.outdir)
    sets_dir = outdir / "sets"
    cards_dir = outdir / "cards"

    spark = SparkSession.builder.enableHiveSupport().getOrCreate()
    spark.udf.register("pad_collector_number", pad_collector_number, "string")

    sink_sets(spark, sets_dir)
    sink_cards(spark, cards_dir)


if __name__ == "__main__":
    main()
