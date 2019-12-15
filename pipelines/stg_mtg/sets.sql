/**
* Create the sets table.
*
* Variables:
*  `dbname`: database to create the table under
*  `tablename`: the name of the sets table to create
**/

DROP TABLE IF EXISTS ${dbname}.${tablename};
CREATE TABLE ${dbname}.${tablename}
USING parquet
AS
SELECT
    COALESCE(rc.id, uuid()) AS id,
    UPPER(sf.code) AS code,
    sf.name AS name,
    sf.id AS scryfall_id
FROM
    src_mtg.raw_recycle_sets AS rc
    FULL OUTER JOIN src_mtg.raw_scryfall_sets AS sf
        ON rc.scryfall_id = sf.id;

SELECT * FROM ${dbname}.${tablename} LIMIT 10
