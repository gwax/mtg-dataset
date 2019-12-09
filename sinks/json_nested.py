"""Sink data to per-set json with nested card arrays."""

import argparse
import json
import pathlib
import string
from typing import Tuple, Any, Dict

from pyspark.sql import SparkSession
from pyspark.sql.types import Row
from slugify import slugify

QUERY = """\
WITH
set_cards AS (
SELECT
    set_code,
    COLLECT_LIST(STRUCT(*)) AS cards
FROM
    stg_mtg.cards
GROUP BY
    set_code
)

SELECT
    sets.*,
    set_cards.cards
FROM
    stg_mtg.sets AS sets
    JOIN set_cards
        ON sets.code = set_cards.set_code
"""


def card_sort_key(card: Row) -> Tuple[str, int, str]:
    """Deterministic collector number based sort key for cards."""
    prefix = ""
    core = ""
    suffix = ""
    in_prefix = True
    for i, rune in enumerate(card.collector_number):
        if rune in string.digits:
            in_prefix = False
            core += rune
        elif in_prefix:
            prefix += rune
        else:
            suffix = card.collector_number[i:]
    prefix = prefix.replace("★", "*")
    suffix = suffix.replace("★", "*")
    return (prefix, int(core), suffix)


def sink(spark: SparkSession, outdir: pathlib.Path) -> None:
    """Sink set data with nest cards to json files."""
    outdir.mkdir(parents=True, exist_ok=True)
    dataframe = spark.sql(QUERY)
    for row in dataframe.toLocalIterator():
        filename = f"{row.code}_{slugify(row.name)}.json"
        filepath = outdir / filename
        if filepath.exists():
            raise Exception(f"Cannot write duplicate {filepath}")

        row.cards.sort(key=card_sort_key)
        row_dict = row.asDict(recursive=True)

        with filepath.open("wt") as set_file:
            json.dump(row_dict, set_file, indent=2)


def get_args() -> argparse.Namespace:
    """Get cli arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("outdir", help="output directory for json files.")
    return parser.parse_args()


def main() -> None:
    """Main sink function."""
    args = get_args()
    outdir = pathlib.Path(args.outdir)
    spark = SparkSession.builder.enableHiveSupport().getOrCreate()
    sink(spark, outdir)


if __name__ == "__main__":
    main()
