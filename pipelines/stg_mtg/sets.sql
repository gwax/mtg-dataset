/**
 * Create the sets table.
 *
 * Variables:
 *  `dbname`: database to create the table under
 *  `tablename`: the name of the sets table to create
 */
CREATE TABLE ${dbname}.${tablename}
USING parquet
AS
SELECT
    uuid() as id,
    src_mtg.raw_scryfall_sets.code,
    src_mtg.raw_scryfall_sets.name,
    src_mtg.raw_scryfall_sets.id AS scryfall_id
FROM
    src_mtg.raw_scryfall_sets;

SELECT * FROM ${dbname}.${tablename} LIMIT 10;
