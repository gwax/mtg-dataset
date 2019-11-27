/**
 * Create a raw table from an input jsonlines file.
 *
 * Variables:
 *  `dbname`: database to create the table under
 *  `name`: the name of the table to create
 *  `input_file`: the path to the jsonlines file to ingest
 */
CREATE TEMPORARY VIEW input_data
USING json
OPTIONS (
    path "${input_file}"
);

CREATE TABLE ${dbname}.${tablename}
USING parquet
AS SELECT * FROM input_data;

SELECT * FROM ${dbname}.${tablename} LIMIT 10;
