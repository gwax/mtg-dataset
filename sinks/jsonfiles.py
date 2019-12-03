"""Sink data to json."""

import argparse
import json
import pathlib

from pyspark.sql import SparkSession
from slugify import slugify


def get_args():
    """Get cli arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("outdir", help="output directory for json files.")
    return parser.parse_args()


def main():
    """Main sink function."""
    args = get_args()
    outdir = pathlib.Path(args.outdir)

    spark = SparkSession.builder.enableHiveSupport().getOrCreate()
    query = r"""
        SELECT
            LPAD(REGEXP_EXTRACT(collector_number, '(\\d+)(.*)', 1), 4, '0')
                || REGEXP_EXTRACT(collector_number, '(\\d+)(.*)', 2)
                AS padded_collector_number,
            *
        FROM
            stg_mtg.mycards
    """
    results_df = spark.sql(query)
    for row in results_df.toLocalIterator():
        filename = f"{row.padded_collector_number}_{slugify(row.name)}.json"
        row_dict = row.asDict()
        del row_dict["padded_collector_number"]

        set_dir = outdir / row_dict['set_code']
        set_dir.mkdir(parents=True, exist_ok=True)

        row_filepath = set_dir / filename
        with row_filepath.open("wt") as row_file:
            json.dump(row_dict, row_file, indent=4, sort_keys=True)


if __name__ == "__main__":
    main()
