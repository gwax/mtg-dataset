"""Try a thing."""

import json
from pyspark.sql import SparkSession


def main():
    spark = SparkSession.builder.enableHiveSupport().getOrCreate()
    query = """
        SELECT
            *
        FROM
            stg_mtg.mycards
        ORDER BY
            set_code,
            CAST(REGEXP_EXTRACT(collector_number, '(\d+).*', 1) AS int),
            collector_number
    """
    resultsDF = spark.sql(query)
    # result_iter = resultsDF.toLocalIterator()
    results = resultsDF.collect()
    for i, result in enumerate(results):
        print(json.dumps(result.asDict(), sort_keys=True))
        if i > 100:
            break


if __name__ == "__main__":
    main()
