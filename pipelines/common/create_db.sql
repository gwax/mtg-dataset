/**
 * Create a database with the given name under the warehouse dir.
 *
 * Variables:
 *  `dbname`: the name of the database to create
 *  `location`: the path to the database storage
 */
CREATE DATABASE ${dbname}
LOCATION '${location}';
