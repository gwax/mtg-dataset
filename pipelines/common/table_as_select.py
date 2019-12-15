"""Build a table from a SQL SELECT statement."""

import argparse
import os
import pathlib
import string
from typing import Dict

from pyspark.sql import DataFrame, SparkSession


def create_table(
    spark: SparkSession, fqname: str, select: str, vars: Dict[str, str]
) -> DataFrame:
    """Create a table from a select statement and return it as a dataframe."""
    select_template = string.Template(select)
    select_query = select_template.substitute(vars)
    create_query = f"CREATE TABLE {fqname} USING parquet AS {select_query}"

    drop_query = f"DROP TABLE IF EXISTS {fqname}"

    spark.sql(drop_query)
    spark.sql(create_query)
    return spark.table(fqname)


def write_schema(dataframe: DataFrame, schema_path: pathlib.Path) -> None:
    """Write the schema of a dataframe to a given text file."""
    with schema_path.open("wt") as schema_file:
        # pylint: disable=protected-access
        schema_file.write(dataframe._jdf.schema().treeString())


def show_sample(dataframe: DataFrame) -> None:
    """Show a number of sample rows from the table."""
    dataframe.show(10)


def get_args() -> argparse.Namespace:
    """Get CLI arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", required=True, help="Target database name.")
    parser.add_argument(
        "--schema-dir", required=True, help="Directory to write schema info."
    )
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
    return parser.parse_args()


def main() -> None:
    """Script entrypoint."""
    args = get_args()

    sqlfilepath = pathlib.Path(args.sqlfile)
    schema_dir = pathlib.Path(args.schema_dir)

    tablename, _ = os.path.splitext(sqlfilepath.name)
    fqtablename = f"{args.db}.{tablename}"
    schema_path = schema_dir / f"{fqtablename}.txt"

    with sqlfilepath.open("rt") as sqlfile:
        sqldata = sqlfile.read()
    schema_dir.mkdir(parents=True, exist_ok=True)

    spark = SparkSession.builder.enableHiveSupport().getOrCreate()

    dataframe = create_table(spark, fqtablename, sqldata, args.VARS)
    write_schema(dataframe, schema_path)
    show_sample(dataframe)


if __name__ == "__main__":
    main()
