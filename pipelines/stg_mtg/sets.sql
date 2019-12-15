/**
* Select to construct all sets data.
**/

SELECT
    COALESCE(rc.id, uuid()) AS id,
    UPPER(sf.code) AS code,
    sf.name AS name,
    sf.id AS scryfall_id
FROM
    src_mtg.raw_recycle_sets AS rc
    FULL OUTER JOIN src_mtg.raw_scryfall_sets AS sf
        ON rc.scryfall_id = sf.id
