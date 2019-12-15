"""Sink all table schemas as trees in text files."""

import argparse
import pathlib

from pyspark.sql import SparkSession


def write_schemas(spark: SparkSession, outdir: pathlib.Path) -> None:
    """Write all schemas to the target directory."""
    for database in spark.catalog.listDatabases():
        for table in spark.catalog.listTables(database.name):
            tablename = f"{database.name}.{table.name}"
            schema_path = outdir / f"{tablename}.txt"
            dataframe = spark.table(f"{database.name}.{table.name}")
            with schema_path.open("wt") as schema_file:
                # pylint: disable=protected-access
                schema_file.write(dataframe._jdf.schema().treeString())


def get_args() -> argparse.Namespace:
    """Get CLI arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("outdir", help="Output directory for schema descriptions.")
    return parser.parse_args()


def main() -> None:
    """Main sink function."""
    args = get_args()
    outdir = pathlib.Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    spark = SparkSession.builder.enableHiveSupport().getOrCreate()
    write_schemas(spark, outdir)


if __name__ == "__main__":
    main()
