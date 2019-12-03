/**
 * Create the mycards table.
 *
 * Variables:
 *  `dbname`: database to create the table under
 *  `tablename`: the name of the table to create
 */
CREATE TABLE ${dbname}.${tablename}
USING parquet
AS
SELECT
    uuid() AS my_id,
    src_mtg.raw_scryfall_cards.set AS set_code,
    src_mtg.raw_scryfall_cards.collector_number AS collector_number,
    src_mtg.raw_scryfall_cards.name AS name,
    src_mtg.raw_scryfall_cards.id AS scryfall_id
FROM
    src_mtg.raw_scryfall_cards;

SELECT * FROM ${dbname}.${tablename} LIMIT 10;
