/**
 * Create the mycards table.
 *
 * Variables:
 *  `dbname`: database to create the table under
 *  `tablename`: the name of the table to create
 */
CREATE TABLE ${dbname}.${tablename}
USING delta
TBLPROPERTIES (
    delta.autoOptimize.optimizeWrite = true,
    delta.autoOptimize.autoCompact = true
)
AS
SELECT
    CAST(NULL AS string) AS my_id,
    src_mtg.raw_scryfall_cards.id AS scryfall_id,
    src_mtg.raw_scryfall_cards.name AS name
FROM
    src_mtg.raw_scryfall_cards;

SELECT * FROM ${dbname}.${tablename} LIMIT 10;
