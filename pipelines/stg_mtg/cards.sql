/**
 * Create the cards table.
 *
 * Variables:
 *  `dbname`: database to create the table under
 *  `tablename`: the name of the table to create
 */

DROP TABLE IF EXISTS ${dbname}.${tablename};
CREATE TABLE ${dbname}.${tablename}
USING parquet
AS
SELECT
    COALESCE(rc.id, uuid()) AS id,
    sf.set AS set_code,
    sf.collector_number AS collector_number,
    sf.name AS name,
    sf.id AS scryfall_id
FROM
    src_mtg.raw_recycle_cards AS rc
    FULL OUTER JOIN src_mtg.raw_scryfall_cards AS sf
        ON rc.scryfall_id = sf.id;

SELECT * FROM ${dbname}.${tablename} LIMIT 10
