/**
* Select to construct all cards data.
**/

SELECT
    COALESCE(rc.id, uuid()) AS id,
    UPPER(sf.set) AS set_code,
    sf.collector_number AS collector_number,
    sf.name AS name,
    sf.id AS scryfall_id
FROM
    src_mtg.raw_recycle_cards AS rc
    FULL OUTER JOIN src_mtg.raw_scryfall_cards AS sf
        ON rc.scryfall_id = sf.id
