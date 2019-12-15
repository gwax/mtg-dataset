"""Build a table from a SQL SELECT statement."""

import argparse
import pathlib
import string
from typing import Dict

from pyspark.sql import DataFrame, SparkSession


def create_table(
    spark: SparkSession, fqname: str, select: str, variables: Dict[str, str]
) -> DataFrame:
    """Create a table from a select statement and return it as a dataframe."""
    select_template = string.Template(select)
    select_query = select_template.substitute(variables)
    create_query = f"CREATE TABLE {fqname} USING parquet AS {select_query}"

    drop_query = f"DROP TABLE IF EXISTS {fqname}"

    spark.sql(drop_query)
    spark.sql(create_query)
    return spark.table(fqname)


def get_args() -> argparse.Namespace:
    """Get CLI arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", required=True, help="Target database name.")
    parser.add_argument("--name", required=True, help="Target table name.")
    parser.add_argument(
        "--sqlfile", required=True, help="SQL file containing desired select statement."
    )
    parser.add_argument(
        "VARS",
        nargs="*",
        type=lambda s: s.split("="),
        help="Variables as key=value to replace ${key} in the select statement.",
    )
    args = parser.parse_args()
    try:
        args.VARS = dict(args.VARS)
    except ValueError:
        raise argparse.ArgumentTypeError(
            "VARS must be of the form key1=value1 key2=value2..."
        )
    return args


def main() -> None:
    """Script entrypoint."""
    args = get_args()

    fqtablename = f"{args.db}.{args.name}"

    sqlfilepath = pathlib.Path(args.sqlfile)
    with sqlfilepath.open("rt") as sqlfile:
        sqldata = sqlfile.read()

    spark = SparkSession.builder.enableHiveSupport().getOrCreate()

    dataframe = create_table(spark, fqtablename, sqldata, args.VARS)
    dataframe.show(10)


if __name__ == "__main__":
    main()
