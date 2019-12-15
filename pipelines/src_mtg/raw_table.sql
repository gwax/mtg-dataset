/**
* Create a raw table from an input jsonlines file.
*
* Variables:
*  `input_file`: the path to the jsonlines file to ingest
**/

SELECT * FROM json.`${input_file}`
